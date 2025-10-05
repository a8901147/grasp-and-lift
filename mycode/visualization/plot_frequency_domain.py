import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

def plot_frequency_domain(subject_series):
    """
    Plots the frequency domain signal (FFT) for a given subject and series.

    Args:
        subject_series (str): The subject and series identifier (e.g., 'subj1_series1').
    """
    script_dir = os.path.dirname(__file__)
    data_file = os.path.join(script_dir, '..', '..', 'data', 'train', f'{subject_series}_data.csv')
    output_dir = os.path.join(script_dir, '..', '..', 'out', subject_series)
    output_file = os.path.join(output_dir, 'frequency_domain.png')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the data
    try:
        data = pd.read_csv(data_file, index_col='id')
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_file}")
        return

    # --- FFT Calculation ---
    sampling_rate = 500  # 500 Hz
    n = len(data)
    fft_freq = np.fft.rfftfreq(n, d=1./sampling_rate)

    # Plot all 32 channels
    plt.figure(figsize=(20, 15))
    for i, col in enumerate(data.columns):
        # Get the signal for the current channel
        signal = data[col].values

        # Compute FFT
        fft_vals = np.fft.rfft(signal)
        fft_mag = np.abs(fft_vals)

        plt.subplot(8, 4, i + 1)
        plt.plot(fft_freq, fft_mag)
        plt.title(col)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.grid(True)

    plt.suptitle(f'Frequency Domain (FFT) for {subject_series}', fontsize=24)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save the plot
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot EEG frequency domain signals.')
    parser.add_argument('subject_series', type=str, help='Subject and series identifier (e.g., subj1_series1)')
    args = parser.parse_args()

    plot_frequency_domain(args.subject_series)
