
import os
import sys
import argparse
import pandas as pd
import numpy as np
import joblib
from tqdm import tqdm

import torch

# Adjust path to import from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.eegnet import EEGNet
from train_eegnet import ALL_CHANNELS, ALL_EVENTS # Import constants

# --- Constants ---
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/test'))

def predict_eegnet(
    subject, event, channels_to_use, model_dir, output_dir,
    window_size=500, batch_size=256,
    verbose=True
):
    if verbose:
        print(f"--- Evaluating EEGNet: Subj {subject}, Event {event}, Channels: {'/'.join(channels_to_use)} ---")

    # 1. Load Model and Scaler
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if verbose: print(f"Using device: {device}")

    model_path = os.path.join(model_dir, "model.pth")
    scaler_path = os.path.join(model_dir, "scaler.joblib")

    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Model or scaler not found in {model_dir}")

    model = EEGNet(
        n_channels=len(channels_to_use),
        n_classes=1,
        input_size_s=window_size
    ).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    scaler = joblib.load(scaler_path)
    if verbose: print("Model and scaler loaded successfully.")

    # 2. Process each test series
    all_predictions = []
    for series_id in [9, 10]:
        if verbose: print(f"Processing Series {series_id}...")
        
        data_file = f"{DATA_DIR}/subj{subject}_series{series_id}_data.csv"
        df_data = pd.read_csv(data_file)
        
        scaled_data = scaler.transform(df_data[channels_to_use])
        
        series_preds = [0.0] * (window_size - 1)

        def window_batch_generator():
            window_batch = []
            for i in range(window_size - 1, len(scaled_data)):
                window = scaled_data[i - window_size + 1 : i + 1]
                window_batch.append(window.T)
                if len(window_batch) == batch_size:
                    yield np.array(window_batch)
                    window_batch = []
            if window_batch:
                yield np.array(window_batch)

        with torch.no_grad():
            total_batches = int(np.ceil((len(scaled_data) - window_size + 1) / batch_size))
            pbar = tqdm(window_batch_generator(), total=total_batches, desc=f"Predicting Series {series_id}", leave=False)
            for batch_windows in pbar:
                inputs = torch.from_numpy(batch_windows).float().to(device)
                outputs = model(inputs)
                series_preds.extend(outputs.cpu().numpy().flatten().tolist())

        pred_df = pd.DataFrame({'id': df_data['id'], event: series_preds})
        all_predictions.append(pred_df)

    # 3. Combine and Save Results
    final_df = pd.concat(all_predictions).set_index('id')
    os.makedirs(output_dir, exist_ok=True)
    
    submission_file = os.path.join(output_dir, 'submission.csv')
    if os.path.exists(submission_file):
        if verbose: print(f"Updating existing submission file: {submission_file}")
        existing_df = pd.read_csv(submission_file, index_col='id')
        existing_df[event] = final_df[event]
        existing_df.to_csv(submission_file)
    else:
        if verbose: print(f"Creating new submission file: {submission_file}")
        for other_event in ALL_EVENTS:
            if other_event != event:
                final_df[other_event] = 0
        final_df = final_df[ALL_EVENTS]
        final_df.to_csv(submission_file)

    if verbose: print(f"Predictions for {event} saved.")
    return submission_file


def main():
    parser = argparse.ArgumentParser(description="Evaluate an EEGNet model (can be run standalone).")
    parser.add_argument('subject', type=int, help="Subject ID (e.g., 1).")
    parser.add_argument('event', help="Event name (e.g., 'HandStart').")
    parser.add_argument('--channels', default='all', help="Channels used for training: 'all' or a single channel name.")
    parser.add_argument('--model_dir_base', required=True, help="Base directory where the model and scaler are saved.")
    parser.add_argument('--output_dir_base', required=True, help="Base directory to save the submission file.")
    parser.add_argument('--window-size', type=int, default=500, help="Size of the input window for the model (samples).")
    
    args = parser.parse_args()

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

    run_name = f"subj-{args.subject}_chan-{chan_str}_evt-{event_name.lower()}"
    model_dir = os.path.join(args.model_dir_base, run_name, "model")
    output_dir = os.path.join(args.output_dir_base, run_name, "results")
    
    print(f"Loading model from: {model_dir}")
    print(f"Saving results to: {output_dir}")

    predict_eegnet(
        subject=args.subject,
        event=event_name,
        channels_to_use=channels_to_use,
        model_dir=model_dir,
        output_dir=output_dir,
        window_size=args.window_size
    )

if __name__ == '__main__':
    main()
