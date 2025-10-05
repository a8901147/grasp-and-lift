import pandas as pd
import numpy as np
import pywt
import matplotlib.pyplot as plt
import os
import argparse

def plot_wavelet(subject_series):
    """
    Plots the Wavelet Transform (Scalogram) for a given subject and series.

    Args:
        subject_series (str): The subject and series identifier (e.g., 'subj1_series1').
    """
    script_dir = os.path.dirname(__file__)
    data_file = os.path.join(script_dir, '..', '..', 'data', 'train', f'{subject_series}_data.csv')
    output_dir = os.path.join(script_dir, '..', '..', 'out', subject_series)
    output_file = os.path.join(output_dir, 'wavelet_scalogram.png')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the data
    try:
        data = pd.read_csv(data_file, index_col='id')
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_file}")
        return

    # --- Wavelet Calculation ---
    sampling_rate = 500  # 500 Hz
    wavelet = 'cmor1.5-1.0' # Complex Morlet wavelet
    scales = np.arange(1, 128)
    
    plt.figure(figsize=(20, 15))
    for i, col in enumerate(data.columns):
        # Get the signal for the current channel
        signal = data[col].values

        # Perform CWT
        coefficients, frequencies = pywt.cwt(signal, scales, wavelet, 1.0/sampling_rate)
        time = np.arange(0, len(signal)) / sampling_rate

        plt.subplot(8, 4, i + 1)
        plt.pcolormesh(time, frequencies, np.abs(coefficients))
        plt.title(col)
        plt.ylabel('Freq [Hz]')
        plt.xlabel('Time [sec]')
        plt.ylim(1, 150)

    plt.suptitle(f'Wavelet Scalogram for {subject_series}', fontsize=24)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save the plot
    plt.savefig(output_file)
    print(f"Wavelet plot saved to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot EEG Wavelet Scalogram.')
    parser.add_argument('subject_series', type=str, help='Subject and series identifier (e.g., subj1_series1)')
    args = parser.parse_args()

    plot_wavelet(args.subject_series)
