import argparse
import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
from datetime import datetime

# Add the script's directory to the Python path to allow for module imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

from train import train_model
from evaluate import evaluate_model

def parse_subject_ids(subject_str):
    """
    Parses a subject ID string (e.g., '1', '1,2', '1-5', 'all') into a list of integers.
    """
    if subject_str.lower() == 'all':
        return list(range(1, 13))
    
    subjects = []
    parts = subject_str.split(',')
    for part in parts:
        part = part.strip()
        try:
            if '-' in part:
                start, end = map(int, part.split('-'))
                subjects.extend(range(start, end + 1))
            else:
                subjects.append(int(part))
        except ValueError:
            print(f"Error: Invalid subject format '{part}'. Please use formats like '1', '1,2', or '1-5'.")
            sys.exit(1)
    return subjects

def get_channels(channel_arg):
    """
    Gets a list of channels based on the input argument.
    """
    if channel_arg.lower() == 'all':
        return ['Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6', 'T7', 'C3', 'Cz', 'C4', 'T8', 'TP9', 'CP5', 'CP1', 'CP2', 'CP6', 'TP10', 'P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10']
    else:
        return [channel_arg]

ALL_EVENTS = ['HandStart', 'FirstDigitTouch', 'BothStartLoadPhase', 'LiftOff', 'Replace', 'BothReleased']


def plot_and_save_results(results, title, event, file_path, average_auc=None):
    """
    Sorts results, plots them as a bar chart, and saves the figure.
    """
    if not results:
        print(f"No results to plot for {title}.")
        return

    sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)
    channels = [item[0] for item in sorted_results]
    scores = [item[1] for item in sorted_results]

    plt.figure(figsize=(14, 8))
    ax = sns.barplot(x=channels, y=scores, palette="viridis")
    
    plot_title = f'AUC Scores for {title} - Event: {event}'
    if average_auc is not None:
        plot_title += f' (Avg AUC: {average_auc:.4f})'
    ax.set_title(plot_title, fontsize=16)

    ax.set_xlabel('Channel', fontsize=12)
    ax.set_ylabel('AUC Score', fontsize=12)
    ax.set_ylim(0, 1)
    plt.xticks(rotation=45, ha='right')
    
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.4f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=9, color='black', xytext=(0, 5),
                    textcoords='offset points')

    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

def plot_and_save_summary_results(all_results, subjects, event, heatmap_path, boxplot_path):
    """
    Generates and saves a heatmap and a boxplot for summary results across all subjects.
    """
    df = pd.DataFrame(all_results).T
    df.index.name = 'Subject'
    
    # --- Dynamic Title Generation ---
    if sorted(subjects) == list(range(1, 13)):
        subject_title_str = "All Subjects (1-12)"
    else:
        # Sort numerically and create string (e.g., "Subjects 1, 2, 5")
        subject_str = ', '.join(map(str, sorted(subjects)))
        subject_title_str = f"Subjects {subject_str}"

    # Heatmap
    plt.figure(figsize=(20, 10))
    sns.heatmap(df, annot=True, fmt=".4f", cmap="viridis", linewidths=.5)
    plt.title(f'AUC Score Heatmap for {subject_title_str} - Event: {event}', fontsize=16)
    plt.xlabel('Channel', fontsize=12)
    plt.ylabel('Subject', fontsize=12)
    plt.tight_layout()
    plt.savefig(heatmap_path)
    plt.close()

    # Boxplot
    df_melted = df.melt(var_name='Channel', value_name='AUC')
    median_order = df.median().sort_values(ascending=False).index
    
    plt.figure(figsize=(20, 10))
    ax = sns.boxplot(x='Channel', y='AUC', data=df_melted, palette='coolwarm', order=median_order)
    ax.set_title(f'Channel Performance Distribution for {subject_title_str} - Event: {event}', fontsize=16)
    ax.set_xlabel('Channel', fontsize=12)
    ax.set_ylabel('AUC Score', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(boxplot_path)
    plt.close()

def print_channel_ranking(all_results, event):
    """
    Prints a markdown table of channel rankings for each subject.
    """
    print("\n\n###########################################################")
    print(f"        Full Channel Ranking per Subject for Event: {event}")
    print("###########################################################")
    
    header = "| Subject    | All Channels Sorted by AUC (Channel | AUC Score)                                                                         |"
    separator = "|------------|--------------------------------------------------------------------------------------------------------------------------|"
    print(header)
    print(separator)

    for subj_name, results in all_results.items():
        sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)
        ranking_str = " ".join([f"{ch}({auc:.4f})" for ch, auc in sorted_results])
        print(f"| {subj_name: <10} | {ranking_str: <124} |")
    
    print("###########################################################\n")

def main():
    """
    Main function to run the EEG analysis pipeline.
    """
    parser = argparse.ArgumentParser(description="Run EEG signal analysis.")
    parser.add_argument('subject', help="Subject ID(s) (e.g., '1', '1,2', '1-3', or 'all').")
    parser.add_argument('channel', help="Channel name(s) (e.g., 'Fp1', or 'all').")
    parser.add_argument('event', help="Event name (e.g., 'HandStart').")
    parser.add_argument('--output_dir', type=str, default='./out',
                        help='Directory to save the output plots.')
    parser.add_argument('--model_dir', default='./out', help="Directory to save models.")
    parser.add_argument('--feature-extractor', default=None, choices=['filterbank', None], help="Specify the feature extractor to use (e.g., 'filterbank').")
    parser.add_argument('--filterbank-freqs', type=str, default=None, help="Custom filterbank frequencies as a comma-separated string (e.g., '0.1,1,3,5,7,10,14,20,28,38').")
    args = parser.parse_args()

    # --- Parse custom filterbank frequencies if provided ---
    custom_freqs = None
    if args.filterbank_freqs:
        if args.feature_extractor != 'filterbank':
            print("Warning: --filterbank-freqs is provided but --feature-extractor is not 'filterbank'. The custom frequencies will be ignored.")
        try:
            custom_freqs = [[float(f)] for f in args.filterbank_freqs.split(',')]
        except ValueError:
            print("Error: Invalid format for --filterbank-freqs. Please use a comma-separated list of numbers.")
            sys.exit(1)

    # If using the default output directory, create a unique subfolder to avoid conflicts
    if args.output_dir == './out':
        # Sanitize subject and channel args for folder names
        subj_str = args.subject.replace(',', '-').replace(' ', '')
        chan_str = args.channel.replace(',', '-').replace(' ', '')
        run_name = f"subj-{subj_str}_chan-{chan_str}_evt-{args.event}"
        
        base_dir = args.output_dir
        args.output_dir = os.path.join(base_dir, run_name, 'results')
        # Also redirect model_dir to be inside the unique run folder
        args.model_dir = os.path.join(base_dir, run_name, 'model')
        print(f"Default directory used. Saving outputs to unique folder: {os.path.join(base_dir, run_name)}")
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.model_dir, exist_ok=True)

    subjects = parse_subject_ids(args.subject)
    channels = get_channels(args.channel)
    
    # --- Normalize and Validate Event Name (Case-Insensitive) ---
    event_name = next((e for e in ALL_EVENTS if e.lower() == args.event.lower()), None)
    if not event_name:
        print(f"Error: Invalid event name '{args.event}'.")
        sys.exit(1)
    event = event_name

    print("--- Starting Analysis ---")
    print(f"Subjects: {args.subject} -> {subjects}")
    print(f"Channels: {args.channel}, Event: {event}")
    print(f"Output Directory: {args.output_dir}")

    all_results = {}

    for subj in subjects:
        subj_results = {}
        for chan in tqdm(channels, desc=f"Processing Subject {subj} for event {event}", unit="channel"):
            model_path = os.path.join(args.model_dir, f"subj{subj}_{event.lower()}_{chan}_model.joblib")
            train_model(subj, chan, event, args.model_dir, 
                        feature_extractor=args.feature_extractor,
                        filterbank_custom_freqs=custom_freqs)
            auc_score = evaluate_model(subj, chan, event, model_path)
            subj_results[chan] = auc_score
        all_results[f"subj{subj}"] = subj_results

        # --- Calculate and Print Average AUC for the subject ---
        if subj_results:
            avg_auc = sum(subj_results.values()) / len(subj_results)
            print(f"  -> Subject {subj} Average AUC: {avg_auc:.4f}")


    print_channel_ranking(all_results, event)
    
    print("\n--- Generating and Saving Detailed Plots ---")
    for subj_name, results in all_results.items():
        subj_id = subj_name.replace('subj', '')
        # --- Calculate average AUC for plotting ---
        avg_auc_plot = sum(results.values()) / len(results) if results else None
        plot_path = os.path.join(args.output_dir, f"subj{subj_id}_{event}_channel_ranking.png")
        plot_and_save_results(results, f"Subject {subj_id}", event, plot_path, average_auc=avg_auc_plot)
        print(f"Plot saved for {subj_name} to {plot_path}")

    if len(subjects) > 1:
        print("\n--- Generating and Saving Summary Plots ---")
        heatmap_path = os.path.join(args.output_dir, f"summary_{event}_heatmap.png")
        boxplot_path = os.path.join(args.output_dir, f"summary_{event}_channel_boxplot.png")
        plot_and_save_summary_results(all_results, subjects, event, heatmap_path, boxplot_path)
        print(f"Summary heatmap saved to {heatmap_path}")
        print(f"Summary boxplot saved to {boxplot_path}")
    
    # --- Calculate and Print Overall Average AUC ---
    all_scores = [score for subj_results in all_results.values() for score in subj_results.values()]
    if all_scores:
        overall_avg_auc = sum(all_scores) / len(all_scores)
        print("\n###########################################################")
        print(f"  Overall Average AUC across all subjects: {overall_avg_auc:.4f}")
        print("###########################################################")

    print("--- Analysis Complete ---")

if __name__ == "__main__":
    main()
