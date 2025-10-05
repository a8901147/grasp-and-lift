import pandas as pd
import numpy as np
from scipy.signal import stft
import matplotlib.pyplot as plt
import os
import argparse

def plot_stft(subject_series):
    """
    Plots the Short-Time Fourier Transform (STFT) for a given subject and series.

    Args:
        subject_series (str): The subject and series identifier (e.g., 'subj1_series1').
    """
    script_dir = os.path.dirname(__file__)
    data_file = os.path.join(script_dir, '..', '..', 'data', 'train', f'{subject_series}_data.csv')
    output_dir = os.path.join(script_dir, '..', '..', 'out', subject_series)
    output_file = os.path.join(output_dir, 'stft_spectrogram.png')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the data
    try:
        data = pd.read_csv(data_file, index_col='id')
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_file}")
        return

    # --- STFT Calculation ---
    sampling_rate = 500  # 500 Hz

    plt.figure(figsize=(20, 15))
    for i, col in enumerate(data.columns):
        # Get the signal for the current channel
        signal = data[col].values

        # Compute STFT
        f, t, Zxx = stft(signal, fs=sampling_rate, nperseg=256)

        plt.subplot(8, 4, i + 1)
        # Limit frequency range for better visualization
        f_mask = f <= 100 
        plt.pcolormesh(t, f[f_mask], np.abs(Zxx[f_mask, :]), shading='gouraud')
        plt.title(col)
        plt.ylabel('Freq [Hz]')
        plt.xlabel('Time [sec]')

    plt.suptitle(f'STFT Spectrogram for {subject_series}', fontsize=24)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save the plot
    plt.savefig(output_file)
    print(f"STFT plot saved to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot EEG STFT Spectrogram.')
    parser.add_argument('subject_series', type=str, help='Subject and series identifier (e.g., subj1_series1)')
    args = parser.parse_args()

    plot_stft(args.subject_series)
