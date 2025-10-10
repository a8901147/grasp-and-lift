### **Experiment 1: Baseline Model with Raw EEG Signal for "LiftOff" Event**

**1. Research Question**

This experiment aims to establish a baseline performance for event prediction using raw EEG signals without any feature engineering. The central question is: Does the unprocessed EEG signal from a single channel contain sufficient information to predict the "LiftOff" event with an accuracy significantly better than random chance? This baseline will serve as a benchmark to evaluate the effectiveness of future feature engineering and modeling improvements.

**2. Methodology**

*   **Model:**
    *   Logistic Regression. This model was chosen for its simplicity and efficiency as a baseline classifier. It is configured with balanced class weights to handle imbalanced data.

*   **Features:**
    *   Raw EEG signal data from a single channel at a time. No transformations or feature extraction methods were applied.

*   **Procedure:**
    1.  **Data Splitting:** For each subject, data from series 1-6 were used for training, and series 7-8 were used for validation.
    2.  **Training:** A separate model was trained for each of the 32 EEG channels for each of the 12 subjects. The training process involved a pipeline that first standardized the data using `StandardScaler` and then fed it to the `LogisticRegression` classifier.
    3.  **Evaluation:** The performance of each model was evaluated using the Area Under the Receiver Operating Characteristic Curve (AUC). An average AUC score was then calculated across all 32 channels for each subject to provide a summary of overall performance.

**3. Key Findings & Analysis**

The experiment was executed for all 12 subjects across all 32 channels. The average AUC scores for each subject are summarized below:

| Subject | Average AUC |
| :--- | :--- |
| 1 | 0.5822 |
| 2 | 0.5485 |
| 3 | 0.6338 |
| 4 | 0.5323 |
| 5 | 0.5406 |
| 6 | 0.5378 |
| 7 | 0.5653 |
| 8 | 0.5341 |
| 9 | 0.5659 |
| 10 | 0.5576 |
| 11 | 0.5436 |
| 12 | 0.5441 |

The results for the "LiftOff" event are consistent with other baseline experiments. The average AUC scores hover above 0.5, indicating some level of predictive capability from the raw signal, but the performance is not strong enough for a reliable model.

**4. Conclusion & Next Steps**

This experiment establishes a performance baseline for the "LiftOff" event. As with the other events, the raw EEG signal alone is not sufficient for high-performance prediction.

The next step is to proceed with the **feature_filterbank_v1** experiment to see if feature engineering can improve these results.
