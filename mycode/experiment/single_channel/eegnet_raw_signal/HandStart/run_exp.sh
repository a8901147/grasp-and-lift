#!/bin/bash

##############################################################################
# Experiment: EEGNet with Raw Signal
#
# This script runs the EEGNet model on raw EEG signals.
# It serves as a single entry point for training and evaluating the model.
##############################################################################

# --- Usage ---
#
# ./run_exp.sh [subject] [channels] [event]
#
# Arguments:
#   [subject]:  Subject ID (e.g., 1, 2, ... 12) or 'all'. Defaults to 1.
#   [channels]: Channels to use ('all' or a specific name like 'C3'). Defaults to 'all'.
#   [event]:    Event name (e.g., HandStart, LiftOff). Defaults to 'HandStart'.
#
# Examples:
#   # Run for Subject 1, all channels, HandStart event
#   ./run_exp.sh 1 all HandStart
#
#   # Run for Subject 2, channel Fp1, LiftOff event
#   ./run_exp.sh 2 Fp1 LiftOff
#
#   # Run for all subjects, all channels, HandStart event
#   ./run_exp.sh all all HandStart
#
##############################################################################

# --- Script Body ---

# 1. Define Experiment Parameters from command line arguments
SUBJECT_TARGET="${1:-1}"
CHANNELS_TARGET="${2:-all}"
EVENT_TARGET="${3:-HandStart}"

# 2. Get Script Directory and Define Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
# The experiment name is derived from the parent directory name
EXP_NAME=$(basename "$(dirname "$SCRIPT_DIR")") 
LOG_FILE="${SCRIPT_DIR}/run_exp.log"
FRAMEWORK_DIR="${SCRIPT_DIR}/../../../scripts"
# Base directories for model and results, the python script will create subfolders
MODEL_DIR_BASE="${SCRIPT_DIR}/../../$EXP_NAME"
OUTPUT_DIR_BASE="${SCRIPT_DIR}/../../$EXP_NAME"

# Create the experiment directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# 3. Execute the Python Engine and Log Output
# Clear previous log
> "$LOG_FILE"

echo "======================================================================" | tee -a "$LOG_FILE"
echo "Starting Experiment: $EXP_NAME" | tee -a "$LOG_FILE"
echo "  - Subject(s): $SUBJECT_TARGET" | tee -a "$LOG_FILE"
echo "  - Channel(s): $CHANNELS_TARGET" | tee -a "$LOG_FILE"
echo "  - Event:      $EVENT_TARGET" | tee -a "$LOG_FILE"
echo "======================================================================" | tee -a "$LOG_FILE"
echo "Output is being logged to: $LOG_FILE"

# Call the main python analysis script
python3 "${FRAMEWORK_DIR}/run_analysis_eegnet.py" \
    "$SUBJECT_TARGET" \
    "$CHANNELS_TARGET" \
    "$EVENT_TARGET" \
    --model_dir_base "$MODEL_DIR_BASE" \
    --output_dir_base "$OUTPUT_DIR_BASE" \
    --epochs 1 \
    2>&1 | tee -a "$LOG_FILE"

# 4. Check Exit Code and Finalize
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "Error: Python script failed. Check log for details: $LOG_FILE" | tee -a "$LOG_FILE"
    exit 1
fi

echo "======================================================================" | tee -a "$LOG_FILE"
echo "Experiment Finished Successfully." | tee -a "$LOG_FILE"
echo "Results are saved in subdirectories within: $OUTPUT_DIR_BASE"
echo "Log file is at: $LOG_FILE"
echo "======================================================================"

exit 0
