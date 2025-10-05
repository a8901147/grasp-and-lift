#!/bin/bash

# ##############################################################################
# # Experiment 1: Baseline Model with Raw Signal
# #
# # This script runs the baseline analysis using raw single-channel EEG signals.
# ##############################################################################

# --- Usage ---
#
# ./run_exp.sh <subject_id> <channel_name> <event_name>
# Example (single subject, single channel):
#   ./run_exp.sh 1 C3 HandStart
#
# Example (all subjects, all channels):
#   ./run_exp.sh all all HandStart
#
# ##############################################################################

# --- Script Body ---

# 1. Define Experiment Parameters
SUBJECT_TARGET="${1:-all}"
CHANNEL_TARGET="${2:-all}"
EVENT_TARGET="${3:-HandStart}"
FEATURE_EXTRACTOR=""  # Baseline experiment uses no feature extractor (raw signal)

# 2. Get Script Directory and Define Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
LOG_FILE="${SCRIPT_DIR}/run_exp.log"
FRAMEWORK_DIR="${SCRIPT_DIR}/../../../scripts"
OUTPUT_DIR="${SCRIPT_DIR}/results"
MODEL_DIR="${SCRIPT_DIR}/model"

# Create the output directories if they don't exist
mkdir -p "$OUTPUT_DIR"
mkdir -p "$MODEL_DIR"

# 3. Execute the Python Engine and Log Output
echo "======================================================================" > "$LOG_FILE"
echo "Starting Experiment: $(basename "$SCRIPT_DIR")" | tee -a "$LOG_FILE"
echo "  - Subject(s): $SUBJECT_TARGET" | tee -a "$LOG_FILE"
echo "  - Channel(s): $CHANNEL_TARGET" | tee -a "$LOG_FILE"
echo "  - Event:      $EVENT_TARGET" | tee -a "$LOG_FILE"
echo "  - Features:   <None (Raw Signal)>" | tee -a "$LOG_FILE"
echo "  - Output Dir: $OUTPUT_DIR" | tee -a "$LOG_FILE"
echo "  - Model Dir:  $MODEL_DIR" | tee -a "$LOG_FILE"
echo "======================================================================" | tee -a "$LOG_FILE"
echo "Output is being logged to: $LOG_FILE"

# Call the main python analysis script
# The --feature-extractor argument will be empty, defaulting to None in the Python script
python3 "${FRAMEWORK_DIR}/run_analysis.py" \
    "$SUBJECT_TARGET" \
    "$CHANNEL_TARGET" \
    "$EVENT_TARGET" \
    --output_dir "$OUTPUT_DIR" \
    --model_dir "$MODEL_DIR" \
    --feature-extractor "$FEATURE_EXTRACTOR" 2>&1 | tee -a "$LOG_FILE"

# 4. Check Exit Code and Finalize
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "Error: Python script failed. Check log for details: $LOG_FILE" | tee -a "$LOG_FILE"
    exit 1
fi

echo "======================================================================" | tee -a "$LOG_FILE"
echo "Experiment Finished Successfully." | tee -a "$LOG_FILE"
echo "Results are saved in: $OUTPUT_DIR"
echo "Log file is at: $LOG_FILE"
echo "======================================================================"

exit 0