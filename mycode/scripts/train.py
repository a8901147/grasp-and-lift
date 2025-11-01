
import os
import sys
import pandas as pd
import joblib
from tqdm import tqdm
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from feature_engineering import FilterBank, CSPFeatureExtractor
import argparse

# --- Feature Extractor Mapping ---
EXTRACTOR_MAP = {
    'FilterBank': FilterBank,
    'CSP': CSPFeatureExtractor
}
# ---------------------------------

# Constants
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/train'))
DEFAULT_TRAIN_SERIES = list(range(1, 7))  # Default: Series 1-6 for training


# --- Constants ---
ALL_CHANNELS = [
    'Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6', 
    'T7', 'C3', 'Cz', 'C4', 'T8', 'TP9', 'CP5', 'CP1', 'CP2', 'CP6', 'TP10', 
    'P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10'
]
ALL_EVENTS = ['HandStart', 'FirstDigitTouch', 'BothStartLoadPhase', 'LiftOff', 'Replace', 'BothReleased']

def parse_series(series_str):
    """Parses a series string (e.g., '1,2,3' or '1-6') into a list of integers."""
    series = []
    parts = series_str.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            series.extend(range(start, end + 1))
        else:
            series.append(int(part))
    return series

def load_data_for_series(subject, series_list, event, channel, verbose=True):
    """Loads and combines data for a specific subject and list of series."""
    all_dfs = []
    # Use tqdm for a progress bar, but disable it in non-verbose mode
    desc = f"Loading train data for Subj {subject} ({event}/{channel})"
    for series in tqdm(series_list, desc=desc, disable=not verbose):
        data_file = f"{DATA_DIR}/subj{subject}_series{series}_data.csv"
        event_file = f"{DATA_DIR}/subj{subject}_series{series}_events.csv"
        df_data = pd.read_csv(data_file, index_col='id')
        df_events = pd.read_csv(event_file, index_col='id')
        df_merged = df_data.join(df_events)
        all_dfs.append(df_merged)
    if not all_dfs:
        raise FileNotFoundError(f"No data found for subject {subject} in series {list(series_list)} at {DATA_DIR}")
    return pd.concat(all_dfs)

def load_data(subject, series_list, event, channels, verbose=True):
    """
    Loads data for a subject and series, then extracts features and target.
    """
    # Create a descriptive string for the progress bar
    channel_desc = channels[0] if len(channels) == 1 else 'all'
    df = load_data_for_series(subject, series_list, event, channel_desc, verbose=verbose)
    
    # Ensure all requested channels and the event column exist
    for col in channels + [event]:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in the loaded data.")
            
    X_train = df[channels]
    y_train = df[event]
    return X_train, y_train

def train_model(subjects, channel, event, output_dir, train_series=DEFAULT_TRAIN_SERIES, feature_extractor_str='', filterbank_custom_freqs=None, model_filename=None, verbose=True):
    """
    Trains a model for a specific subject(s), channel(s), and event.

    Args:
        subjects (list): A list of subject IDs.
        channel (str): The channel name or 'all' for multichannel processing.
        event (str): The event name.
        output_dir (str): The directory to save the trained model.
        train_series (list): A list of series numbers to use for training.
        feature_extractor_str (str, optional): A comma-separated string of feature extractors.
        filterbank_custom_freqs (list, optional): Custom frequencies for the FilterBank.
        model_filename (str, optional): Specific filename for the saved model.
        verbose (bool): If True, prints progress messages.
    """
    if verbose:
        print(f"--- Training: Subj(s) {subjects}, Channel {channel}, Event {event} ---")
        print(f"--- Using training series: {train_series} ---")
    
    # Define paths
    if model_filename:
        model_path = os.path.join(output_dir, model_filename)
    else:
        model_path = os.path.join(output_dir, f"subj{subjects[0]}_{event.lower()}_{channel}_model.joblib")

    # Load data
    X_train_all_subjects = []
    y_train_all_subjects = []
    channels_to_load = ALL_CHANNELS if channel == 'all' else [channel]
    for subject in subjects:
        X_train_sub, y_train_sub = load_data(subject, train_series, event, channels_to_load, verbose=verbose)
        X_train_all_subjects.append(X_train_sub)
        y_train_all_subjects.append(y_train_sub)
    X_train = pd.concat(X_train_all_subjects)
    y_train = pd.concat(y_train_all_subjects)
    
    # --- Dynamic Pipeline Construction ---
    steps = []
    fit_params = {}
    
    if feature_extractor_str:
        extractor_names = [name.strip() for name in feature_extractor_str.split(',')]
        for name in extractor_names:
            if name in EXTRACTOR_MAP:
                if verbose:
                    print(f"--- Adding step: {name} ---")
                
                # Use lowercase name for scikit-learn pipeline step naming
                step_name = name.lower()
                
                # Handle specific parameters
                if name == 'FilterBank' and filterbank_custom_freqs:
                    steps.append((step_name, EXTRACTOR_MAP[name](filters=filterbank_custom_freqs)))
                else:
                    steps.append((step_name, EXTRACTOR_MAP[name]()))
                
                # Special handling for CSP fit_params
                if name == 'CSP':
                    fit_params[f'{step_name}__y'] = y_train
            else:
                raise ValueError(f"Unknown feature extractor '{name}' specified.")

    steps.append(('scaler', StandardScaler()))
    steps.append(('classifier', LogisticRegression(class_weight='balanced', solver='liblinear', random_state=42)))
    
    pipeline = Pipeline(steps)
    
    # Train the model
    pipeline.fit(X_train, y_train, **fit_params)
    
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(pipeline, model_path)
    if verbose:
        print(f"--- Model saved to: {model_path} ---")


def print_usage():
    """Prints the usage instructions for the script."""
    print("\n--- EEG Model Training Script ---")
    print("\nThis script trains a model for a single subject, channel, and event.")
    print("\nUsage: python train.py <subject_id> <channel_name> <event_name> [--output_dir <path>] [--train-series <series>] [--feature-extractor <name>]")
    print("\nArguments:")
    print("  <subject_id>        : Subject ID (e.g., 1, 2, ... 12)")
    print("  <channel_name>      : Name of the EEG channel (case-insensitive, e.g., 'Fp1', 'c3')")
    print("  <event_name>        : Name of the event (case-insensitive, e.g., 'HandStart', 'liftoff')")
    print("  --output_dir        : (Optional) Base directory to save the model. Defaults to './out'.")
    print("                        If default is used, a structured path will be created automatically.")
    print("  --train-series      : (Optional) Series to use for training (e.g., '1-6', '1,2,3'). Defaults to '1-6'.")
    print("  --feature-extractor : (Optional) Feature extractor to use. Currently only 'filterbank' is supported.")
    print("\nExample (standalone with features):")
    print("  python train.py 1 Fp1 HandStart --feature-extractor filterbank\n")


def main():
    """Main function to handle command-line execution."""
    parser = argparse.ArgumentParser(description="Train an EEG model for a specific target.")
    parser.add_argument('subject', help="Subject ID (e.g., '1').")
    parser.add_argument('channel', help="Channel name (e.g., 'Fp1').")
    parser.add_argument('event', help="Event name (e.g., 'HandStart').")
    parser.add_argument('--output_dir', default='./out', help="Base directory to save the model. Defaults to './out'.")
    parser.add_argument('--train-series', default='1-6', help="Series to use for training (e.g., '1-6' or '1,2,3').")
    parser.add_argument('--feature-extractor', default=None, choices=['filterbank', None], help="Specify the feature extractor to use (e.g., 'filterbank').")
    
    args = parser.parse_args()

    # --- Normalize and Validate Inputs (Case-Insensitive) ---
    channel_name = next((c for c in ALL_CHANNELS if c.lower() == args.channel.lower()), None)
    if not channel_name:
        print(f"Error: Invalid channel name '{args.channel}'.")
        sys.exit(1)

    event_name = next((e for e in ALL_EVENTS if e.lower() == args.event.lower()), None)
    if not event_name:
        print(f"Error: Invalid event name '{args.event}'.")
        sys.exit(1)

    # --- Directory Logic ---
    output_dir = args.output_dir
    if output_dir == './out':
        run_name = f"subj-{args.subject}_chan-{channel_name}_evt-{event_name}"
        if args.feature_extractor:
            run_name += f"_{args.feature_extractor}" # Add feature name to folder
        output_dir = os.path.join(output_dir, run_name, 'model')
        print(f"Default directory used. Saving model to: {output_dir}")

    os.makedirs(output_dir, exist_ok=True)
    
    # --- Data and Training ---
    train_series_list = parse_series(args.train_series)
    
    print(f"(Input corrected to: Subject {args.subject}, Channel {channel_name}, Event {event_name})")
    train_model(args.subject, channel_name, event_name, output_dir, train_series_list, feature_extractor=args.feature_extractor)

if __name__ == '__main__':
    main()
