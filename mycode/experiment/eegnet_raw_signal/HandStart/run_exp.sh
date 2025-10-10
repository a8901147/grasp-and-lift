#!/bin/bash

# --- Experiment Configuration ---
SUBJECT=${1:-1}          # Use the 1st argument, or default to 1
CHANNELS=${2:-"all"}     # Use the 2nd argument, or default to "all"
EVENT=${3:-"HandStart"}  # Use the 3rd argument, or default to "HandStart" 
BASE_EXP_DIR_NAME="eegnet_raw_signal"

# --- Script Configuration ---
# Construct absolute paths to avoid issues with cd
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ROOT_DIR="$SCRIPT_DIR/../../../../" # Root of the project
SCRIPTS_DIR="$ROOT_DIR/mycode/scripts"
TRAIN_SCRIPT="$SCRIPTS_DIR/train_eegnet.py"
EVAL_SCRIPT="$SCRIPTS_DIR/evaluate_eegnet.py"

# --- Path Definitions (now dynamic based on config) ---
RUN_NAME="subj-${SUBJECT}_chan-${CHANNELS}_evt-$(echo "$EVENT" | tr '[:upper:]' '[:lower:]')"
EXP_DIR="$ROOT_DIR/mycode/experiment/$BASE_EXP_DIR_NAME/$RUN_NAME"
MODEL_DIR_BASE="$ROOT_DIR/mycode/experiment/$BASE_EXP_DIR_NAME" # Base dir for models
RESULTS_DIR_BASE="$ROOT_DIR/mycode/experiment/$BASE_EXP_DIR_NAME" # Base dir for results

LOG_FILE="$EXP_DIR/run_exp.log"

# --- Hyperparameters ---
EPOCHS=1 # Using a small number for a quick test run
BATCH_SIZE=64
LEARNING_RATE=0.001
WINDOW_SIZE=500 # 500 samples = 1 second of data at 500Hz

# --- Ensure directories exist ---
mkdir -p "$EXP_DIR"

# --- Start Logging ---
# Clear previous log file
> "$LOG_FILE"
# Function to tee output to both console and log file
log() {
    echo "$@" | tee -a "$LOG_FILE"
}

log "======================================================================="
log "Starting EEGNet Experiment: Subject $SUBJECT, Event $EVENT, Channels $CHANNELS"
log "Timestamp: $(date)"
log "======================================================================="
log "Configuration:"
log "  - Experiment Dir: $EXP_DIR"
log "  - Log File: $LOG_FILE"
log "  - Epochs: $EPOCHS"
log "  - Batch Size: $BATCH_SIZE"
log "  - Learning Rate: $LEARNING_RATE"
log "  - Window Size: $WINDOW_SIZE"
log "-----------------------------------------------------------------------"


# --- 1. Training ---
log "Step 1: Starting Training..."
# Change to the project root so imports and relative paths in python work correctly
cd "$ROOT_DIR"

python3 -u "$TRAIN_SCRIPT" "$SUBJECT" "$EVENT" \
    --channels "$CHANNELS" \
    --output_dir_base "$MODEL_DIR_BASE" \
    --epochs "$EPOCHS" \
    --batch-size "$BATCH_SIZE" \
    --lr "$LEARNING_RATE" \
    --window-size "$WINDOW_SIZE" \
    2>&1 | tee -a "$LOG_FILE"

# Check if training was successful
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    log "Error: Training script failed. See log for details."
    exit 1
fi
log "Step 1: Training finished successfully."
log "-----------------------------------------------------------------------"


# --- 2. Evaluation ---
log "Step 2: Starting Evaluation..."

python3 -u "$EVAL_SCRIPT" "$SUBJECT" "$EVENT" \
    --channels "$CHANNELS" \
    --model_dir_base "$MODEL_DIR_BASE" \
    --output_dir_base "$RESULTS_DIR_BASE" \
    --window-size "$WINDOW_SIZE" \
    2>&1 | tee -a "$LOG_FILE"

if [ ${PIPESTATUS[0]} -ne 0 ]; then
    log "Error: Evaluation script failed. See log for details."
    exit 1
fi
log "Step 2: Evaluation finished successfully."
log "======================================================================="
log "Experiment finished."
log "Submission file generated in: $EXP_DIR/results/submission.csv"
log "======================================================================="

# Return to the original directory
cd "$SCRIPT_DIR"