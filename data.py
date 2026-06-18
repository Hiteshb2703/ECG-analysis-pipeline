import pandas as pd
import numpy as np
import os

def load_ecg_data():
    file_path = "mitbih_test.csv" 
    
    if not os.path.exists(file_path):
        if os.path.exists("mitbih_test"):
            file_path = "mitbih_test"
        else:
            print("ERROR: mitbih_test.csv not found!")
            return None

    df = pd.read_csv(file_path, header=None)
    arrhythmia_data = df[df.iloc[:, -1] != 0]
    
    if not arrhythmia_data.empty:
        signal = arrhythmia_data.iloc[0, :-1].values
    else:
        signal = df.iloc[0, :-1].values

    return np.tile(signal, 5)