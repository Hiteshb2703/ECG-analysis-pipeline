import requests

def generate_llm_interpretation(features):
    """
    Sends ECG features to a local Ollama instance and returns a clinical summary.
    """
    model = "llama3" 
    
    prompt = f"""
    You are a cardiologist's assistant. Analyze the following extracted ECG metrics:
    - Heart Rate: {features.get('hr', 'N/A')} bpm
    - HRV (RMSSD): {features.get('rmssd', 'N/A')} ms
    - QRS Duration: {features.get('qrs_dur', 'N/A')} ms
    - PR Interval: {features.get('pr_int', 'N/A')} ms
    - QT Interval: {features.get('qt_int', 'N/A')} ms

    Provide a brief, professional clinical summary of these findings. 
    Keep the tone objective and concise.
    """

    url = "http://localhost:11434/api/generate"
    
    data_to_send = {
        "model": model,
        "prompt": prompt,
        "stream": False 
    }

    try:
        response = requests.post(url, json=data_to_send)
        result = response.json()
        return result.get("response", "Error: No response from LLM.")

    except Exception as e:
        return f"LLM Error: Could not connect to Ollama. ({e})"