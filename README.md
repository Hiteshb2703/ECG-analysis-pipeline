# ECG-analysis-pipeline
A signal processing pipeline for ECG analysis that extracts clinical features 
from raw ECG data and generates natural language diagnostic reports using a 
locally run LLM.
## What it does

Takes a raw single-channel ECG signal (.dat format, 500 Hz) and runs it through 
a five stage pipeline:

1. Filtering: Butterworth bandpass filter (0.5–40 Hz, order 4, zero-phase) 
   to remove baseline wander and high-frequency noise while preserving QRS 
2. Peak Detection: Differentiation + squaring + moving-average energy envelope 
   to robustly locate R-peaks, followed by fixed-window search for P, Q, S, T peaks
3. Feature Extraction: Computes heart rate, HRV metrics (RMSSD, RR std), 
   PR interval, QRS duration, and QT interval
4. LLM Interpretation: Feeds extracted features to a locally-run Ollama model 
   for natural language rhythm analysis (no patient data used)
5. Report Generation: Outputs a structured PDF with signal plots and 
   the LLM generated clinical summary

## Pipeline
    ECG.dat → bandpass_filter() → extract_all_peaks() → extract_features() → Ollama LLM → ECG_Report.pdf

## How to run

```bash
# Install dependencies
pip install numpy scipy reportlab ollama

# Run Ollama locally
ollama serve

# Run the pipeline
python main.py
```

## Design decisions

1. Local LLM over cloud API: ECG data is sensitive,keeping inference 
  local avoids sending patient data to external servers.
2. Zero-phase filtering (filtfilt): Forward-backward filtering eliminates phase 
  delay, critical for accurate peak timing.
3. Butterworth over Chebyshev: Maximally flat passband avoids distorting QRS 
   data; rolloff sharpness is less critical than passband flatness for ECG.

## Limitations

1. Peak detection uses fixed windows relative to R.
2. Not validated against annotated databases like MIT-BIH Arrhythmia Database.
