#!/bin/bash

# This script generates time-domain plots for each filter in the filter bank,
# allowing for a visual comparison of their effects on the raw signal.

# --- Usage ---
#
# ./time_domain_visual.sh [subject_series]
#
# Arguments:
#   [subject_series]: The subject and series to plot (e.g., 'subj1_series1').
#                     Defaults to 'subj1_series1'.
#
# ##############################################################################

# 1. Define Parameters
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT="$(dirname $(dirname $(dirname $(dirname $(dirname "$SCRIPT_DIR")))))"
VISUALIZATION_SCRIPT="${PROJECT_ROOT}/mycode/visualization/plot_time_domain.py"

SUBJECT_SERIES="${1:-subj1_series1}"
OUTPUT_DIR="${SCRIPT_DIR}/time_domain_visualize"

# Frequencies used in the FilterBank experiment
FREQS=(0.5 1 2 3 4 5 7 9 15 30)

# 2. Setup Environment
echo "======================================================================"
echo "Starting Time Domain Visualization for Filter Bank"
echo "  - Subject/Series: ${SUBJECT_SERIES}"
echo "  - Output Directory: ${OUTPUT_DIR}"
echo "======================================================================"
echo "[INFO] This script assumes you have activated the project's virtual environment."
echo "       (e.g., by running 'source venv/bin/activate' from the project root)"
echo ""

# Create Output Directory
mkdir -p "$OUTPUT_DIR"

# 3. Loop Through Frequencies and Generate Plots
echo "Generating plots for each filter frequency..."

# --- Generate Unfiltered Plot ---
echo "  - Processing unfiltered raw signal..."
python3 "$VISUALIZATION_SCRIPT" "$SUBJECT_SERIES"
ls -l "${PROJECT_ROOT}/out/${SUBJECT_SERIES}/"
GENERATED_FILE_UNFILTERED="${PROJECT_ROOT}/out/${SUBJECT_SERIES}/time_domain.png"
if [ -f "$GENERATED_FILE_UNFILTERED" ]; then
    # Move the generated plot to the local output directory
    mv "$GENERATED_FILE_UNFILTERED" "${OUTPUT_DIR}/time_domain_unfiltered.png"
    echo "    -> Plot saved to ${OUTPUT_DIR}/time_domain_unfiltered.png"
else
    echo "    -> [ERROR] Unfiltered plot file was not generated."
fi

# --- Generate Filtered Plots ---
for freq in "${FREQS[@]}"; do
    echo "  - Processing low-pass filter @ ${freq} Hz..."

    # Run the visualization script
    python3 "$VISUALIZATION_SCRIPT" "$SUBJECT_SERIES" --freqs "$freq"

    # Define the expected output file and move it
    GENERATED_FILE="${PROJECT_ROOT}/out/${SUBJECT_SERIES}/time_domain_lowpass_$(printf "%.1f" "$freq")hz.png"
    echo "Checking for file: $GENERATED_FILE"
    if [ -f "$GENERATED_FILE" ]; then
        # Move the generated plot to the local output directory
        mv "$GENERATED_FILE" "$OUTPUT_DIR/"
        echo "    -> Plot saved to ${OUTPUT_DIR}/time_domain_lowpass_$(printf "%.1f" "$freq")hz.png"
    else
        echo "    -> [ERROR] Plot file was not generated for ${freq} Hz."
    fi
done

echo ""
echo "======================================================================"
echo "Visualization script finished."
echo "All plots are located in: ${OUTPUT_DIR}"
echo "======================================================================"

exit 0
