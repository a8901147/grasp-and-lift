import pandas as pd
import numpy as np
import joblib
import os
import sys
from sklearn.metrics import roc_auc_score
from tqdm import tqdm
from feature_engineering import FilterBank, CSPFeatureExtractor

# --- Configuration: Data Source ---
# Dynamically find the project root and build the path to the data directory
# This makes the script runnable from any location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'train')

VALID_SERIES = range(7, 9)
# ---

# --- Constants ---
ALL_CHANNELS = [
    'Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6', 
    'T7', 'C3', 'Cz', 'C4', 'T8', 'TP9', 'CP5', 'CP1', 'CP2', 'CP6', 'TP10', 
    'P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10'
]
ALL_EVENTS = ['HandStart', 'FirstDigitTouch', 'BothStartLoadPhase', 'LiftOff', 'Replace', 'BothReleased']

def load_data_for_series(subject, series_list, event, channel, verbose=True):

    """Loads and combines data for a specific subject and list of series."""

    all_dfs = []

    # Use tqdm for a progress bar, but disable it in non-verbose mode

    desc = f"Loading valid data for Subj {subject} ({event}/{channel})"

    for series in tqdm(series_list, desc=desc, leave=False, disable=not verbose):

        data_file = f"{DATA_DIR}/subj{subject}_series{series}_data.csv"

        event_file = f"{DATA_DIR}/subj{subject}_series{series}_events.csv"

        df_data = pd.read_csv(data_file, index_col='id')

        df_events = pd.read_csv(event_file, index_col='id')

        df_merged = df_data.join(df_events)

        all_dfs.append(df_merged)

    if not all_dfs:

        raise FileNotFoundError(f"No data found for subject {subject} in series {list(series_list)} at {DATA_DIR}")

    return pd.concat(all_dfs)



def evaluate_model(subjects, channel, event, model_path, verbose=True):

    """

    Loads a pre-trained model and evaluates it, returning the AUC score.

    Can handle single or multiple subjects for evaluation.

    

    Args:

        subjects (list): A list of subject IDs for loading validation data.

        channel (str): The EEG channel(s) to use. 'all' for all channels.

        event (str): The target event for prediction.

        model_path (str): The full path to the trained model .joblib file.

        verbose (bool): If True, prints progress messages.

        

    Returns:

        float: The calculated AUC score.

    """

    if verbose:

        print(f"--- Evaluating: Subj(s) {subjects}, Channel {channel}, Event {event} ---")



    # 1. Load Model

    if not os.path.exists(model_path):

        raise FileNotFoundError(f"Model not found at {model_path}. Please provide a valid path.")

    model_pipeline = joblib.load(model_path)



    # 2. Load Validation Data for all specified subjects

    all_valid_dfs = []

    channels_to_load = ALL_CHANNELS if channel == 'all' else [channel]

    channel_desc = 'all' if channel == 'all' else channel # For progress bar



    for subject_id in subjects:

        df_valid_sub = load_data_for_series(subject_id, VALID_SERIES, event, channel_desc, verbose=verbose)

        all_valid_dfs.append(df_valid_sub)

    

    df_valid = pd.concat(all_valid_dfs)



    # 3. Prepare features (X) and target (y)

    for col in channels_to_load + [event]:

        if col not in df_valid.columns:

            raise ValueError(f"Column '{col}' not found in the validation data.")

            

    X_valid = df_valid[channels_to_load]

    y_valid = df_valid[event]



    # If CSP is part of the pipeline, it needs event_data for transform

    # We assume the pipeline is already fitted.

    if 'csp' in model_pipeline.named_steps and isinstance(model_pipeline.named_steps['csp'], CSPFeatureExtractor):

        # For transform, CSPFeatureExtractor expects y as event_data

        valid_probs = model_pipeline.predict_proba(X_valid, y=y_valid)[:, 1]

    else:

        valid_probs = model_pipeline.predict_proba(X_valid)[:, 1]

    auc_score = roc_auc_score(y_valid, valid_probs)

    

    if verbose:

        print(f"--- AUC for Subj(s) {subjects}, Channel {channel}, Event {event}: {auc_score:.4f} ---")

    return auc_score
import argparse

def print_usage():
    """Prints the usage instructions for the script."""
    print("\n--- EEG Model Evaluation Script ---")
    print("\nThis script evaluates a pre-trained model by locating it based on parameters.")
    print("\nUsage: python evaluate.py <subject_id> <channel_name> <event_name> [--model_dir <path>] [--feature-extractor <name>]")
    print("\nArguments:")
    print("  <subject_id>        : Subject ID for loading validation data (e.g., 1, 2).")
    print("  <channel_name>      : Name of the EEG channel used for the model (e.g., 'Fp1').")
    print("  <event_name>        : Name of the event the model predicts (e.g., 'HandStart').")
    print("  --model_dir         : (Optional) Base directory where the model is stored. Defaults to './out'.")
    print("                        If default is used, it will look inside the auto-generated structure.")
    print("  --feature-extractor : (Optional) Feature extractor used for the model. Affects model path.")
    print("\nExample (standalone with features):")
    print("  python evaluate.py 1 Fp1 HandStart --feature-extractor filterbank\n")

def main():
    """Main function to handle command-line execution."""
    parser = argparse.ArgumentParser(description="Evaluate a pre-trained EEG model.")
    parser.add_argument('subject', help="Subject ID (e.g., '1').")
    parser.add_argument('channel', help="Channel name (e.g., 'Fp1').")
    parser.add_argument('event', help="Event name (e.g., 'HandStart').")
    parser.add_argument('--model_dir', default='./out', help="Base directory to load the model from. Defaults to './out'.")
    parser.add_argument('--feature-extractor', default=None, choices=['filterbank', None], help="Specify the feature extractor used for the model.")
    
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
        
    # --- Path Construction Logic ---
    model_dir = args.model_dir
    if model_dir == './out':
        run_name = f"subj-{args.subject}_chan-{channel_name}_evt-{event_name}"
        if args.feature_extractor:
            run_name += f"_{args.feature_extractor}"
        model_dir = os.path.join(model_dir, run_name, 'model')
        print(f"Default directory used. Loading model from: {model_dir}")

    model_path = os.path.join(model_dir, f"subj{args.subject}_{event_name.lower()}_{channel_name}_model.joblib")
    
    print(f"(Input corrected to: Subject {args.subject}, Channel {channel_name}, Event {event_name})")
    evaluate_model([args.subject], channel_name, event_name, model_path)

if __name__ == '__main__':
    main()