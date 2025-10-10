
import os
import sys
import argparse
import pandas as pd
import numpy as np
import joblib
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

from sklearn.preprocessing import StandardScaler

# Adjust path to import from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.eegnet import EEGNet

# --- Constants ---
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/train'))
ALL_CHANNELS = [
    'Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6', 
    'T7', 'C3', 'Cz', 'C4', 'T8', 'TP9', 'CP5', 'CP1', 'CP2', 'CP6', 'TP10', 
    'P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10'
]
ALL_EVENTS = ['HandStart', 'FirstDigitTouch', 'BothStartLoadPhase', 'LiftOff', 'Replace', 'BothReleased']
DEFAULT_TRAIN_SERIES = list(range(1, 9)) # Use Series 1-8 for training/validation split

# --- Data Loading Functions (can be shared) ---
def parse_series(series_str):
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

def load_data_for_series(subject, series_list, data_dir, verbose=True):
    all_dfs = []
    desc = f"Loading data for Subj {subject}"
    for series in tqdm(series_list, desc=desc, disable=not verbose, leave=False):
        data_file = f"{data_dir}/subj{subject}_series{series}_data.csv"
        event_file = f"{data_dir}/subj{subject}_series{series}_events.csv"
        df_data = pd.read_csv(data_file, index_col='id')
        df_events = pd.read_csv(event_file, index_col='id')
        df_merged = df_data.join(df_events)
        all_dfs.append(df_merged)
    if not all_dfs:
        raise FileNotFoundError(f"No data found for subject {subject} in series {list(series_list)} at {data_dir}")
    return pd.concat(all_dfs)

# --- PyTorch Dataset ---
class EEGWindowDataset(Dataset):
    def __init__(self, X, y, window_size, channels):
        self.X = X[channels].values
        self.y = y.values
        self.window_size = window_size
        self.channels = channels
        self.valid_indices = range(window_size - 1, len(self.X))

    def __len__(self):
        return len(self.valid_indices)

    def __getitem__(self, idx):
        actual_idx = self.valid_indices[idx]
        start_idx = actual_idx - self.window_size + 1
        window_x = self.X[start_idx : actual_idx + 1]
        label = self.y[actual_idx]
        tensor_x = torch.from_numpy(window_x.T).float()
        tensor_y = torch.tensor([label], dtype=torch.float32)
        return tensor_x, tensor_y

# --- Main Training Logic ---
def train_eegnet_model(
    subject, event, channels_to_use, output_dir, train_series, val_series,
    window_size=500, batch_size=64, epochs=10, lr=0.001,
    verbose=True
):
    if verbose:
        print(f"--- Training EEGNet: Subj {subject}, Event {event}, Channels: {'/'.join(channels_to_use)} ---")
        print(f"--- Using train series: {train_series}, validation series: {val_series} ---")

    # 1. Load Data
    df_train = load_data_for_series(subject, train_series, DATA_DIR, verbose)
    df_val = load_data_for_series(subject, val_series, DATA_DIR, verbose)

    X_train_df = df_train[channels_to_use]
    y_train_df = df_train[event]
    X_val_df = df_val[channels_to_use]
    y_val_df = df_val[event]

    # 2. Fit Scaler on Training Data
    if verbose: print(f"Fitting StandardScaler on {len(channels_to_use)} selected channels...")
    scaler = StandardScaler()
    scaler.fit(X_train_df)
    
    scaler_path = os.path.join(output_dir, "scaler.joblib")
    os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
    joblib.dump(scaler, scaler_path)
    if verbose: print(f"Scaler saved to {scaler_path}")

    X_train_scaled = pd.DataFrame(scaler.transform(X_train_df), columns=channels_to_use, index=X_train_df.index)
    X_val_scaled = pd.DataFrame(scaler.transform(X_val_df), columns=channels_to_use, index=X_val_df.index)

    # 3. Create Datasets and DataLoaders
    if verbose: print("Creating PyTorch Datasets and DataLoaders...")
    train_dataset = EEGWindowDataset(X_train_scaled, y_train_df, window_size, channels_to_use)
    val_dataset = EEGWindowDataset(X_val_scaled, y_val_df, window_size, channels_to_use)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    # 4. Initialize Model, Loss, Optimizer
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if verbose: print(f"Using device: {device}")

    model = EEGNet(
        n_channels=len(channels_to_use),
        n_classes=1,
        input_size_s=window_size
    ).to(device)

    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # 5. Training Loop
    if verbose: print("Starting training loop...")
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        pbar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs} [Training]", leave=False)
        for i, (inputs, labels) in enumerate(pbar):
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            pbar.set_postfix({'loss': running_loss / (i + 1)})

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            pbar_val = tqdm(val_loader, desc=f"Epoch {epoch+1}/{epochs} [Validation]", leave=False)
            for i, (inputs, labels) in enumerate(pbar_val):
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                pbar_val.set_postfix({'val_loss': val_loss / (i + 1)})

    # 6. Save the final model
    model_path = os.path.join(output_dir, "model.pth")
    torch.save(model.state_dict(), model_path)
    if verbose: print(f"--- Model saved to: {model_path} ---")
    return model_path, scaler_path


def main():
    parser = argparse.ArgumentParser(description="Train an EEGNet model (can be run standalone).")
    parser.add_argument('subject', type=int, help="Subject ID (e.g., 1).")
    parser.add_argument('event', help="Event name (e.g., 'HandStart').")
    parser.add_argument('--channels', default='all', help="Channels to use: 'all' or a single channel name (e.g., 'Fp1').")
    parser.add_argument('--output_dir_base', default='./out/eegnet_raw_signal', help="Base directory to save the model and scaler.")
    parser.add_argument('--train-series', default='1-6', help="Series for training.")
    parser.add_argument('--val-series', default='7,8', help="Series for validation.")
    parser.add_argument('--window-size', type=int, default=500, help="Size of the input window for the model (samples).")
    parser.add_argument('--batch-size', type=int, default=64, help="Batch size for training.")
    parser.add_argument('--epochs', type=int, default=10, help="Number of training epochs.")
    parser.add_argument('--lr', type=float, default=0.001, help="Learning rate.")
    
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
    output_path = os.path.join(args.output_dir_base, run_name, "model")
    os.makedirs(output_path, exist_ok=True)
    print(f"Output will be saved to: {output_path}")

    train_series_list = parse_series(args.train_series)
    val_series_list = parse_series(args.val_series)

    train_eegnet_model(
        subject=args.subject,
        event=event_name,
        channels_to_use=channels_to_use,
        output_dir=output_path,
        train_series=train_series_list,
        val_series=val_series_list,
        window_size=args.window_size,
        batch_size=args.batch_size,
        epochs=args.epochs,
        lr=args.lr
    )

if __name__ == '__main__':
    main()
