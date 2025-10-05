
import pandas as pd
import numpy as np
import joblib
import os
import sys
from sklearn.metrics import roc_auc_score
from tqdm import tqdm

# --- Configuration: Data Source ---
VALID_SERIES = range(7, 9)
DATA_DIR = '/Users/jeremmy/Desktop/grasp-and-lift/data/train'
# ---

# --- Constants ---
ALL_CHANNELS = [
    'Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6', 
    'T7', 'C3', 'Cz', 'C4', 'T8', 'TP9', 'CP5', 'CP1', 'CP2', 'CP6', 'TP10', 
    'P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10'
]
ALL_EVENTS = ['HandStart', 'FirstDigitTouch', 'BothStartLoadPhase', 'LiftOff', 'Replace', 'BothReleased']

def load_data_for_series(subject, series_list):
    """Loads and combines data for a specific subject and list of series."""
    all_dfs = []
    # Use tqdm for a progress bar, but keep it minimal for module use
    for series in tqdm(series_list, desc=f"Loading validation data for Subj {subject}", leave=False):
        data_file = f"{DATA_DIR}/subj{subject}_series{series}_data.csv"
        event_file = f"{DATA_DIR}/subj{subject}_series{series}_events.csv"
        df_data = pd.read_csv(data_file, index_col='id')
        df_events = pd.read_csv(event_file, index_col='id')
        df_merged = df_data.join(df_events)
        all_dfs.append(df_merged)
    if not all_dfs:
        raise FileNotFoundError(f"No data found for subject {subject} in series {list(series_list)} at {DATA_DIR}")
    return pd.concat(all_dfs)

def evaluate_model(subject_id, channel, event, model_path):
    """
    Loads a pre-trained model and evaluates it, returning the AUC score.
    
    Args:
        subject_id (str): The identifier for the subject (for loading validation data).
        channel (str): The EEG channel to use as a feature.
        event (str): The target event for prediction.
        model_path (str): The full path to the trained model .joblib file.
        
    Returns:
        float: The calculated AUC score.
    """
    print(f"--- Evaluating: Subj {subject_id}, Channel {channel}, Event {event} ---")

    # 1. Load Model
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Please provide a valid path.")
    model_pipeline = joblib.load(model_path)

    # 2. Load Validation Data
    df_valid = load_data_for_series(subject_id, VALID_SERIES)

    # 3. Prepare features (X) and target (y)
    if channel not in df_valid.columns:
        raise ValueError(f"Channel '{channel}' not found in the validation data.")
    if event not in df_valid.columns:
        raise ValueError(f"Event '{event}' not found in the validation data.")
        
    X_valid = df_valid[[channel]]
    y_valid = df_valid[event]

    # 4. Evaluate Model and return AUC score
    valid_probs = model_pipeline.predict_proba(X_valid)[:, 1]
    auc_score = roc_auc_score(y_valid, valid_probs)
    
    print(f"--- AUC: {auc_score:.4f} ---")
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
    evaluate_model(args.subject, channel_name, event_name, model_path)

if __name__ == '__main__':
    main()
