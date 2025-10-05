#!/bin/bash

# ##############################################################################
# # Experiment 2: Flexible Baseline Analysis Framework
# #
# # This script is the main entry point for running baseline analyses.
# # It calls the Python engine 'run_analysis.py' with specified parameters.
# ##############################################################################

# --- Usage ---
#
# This script requires three arguments: subject, channel, and event.
#
# Run for a single subject:
#   ./run_exp.sh <subject_id> <channel_name> <event_name>
#   Example: ./run_exp.sh 1 Fp1 HandStart
#
# Run for all subjects for a specific channel/event:
#   ./run_exp.sh all C3 Replace
#
# Run for all channels for a specific subject/event:
#   ./run_exp.sh 5 all LiftOff
#
# Run for all subjects and all channels for a specific event:
#   ./run_exp.sh all all HandStart
#
# ##############################################################################

# --- Script Body ---

# 1. Handle Help Flag
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    cat <<EOF
--- Usage ---

This script requires three arguments: subject, channel, and event.

Run for a single subject:
  ./run_exp.sh <subject_id> <channel_name> <event_name>
  Example: ./run_exp.sh 1 Fp1 HandStart

Run for all subjects for a specific channel/event:
  ./run_exp.sh all C3 Replace

Run for all channels for a specific subject/event:
  ./run_exp.sh 5 all LiftOff

Run for all subjects and all channels for a specific event:
  ./run_exp.sh all all HandStart
EOF
    exit 0
fi

# 2. Define Experiment Parameters
# Use command-line arguments if provided; otherwise, fall back to the default values.
SUBJECT_TARGET="${1:-1}"
CHANNEL_TARGET="${2:-all}"
EVENT_TARGET="${3:-HandStart}"

# 3. Get Script Directory and Log File Path
# This ensures that scripts are found correctly and logs are saved in the same directory as the script.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
LOG_FILE="${SCRIPT_DIR}/run_exp.log"
FRAMEWORK_DIR="${SCRIPT_DIR}/../../../scripts"
OUTPUT_DIR="${SCRIPT_DIR}/results"
MODEL_DIR="${SCRIPT_DIR}/model"

# Create the output directories if they don't exist
mkdir -p "$OUTPUT_DIR"
mkdir -p "$MODEL_DIR"

# 4. Execute the Python Engine and Log Output
echo "======================================================================" > "$LOG_FILE"
echo "Starting Experiment: $(basename "$SCRIPT_DIR")" | tee -a "$LOG_FILE"
echo "  - Subject(s): $SUBJECT_TARGET" | tee -a "$LOG_FILE"
echo "  - Channel(s): $CHANNEL_TARGET" | tee -a "$LOG_FILE"
echo "  - Event:      $EVENT_TARGET" | tee -a "$LOG_FILE"
echo "  - Output Dir: $OUTPUT_DIR" | tee -a "$LOG_FILE"
echo "======================================================================" | tee -a "$LOG_FILE"
echo "Output is being logged to: $LOG_FILE"

# Call the main python analysis script, piping all output to tee.
# '2>&1' redirects stderr to stdout.
# 'tee -a' appends to the log file while also printing to the terminal.
python3 "${FRAMEWORK_DIR}/run_analysis.py" "$SUBJECT_TARGET" "$CHANNEL_TARGET" "$EVENT_TARGET" --output_dir "$OUTPUT_DIR" --model_dir "$MODEL_DIR" 2>&1 | tee -a "$LOG_FILE"

# 5. Check Exit Code and Finalize
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "Error: Python script failed. Check log for details: $LOG_FILE" | tee -a "$LOG_FILE"
    exit 1
fi

echo "======================================================================" | tee -a "$LOG_FILE"
echo "Experiment Finished Successfully." | tee -a "$LOG_FILE"
echo "Results are saved in: $LOG_FILE"
echo "======================================================================"

exit 0
