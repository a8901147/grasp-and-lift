
import os
import sys
import argparse
from tqdm import tqdm

# Import the core logic from our refactored scripts
from train_eegnet import train_eegnet_model, ALL_CHANNELS, ALL_EVENTS, parse_series
from evaluate_eegnet import predict_eegnet

# --- Constants ---
ALL_SUBJECTS = list(range(1, 13))

def main():
    parser = argparse.ArgumentParser(description="EEGNet Analysis Engine: Train and evaluate models.")
    parser.add_argument('subject', help="Subject ID (e.g., 1) or 'all'.")
    parser.add_argument('channels', help="Channels to use: 'all' or a single channel name (e.g., 'Fp1').")
    parser.add_argument('event', help="Event name (e.g., 'HandStart').")
    
    # Directories are now passed from the shell script, similar to baseline
    parser.add_argument('--model_dir_base', required=True, help="Base directory to save model files.")
    parser.add_argument('--output_dir_base', required=True, help="Base directory to save prediction results.")

    # Hyperparameters
    parser.add_argument('--train-series', default='1-6', help="Series for training.")
    parser.add_argument('--val-series', default='7,8', help="Series for validation.")
    parser.add_argument('--window-size', type=int, default=500, help="Input window size (samples).")
    parser.add_argument('--batch-size', type=int, default=64, help="Batch size for training.")
    parser.add_argument('--epochs', type=int, default=10, help="Number of training epochs.")
    parser.add_argument('--lr', type=float, default=0.001, help="Learning rate.")
    
    args = parser.parse_args()

    # --- 1. Validate and Parse Arguments ---
    event_name = next((e for e in ALL_EVENTS if e.lower() == args.event.lower()), None)
    if not event_name:
        print(f"Error: Invalid event name '{args.event}'.")
        sys.exit(1)

    if args.channels.lower() == 'all':
        channels_to_use = ALL_CHANNELS
        chan_str = 'all'
    else:
        channel_name = next((c for c in ALL_CHANNELS if c.lower() == args.channels.lower()), None)
        if not channel_name:
            print(f"Error: Invalid channel name '{args.channels}'.")
            sys.exit(1)
        channels_to_use = [channel_name]
        chan_str = channel_name

    if args.subject.lower() == 'all':
        subjects_to_process = ALL_SUBJECTS
    else:
        try:
            subject_id = int(args.subject)
            if subject_id not in ALL_SUBJECTS:
                raise ValueError
            subjects_to_process = [subject_id]
        except ValueError:
            print(f"Error: Invalid subject ID '{args.subject}'. Must be an integer from 1-12 or 'all'.")
            sys.exit(1)

    train_series_list = parse_series(args.train_series)
    val_series_list = parse_series(args.val_series)

    # --- 2. Main Processing Loop ---
    print(f"--- Starting EEGNet Analysis ---")
    print(f"Subjects: {args.subject} | Channels: {args.channels} | Event: {event_name}")
    
    pbar = tqdm(subjects_to_process, desc="Processing Subjects")
    for subj_id in pbar:
        pbar.set_postfix_str(f"Subj {subj_id}")
        
        # Define subject-specific paths
        run_name = f"subj-{subj_id}_chan-{chan_str}_evt-{event_name.lower()}"
        model_output_dir = os.path.join(args.model_dir_base, run_name, "model")
        results_output_dir = os.path.join(args.output_dir_base, run_name, "results")
        os.makedirs(model_output_dir, exist_ok=True)
        os.makedirs(results_output_dir, exist_ok=True)

        # --- 2a. Training ---
        print(f"\nTraining model for Subject {subj_id}...")
        train_eegnet_model(
            subject=subj_id,
            event=event_name,
            channels_to_use=channels_to_use,
            output_dir=model_output_dir,
            train_series=train_series_list,
            val_series=val_series_list,
            window_size=args.window_size,
            batch_size=args.batch_size,
            epochs=args.epochs,
            lr=args.lr,
            verbose=True 
        )

        # --- 2b. Evaluation ---
        print(f"\nEvaluating model for Subject {subj_id}...")
        predict_eegnet(
            subject=subj_id,
            event=event_name,
            channels_to_use=channels_to_use,
            model_dir=model_output_dir,
            output_dir=results_output_dir,
            window_size=args.window_size,
            verbose=True
        )
        print("-" * 50)

    print("--- EEGNet Analysis Finished ---")

if __name__ == '__main__':
    main()
