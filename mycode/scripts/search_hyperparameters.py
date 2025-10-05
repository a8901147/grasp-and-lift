
import os
import sys
import numpy as np
from tqdm import tqdm
import warnings
from sklearn.exceptions import ConvergenceWarning
import argparse
import pandas as pd

# --- Add project root to sys.path ---
# This allows us to import modules from the 'scripts' directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'scripts'))
# -----------------------------------------

from skopt import gp_minimize
from skopt.space import Real
from skopt.utils import use_named_args

from train import train_model
from evaluate import evaluate_model
from feature_engineering import FilterBank

# --- Suppress ConvergenceWarning from sklearn ---
warnings.filterwarnings("ignore", category=ConvergenceWarning)
# -------------------------------------------------

# --- Argument Parsing Helpers (from run_analysis.py) ---
def parse_subject_ids(subject_str):
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
            sys.exit(f"Error: Invalid subject format '{part}'.")
    return subjects

def get_channels(channel_arg):
    all_channels = ['Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6', 'T7', 'C3', 'Cz', 'C4', 'T8', 'TP9', 'CP5', 'CP1', 'CP2', 'CP6', 'TP10', 'P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10']
    if channel_arg.lower() == 'all':
        return all_channels
    else:
        # Allow comma-separated list of channels
        selected_channels = [c.strip() for c in channel_arg.split(',')]
        # Validate channels
        invalid_channels = [c for c in selected_channels if c not in all_channels]
        if invalid_channels:
            sys.exit(f"Error: Invalid channel(s) specified: {', '.join(invalid_channels)}")
        return selected_channels


ALL_EVENTS = ['HandStart', 'FirstDigitTouch', 'BothStartLoadPhase', 'LiftOff', 'Replace', 'BothReleased']
# -------------------------------------------------

# --- 1. Define the Search Space for Bayesian Optimization ---
SEARCH_SPACE = [
    Real(0.1, 1.0, name='freq_1'),
    Real(1.0, 3.0, name='freq_2'),
    Real(3.0, 5.0, name='freq_3'),
    Real(5.0, 7.0, name='freq_4'),
    Real(7.0, 10.0, name='freq_5'),
    Real(10.0, 14.0, name='freq_6'),
    Real(14.0, 20.0, name='freq_7'),
    Real(20.0, 28.0, name='freq_8'),
    Real(28.0, 38.0, name='freq_9'),
    Real(38.0, 45.0, name='freq_10')
]

def main():
    parser = argparse.ArgumentParser(description="Run Bayesian Optimization for Filter Bank frequencies.")
    parser.add_argument('subject', help="Subject ID(s) (e.g., '1', '1,2', 'all').")
    parser.add_argument('channel', help="Channel name(s) (e.g., 'Fp1', 'all', 'C3,C4').")
    parser.add_argument('event', help="Event name (e.g., 'HandStart').")
    parser.add_argument('--n_calls', type=int, default=25, help="Number of optimization iterations.")
    parser.add_argument('--output_dir', type=str, default='.', help='Directory to save the output results.')
    parser.add_argument('--output-file', type=str, default='optimization_results.txt', help='Path to save the output results file.')

    args = parser.parse_args()

    subjects = parse_subject_ids(args.subject)
    channels = get_channels(args.channel)
    event = next((e for e in ALL_EVENTS if e.lower() == args.event.lower()), None)
    if not event:
        sys.exit(f"Error: Invalid event name '{args.event}'.")

    MODEL_DIR = os.path.join(args.output_dir, 'temp_models')
    os.makedirs(MODEL_DIR, exist_ok=True)

    # --- 2. Define the Objective Function (as an inner function) ---
    @use_named_args(SEARCH_SPACE)
    def objective(**params):
        freq_list = sorted(params.values())
        current_freqs = [[f] for f in freq_list]
        
        print(f"\nTesting Frequencies: {[round(f, 2) for f in freq_list]}")
        all_auc_scores = []

        for subj in subjects:
            for chan in tqdm(channels, desc=f"  - Evaluating Subject {subj}", leave=False):
                model_path = os.path.join(MODEL_DIR, f"temp_model_{subj}_{chan}.joblib")
                train_model(
                    subj, chan, event, MODEL_DIR,
                    feature_extractor='filterbank',
                    filterbank_custom_freqs=current_freqs,
                    model_filename=os.path.basename(model_path)
                )
                auc_score = evaluate_model(subj, chan, event, model_path)
                all_auc_scores.append(auc_score)

        average_auc = np.mean(all_auc_scores)
        print(f"  - Average AUC for this iteration: {average_auc:.6f}")
        return -average_auc

    # --- 3. Run the Bayesian Optimization ---
    print("======================================================================")
    print(" Starting Bayesian Optimization for Filter Bank Frequencies")
    print("======================================================================")
    print(f"Subjects: {args.subject} -> {subjects}")
    print(f"Channels: {args.channel} -> {len(channels)} channels")
    print(f"Event: {event}")
    print(f"Number of Iterations: {args.n_calls}")
    print("----------------------------------------------------------------------")

    result = gp_minimize(
        func=objective,
        dimensions=SEARCH_SPACE,
        n_calls=args.n_calls,
        random_state=42,
        n_jobs=-1
    )

    # --- 4. Display and Save the Results ---
    best_frequencies = result.x
    best_score = -result.fun
    
    results_str = (
        "\n======================================================================\n"
        " Optimization Finished\n"
        "======================================================================\n"
        f"Subjects: {args.subject}\n"
        f"Channels: {args.channel}\n"
        f"Event: {event}\n"
        f"Iterations: {args.n_calls}\n"
        "----------------------------------------------------------------------\n"
        f"Best Average AUC Score Found: {best_score:.6f}\n"
        "Best Frequency Combination (Hz):\n"
        f"{ [round(f, 2) for f in best_frequencies] }\n"
        "======================================================================\n"
    )
    print(results_str)
    
    # Save results to a file in the specified output directory
    results_file_path = args.output_file
    with open(results_file_path, 'w') as f:
        f.write(results_str)
    print(f"Results saved to {results_file_path}")

    # Clean up temporary models
    for f in os.listdir(MODEL_DIR):
        os.remove(os.path.join(MODEL_DIR, f))
    os.rmdir(MODEL_DIR)
    print("Temporary models cleaned up.")

if __name__ == "__main__":
    main()
