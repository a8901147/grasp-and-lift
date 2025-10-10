### **Experiment 1: Baseline Model with Raw EEG Signal for "BothStartLoadPhase" Event**

**1. Research Question**

This experiment aims to establish a baseline performance for event prediction using raw EEG signals without any feature engineering. The central question is: Does the unprocessed EEG signal from a single channel contain sufficient information to predict the "BothStartLoadPhase" event with an accuracy significantly better than random chance? This baseline will serve as a benchmark to evaluate the effectiveness of future feature engineering and modeling improvements.

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
| 1 | 0.5797 |
| 2 | 0.5484 |
| 3 | 0.6625 |
| 4 | 0.5530 |
| 5 | 0.5367 |
| 6 | 0.5278 |
| 7 | 0.5907 |
| 8 | 0.5385 |
| 9 | 0.5432 |
| 10 | 0.5873 |
| 11 | 0.5356 |
| 12 | 0.5129 |

Similar to other events, the performance of the baseline model on "BothStartLoadPhase" is modest. Most subjects' average AUC scores are above 0.5, confirming the presence of some predictive signal. Subject 3 stands out with a significantly higher AUC, indicating that for this individual, the raw signal is more informative for this specific event.

**4. Conclusion & Next Steps**

A performance baseline for the "BothStartLoadPhase" event has been established. The results reinforce the conclusion from other baseline experiments: raw EEG signals alone are insufficient for building a high-performance, generalizable model.

The next step is to proceed with the **feature_filterbank_v1** experiment. This will involve applying filter bank feature extraction to the signals before training the models, with the hypothesis that this will lead to a significant improvement in AUC scores across all subjects.