import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def plot_events(subject_series):
    """
    Plots the events for a given subject and series.

    Args:
        subject_series (str): The subject and series in the format "subjX_seriesY".
    """
    # Construct the file path
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "..", "..", "data", "train", f"{subject_series}_events.csv")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Read the event data
    try:
        events_df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Get the event columns
    event_columns = events_df.columns[1:]

    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(15, 5))

    # Plot each event
    for i, event in enumerate(event_columns):
        event_times = events_df[events_df[event] == 1].index
        ax.eventplot(event_times, lineoffsets=i + 1, linelengths=0.8, label=event)

    # Generate values for the vertical lines (every 10k)
    end_val = events_df.index[-1]
    lines_values = list(range(0, end_val + 1, 10000))

    # Draw vertical lines every 10k
    for tick in lines_values:
        ax.axvline(x=tick, color='r', linestyle=':')

    # Set plot labels and title
    ax.set_yticks(range(1, len(event_columns) + 1))
    ax.set_yticklabels(event_columns)
    ax.set_xlabel("Frame")
    ax.set_title(f"Event Occurrences for {subject_series}")
    ax.legend()
    plt.grid(True)

    # Save the plot
    output_dir = os.path.join(script_dir, "..", "..", "out", subject_series)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "events.png")
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python plot_events.py <subject_series>")
        print("Example: python plot_events.py subj1_series1")
        sys.exit(1)

    subject_series = sys.argv[1]
    plot_events(subject_series)
