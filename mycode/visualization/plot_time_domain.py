import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse
import math

def plot_time_domain(subject_series):
    """
    Plots the time domain signal for a given subject and series.

    Args:
        subject_series (str): The subject and series identifier (e.g., 'subj1_series1').
    """
    script_dir = os.path.dirname(__file__)
    data_file = os.path.join(script_dir, '..', '..', 'data', 'train', f'{subject_series}_data.csv')
    output_dir = os.path.join(script_dir, '..', '..', 'out', subject_series)
    output_file = os.path.join(output_dir, 'time_domain.png')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the data
    try:
        data = pd.read_csv(data_file, index_col='id')
        # Extract frame number from index and set as new index
        data['frame'] = data.index.str.split('_').str[-1].astype(int)
        data = data.set_index('frame')
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_file}")
        return

    # Plot all 32 channels
    plt.figure(figsize=(20, 15))
    n_frames = len(data.index)
    start_val = data.index[0]
    end_val = data.index[-1]

    # Calculate label values with rounding up to nearest 10k
    val_25 = math.ceil(n_frames * 0.25 / 10000) * 10000
    val_50 = math.ceil(n_frames * 0.50 / 10000) * 10000
    val_75 = math.ceil(n_frames * 0.75 / 10000) * 10000
    label_values = [start_val, val_25, val_50, val_75, end_val]

    # Generate values for the vertical lines (every 10k)
    lines_values = list(range(0, end_val + 1, 10000))

    for i, col in enumerate(data.columns):
        ax = plt.subplot(8, 4, i + 1)
        ax.plot(data.index, data[col])
        
        ax.set_title(col)

        # Draw vertical lines every 10k
        for tick in lines_values:
            ax.axvline(x=tick, color='r', linestyle=':')
        
        ax.set_yticks([]) # Keep y-ticks off as before

        if (i // 4) % 2 == 0: # Only show x-ticks for even rows (0-based)
            ax.set_xticks(label_values)
            ax.set_xticklabels(label_values, fontsize=6)
        else:
            ax.set_xticks([])

    plt.suptitle(f'Time Domain Signals for {subject_series}', fontsize=24)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save the plot
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot EEG time domain signals.')
    parser.add_argument('subject_series', type=str, help='Subject and series identifier (e.g., subj1_series1)')
    args = parser.parse_args()

    plot_time_domain(args.subject_series)