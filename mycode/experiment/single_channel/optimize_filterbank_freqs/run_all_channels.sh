#!/bin/bash

# This script loops through all EEG channels and runs the optimization experiment for each one.

# --- Configuration ---
SUBJECT_ID=1
EVENT_NAME="handstart"
CHANNELS=(
    "Fp1" "Fp2" "F7" "F3" "Fz" "F4" "F8" "FC5" "FC1" "FC2" "FC6"
    "P7" "P3" "Pz" "P4" "P8" "C3" "Cz" "C4" "CP5" "CP1" "CP2" "CP6"
    "T7" "T8" "TP9" "TP10"
    "O1" "Oz" "O2" "PO9" "PO10"
)
SCRIPT_TO_CALL="./run_exp_optimize_filterbank.sh"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# --- Script Body ---
echo "Starting batch experiment run for all channels..."
echo "  - Subject: $SUBJECT_ID"
echo "  - Event:   $EVENT_NAME"
echo "================================================="

for channel in "${CHANNELS[@]}"; do
    echo "Running experiment for channel: $channel"
    # Navigate to the script's directory to run it
    (cd "$SCRIPT_DIR" && bash "$SCRIPT_TO_CALL" "$SUBJECT_ID" "$channel" "$EVENT_NAME")

    # Check the exit code of the last command
    if [ $? -ne 0 ]; then
        echo "Error: Experiment for channel $channel failed. Aborting."
        exit 1
    fi
    echo "-------------------------------------------------"
done

echo "================================================="
echo "All channel experiments completed successfully."
echo "================================================="

exit 0
