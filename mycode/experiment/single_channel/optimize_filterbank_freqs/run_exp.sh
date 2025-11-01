#!/bin/bash

# ##############################################################################
# # Experiment Template
# #
# # This is a template for running experiments. To create a new experiment:
# # 1. Copy this file into your new experiment directory (e.g., mycode/experiment/expX/).
# # 2. Rename it to `run_exp.sh`.
# # 3. Modify the `FEATURE_EXTRACTOR` variable below as needed.
# ##############################################################################

# --- Usage ---
#
# ./run_exp.sh <subject_id> <channel_name> <event_name>
# Example (single target):
#   ./run_exp.sh 1 C3 HandStart
#
# Example (all targets):
#   ./run_exp.sh all all HandStart
#
# ##############################################################################

# --- Script Body ---

# 1. Define Experiment Parameters
# Separate positional args from flags
POSITIONAL_ARGS=()
QUIET_FLAG=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --quiet)
            QUIET_FLAG="--quiet"
            shift # past argument
            ;;
        *)
            POSITIONAL_ARGS+=("$1") # save positional arg
            shift # past argument
            ;;
    esac
done
set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

SUBJECT_TARGET="${1:-all}"
CHANNEL_TARGET="${2:-all}"
EVENT_TARGET="${3:-HandStart}"

# --- TODO: CONFIGURE THIS FOR YOUR EXPERIMENT ---
# Set the feature extractor to use.
# - Leave empty ("") for the baseline model (raw signal).
# - Set to "filterbank" to use the Filter Bank features.
FEATURE_EXTRACTOR="filterbank"
# -----------------------------------------

# 2. Get Script Directory and Define Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
FRAMEWORK_DIR="${SCRIPT_DIR}/../../scripts"

# Create a unique output directory for this run to avoid race conditions
RUN_DIR_NAME="subj${SUBJECT_TARGET}_${CHANNEL_TARGET}_${EVENT_TARGET}"
RUN_OUTPUT_DIR="${SCRIPT_DIR}/${RUN_DIR_NAME}"

LOG_FILE="${RUN_OUTPUT_DIR}/run_exp.log"
# Redefine output/model dirs to be inside the unique run folder
OUTPUT_DIR="${RUN_OUTPUT_DIR}"
MODEL_DIR="${RUN_OUTPUT_DIR}/temp_models"

# Create the output directories if they don't exist
mkdir -p "$OUTPUT_DIR"
mkdir -p "$MODEL_DIR"

# 3. Execute the Python Engine and Log Output
echo "======================================================================" > "$LOG_FILE"
echo "Starting Experiment: $(basename "$SCRIPT_DIR")" | tee -a "$LOG_FILE"
echo "  - Subject(s): $SUBJECT_TARGET" | tee -a "$LOG_FILE"
echo "  - Channel(s): $CHANNEL_TARGET" | tee -a "$LOG_FILE"
echo "  - Event:      $EVENT_TARGET" | tee -a "$LOG_FILE"

# Log the feature extractor being used
if [ -z "$FEATURE_EXTRACTOR" ]; then
    echo "  - Features:   <None (Raw Signal)>" | tee -a "$LOG_FILE"
else
    echo "  - Features:   $FEATURE_EXTRACTOR (Optimization Mode)" | tee -a "$LOG_FILE"
fi

echo "  - Output Dir: $OUTPUT_DIR" | tee -a "$LOG_FILE"
echo "  - Model Dir:  $MODEL_DIR" | tee -a "$LOG_FILE"
echo "======================================================================" | tee -a "$LOG_FILE"
echo "Output is being logged to: $LOG_FILE"

# Call the main python analysis script with optimization flags
python3 "${FRAMEWORK_DIR}/run_analysis.py" \
    "$SUBJECT_TARGET" \
    "$CHANNEL_TARGET" \
    "$EVENT_TARGET" \
    --output_dir "$OUTPUT_DIR" \
    --model_dir "$MODEL_DIR" \
    --feature-extractor "$FEATURE_EXTRACTOR" \
    --optimize-freqs \
    --n_calls 50 \
    $QUIET_FLAG 2>&1 | tee -a "$LOG_FILE"

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