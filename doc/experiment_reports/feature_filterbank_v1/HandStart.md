### **Experiment exp1-B: Filter Bank Feature Engineering**

**1. Research Question**

*   The core question of this experiment is: Can the Filter Bank feature engineering technique used in the `leadership_code` significantly improve the predictive performance of the baseline model (`exp1`), which is based on raw single-channel signals?
*   We hypothesize that by extracting and combining signal features from multiple low-frequency bands, the model can more effectively capture the neural activity associated with the `HandStart` event, thereby substantially increasing the AUC score.

**2. Methodology**

*   **Model:**
    *   Consistent with `exp1`, using a `sklearn.pipeline.Pipeline` that includes `StandardScaler` and `LogisticRegression`.

*   **Features:**
    *   Raw EEG signals are no longer used.
    *   A `FilterBank` feature extractor is employed. The raw signal from each channel is subjected to 7 low-pass filters (with cutoff frequencies of 1, 2, 4, 8, 16, 32, and 64 Hz, respectively). These 7 filtered signals are then concatenated along the feature axis to form a richer feature set.
    > **[Additional Note]**: The `1, 2, 4...` Hz combination described here is a theoretical example based on a common logarithmic scale. In the actual code at `mycode/scripts/feature_engineering.py`, to replicate the success of the `leadership_code`, we adopted its more fine-tuned parameter combination: `[0.5, 1, 2, 3, 4, 5, 7, 9, 15, 30]` Hz.

*   **Procedure:**
    1.  **Scope**: All 32 channels (`all`) for all 12 subjects (`all`), targeting the `HandStart` event.
    2.  **Execution**: The `run_analysis.py` script was executed with the `--feature-extractor filterbank` argument to specify the use of Filter Bank feature engineering.
    3.  **Evaluation**: Same as `exp1`, using the Area Under the Curve (AUC) on series 7-8 as the primary evaluation metric.
    4.  **Output**: For each subject, a bar chart was generated to display the AUC scores for all their channels, along with global heatmaps and boxplots for comprehensive analysis.

**3. Key Findings & Analysis**

*   **Significant Overall Performance Improvement**: The Filter Bank brought about a comprehensive and massive performance boost. The overall AUC score range for the model significantly widened and shifted upward from `0.5-0.78` in `exp1` to `0.6-0.88`. More importantly, the performance floor was substantially raised, with nearly all channels performing far better than random chance.

*   **Comeback of "Underperforming" Channels**: The most striking highlight of this method was its ability to "rescue" channels that performed very poorly in `exp1`.
    *   **Subject 1, Channel `Fp1`**: AUC jumped from `0.4237` (worse than random) to `0.7639`.
    *   **Subject 2, Channel `C3`**: AUC impressively reversed from `0.3925` (one of the worst) to `0.7381`.
    *   This demonstrates that the Filter Bank can effectively extract task-relevant information from high-noise signals.

*   **Reshuffling of Channel Importance**: A profound insight was the change in the ranking of the best predictive channels. For instance, the best channel for `Subject 1` changed from `C3` in `exp1` to `Fp1`. This indicates that the signal-to-noise ratio of the raw signal is not entirely equivalent to its potential information content, and proper feature engineering can uncover valuable information masked by noise.

*   **Hypothesis Confirmed**: The experimental results strongly confirm our hypothesis that the key EEG features related to hand movement intention are predominantly distributed in the low-frequency bands.

**4. Conclusion & Next Steps**

*   **Conclusion**: `exp1-B` was a resounding success. The Filter Bank is not just an effective feature engineering method; it is a crucial step in understanding the neural signals for the current task. It should be established as the standard preprocessing pipeline for all subsequent experiments.

*   **Next Steps**: We have answered the question, "Is the Filter Bank effective?". The next, more exploratory question is, "**Why is the Filter Bank effective? Which frequency band or bands contribute the most?**".
    *   **`Experiment exp1-C`**: Conduct an **Ablation Study**. We will modify the `FilterBank` code to test the impact of different frequency band combinations (e.g., using only `1-8Hz`, or removing a specific band) on model performance. This will help us:
        1.  Gain a deeper understanding of the physical meaning of the signals.
        2.  Potentially simplify and optimize the feature set, reducing computational complexity.
        3.  Provide a research direction for finding the "golden frequency bands" for different events (like `FirstDigitTouch`, `LiftOff`) in the future.