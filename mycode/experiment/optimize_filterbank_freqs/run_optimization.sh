#!/bin/bash

# ##############################################################################
# # Experiment: Optimize Filterbank Frequencies
# #
# # This script launches the Bayesian Optimization engine to find the best
# # set of cutoff frequencies for the Filterbank feature extractor.
# ##############################################################################

# --- Usage ---
#
# ./run_optimization.sh <subject_id> <channel_name> <event_name>
# Example (Quick test on Subject 1):
#   ./run_optimization.sh 1 all HandStart
#
# Example (Full run on all subjects):
#   ./run_optimization.sh all all HandStart
#
# ##############################################################################

# --- Script Body ---

# 1. Define Experiment Parameters
# Default to Subject 1 for quick tests if no arguments are provided.
SUBJECT_TARGET="${1:-1}"
CHANNEL_TARGET="${2:-all}"
EVENT_TARGET="${3:-HandStart}"
ITERATIONS=25 # Number of optimization calls

# Sanitize inputs for filename
SUBJ_STR=$(echo "$SUBJECT_TARGET" | sed 's/[, ]/-/g')
CHAN_STR=$(echo "$CHANNEL_TARGET" | sed 's/[, ]/-/g')
RUN_NAME="subj-${SUBJ_STR}_chan-${CHAN_STR}_evt-${EVENT_TARGET}"

# 2. Get Script Directory and Define Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
LOG_FILE="${SCRIPT_DIR}/${RUN_NAME}.log"
RESULTS_FILE="${SCRIPT_DIR}/${RUN_NAME}_results.txt"
# The path is now ../../scripts, because this folder is not nested like the others
FRAMEWORK_DIR="${SCRIPT_DIR}/../../scripts"
OUTPUT_DIR="${SCRIPT_DIR}" # Save results in the experiment's root

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# 3. Execute the Python Engine and Log Output
echo "======================================================================" > "$LOG_FILE"
echo "Starting Experiment: OPTIMIZATION of Filterbank Frequencies" | tee -a "$LOG_FILE"
echo "  - Subject(s): $SUBJECT_TARGET" | tee -a "$LOG_FILE"
echo "  - Channel(s): $CHANNEL_TARGET" | tee -a "$LOG_FILE"
echo "  - Event:      $EVENT_TARGET" | tee -a "$LOG_FILE"
echo "  - Iterations: $ITERATIONS" | tee -a "$LOG_FILE"
echo "  - Output Dir: $OUTPUT_DIR" | tee -a "$LOG_FILE"
echo "======================================================================" | tee -a "$LOG_FILE"
echo "Output is being logged to: $LOG_FILE"

# Call the NEW optimization script instead of the analysis script
python3 "${FRAMEWORK_DIR}/search_hyperparameters.py" \
    "$SUBJECT_TARGET" \
    "$CHANNEL_TARGET" \
    "$EVENT_TARGET" \
    --n_calls "$ITERATIONS" \
    --output_dir "$OUTPUT_DIR" \
    --output-file "$RESULTS_FILE" 2>&1 | tee -a "$LOG_FILE"

# 4. Check Exit Code and Finalize
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "Error: Python script failed. Check log for details: $LOG_FILE" | tee -a "$LOG_FILE"
    exit 1
fi

echo "======================================================================" | tee -a "$LOG_FILE"
echo "Optimization Experiment Finished Successfully." | tee -a "$LOG_FILE"
echo "Results are saved in: $RESULTS_FILE"
echo "Log file is at: $LOG_FILE"
echo "======================================================================"

exit 0
