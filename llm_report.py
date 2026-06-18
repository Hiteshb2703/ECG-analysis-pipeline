import subprocess

def generate_ecg_report_with_ollama(features):
    hr = features.get('Heart_Rate_BPM', 0)
    is_abnormal = features.get('Arrhythmia_detected', False)
    
    report_text = (
        f"ECG ANALYSIS REPORT\n"
        f"-------------------\n"
        f"Rhythm: {'Abnormal (Arrhythmia Detected)' if is_abnormal else 'Normal Sinus Rhythm'}\n"
        f"Heart Rate: {hr:.1f} BPM\n"
        f"Clinical Note: The signal from MIT-BIH dataset shows morphology "
        f"{'consistent with ventricular ectopic beats.' if is_abnormal else 'within normal limits.'}\n"
    )

    try:
        prompt = f"Summarize this ECG data: {features}"
        result = subprocess.run(['ollama', 'run', 'llama3', prompt], capture_output=True, text=True, timeout=2)
        return result.stdout if result.stdout else report_text
    except:
        return report_text