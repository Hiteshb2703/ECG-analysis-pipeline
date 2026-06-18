<<<<<<< HEAD
import numpy as np
import os
import matplotlib.pyplot as plt 
import data
from filter import bandpass_filter
from peaks import extract_all_peaks
from features import extract_features, summarize_features
from llm_report import generate_ecg_report_with_ollama
from pdf_report import create_ecg_report

fs = 125 

def main():
    ecg_signal = data.load_ecg_data()
    if ecg_signal is None: return

    filtered = bandpass_filter(ecg_signal, fs=fs)
    r_peaks, p_peaks, q_peaks, s_peaks, t_peaks, rr_intervals = extract_all_peaks(filtered, fs=fs)

    plt.figure(figsize=(10, 4))
    plt.plot(filtered, label="Filtered ECG")
    plt.plot(r_peaks, filtered[r_peaks], "ro", label="R-peaks")
    plt.title("Detected Heartbeats")
    plt.legend()
    plot_path = "ecg_plot.png"
    plt.savefig(plot_path)
    plt.close()

    raw_features = extract_features(
        filtered_ecg=filtered,
        rr_intervals=rr_intervals,
        r_peaks=r_peaks,
        p_peaks=p_peaks,
        q_peaks=q_peaks,
        s_peaks=s_peaks,
        t_peaks=t_peaks,
        fs=fs
    )

    summary_features = summarize_features(raw_features)
    interpretation = generate_ecg_report_with_ollama(summary_features)
    print(interpretation)
    create_ecg_report(summary_features, interpretation, plot_path=plot_path)

    print("\n DONE! ECG_Report.pdf generated successfully.\n")

if __name__ == "__main__":
    main()
=======
# main.py
import numpy as np
import os

from filter import bandpass_filter
from peaks import extract_all_peaks
from features import extract_features, summarize_features
from llm_report import generate_ecg_report_with_ollama
from pdf_report import create_ecg_report

fs = 500  # ECG sampling rate

def main():
    print("📥 Loading ECG.dat ...")
    ecg_signal = np.loadtxt("ECG.dat")

    print("🔧 Filtering ECG ...")
    filtered = bandpass_filter(ecg_signal, fs=fs)

    print("📌 Detecting peaks ...")
    r_peaks, p_peaks, q_peaks, s_peaks, t_peaks, rr_intervals = extract_all_peaks(filtered, fs=fs)

    print("📊 Extracting raw features ...")
    raw_features = extract_features(
        filtered_ecg=filtered,
        rr_intervals=rr_intervals,
        r_peaks=r_peaks,
        p_peaks=p_peaks,
        q_peaks=q_peaks,
        s_peaks=s_peaks,
        t_peaks=t_peaks,
        fs=fs
    )

    print("📝 Summarizing features ...")
    summary_features = summarize_features(raw_features)

    print("🧠 Generating AI interpretation (Ollama) ...")
    interpretation = generate_ecg_report_with_ollama(summary_features)
    print("\n--- ECG INTERPRETATION ---\n")
    print(interpretation)

    print("📄 Creating PDF report ...")
    plot_path = "ecg_plot.png"
    if not os.path.exists(plot_path):
        plot_path = None

    create_ecg_report(raw_features, interpretation, plot_path=plot_path)

    print("\n✅ DONE! ECG_Report.pdf generated successfully.\n")


if __name__ == "__main__":
    main()
>>>>>>> 3952caf0e3a2b39da37dc33231d04ec6179eacae
