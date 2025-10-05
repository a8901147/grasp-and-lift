import pandas as pd
import numpy as np
from scipy.signal import welch
import matplotlib.pyplot as plt
import os
import argparse

def plot_psd(subject_series):
    """
    Plots the Power Spectral Density (PSD) for a given subject and series.

    Args:
        subject_series (str): The subject and series identifier (e.g., 'subj1_series1').
    """
    script_dir = os.path.dirname(__file__)
    data_file = os.path.join(script_dir, '..', '..', 'data', 'train', f'{subject_series}_data.csv')
    output_dir = os.path.join(script_dir, '..', '..', 'out', subject_series)
    output_file = os.path.join(output_dir, 'psd.png')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the data
    try:
        data = pd.read_csv(data_file, index_col='id')
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_file}")
        return

    # --- PSD Calculation ---
    sampling_rate = 500  # 500 Hz

    # Plot all 32 channels
    plt.figure(figsize=(20, 15))
    for i, col in enumerate(data.columns):
        # Get the signal for the current channel
        signal = data[col].values

        # Compute PSD using Welch's method
        freqs, psd = welch(signal, fs=sampling_rate, nperseg=1024)

        plt.subplot(8, 4, i + 1)
        plt.semilogy(freqs, psd) # Use a logarithmic scale for the y-axis
        plt.title(col)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power/Frequency (dB/Hz)')
        plt.grid(True)

    plt.suptitle(f'Power Spectral Density (PSD) for {subject_series}', fontsize=24)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save the plot
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot EEG Power Spectral Density (PSD).')
    parser.add_argument('subject_series', type=str, help='Subject and series identifier (e.g., subj1_series1)')
    args = parser.parse_args()

    plot_psd(args.subject_series)
