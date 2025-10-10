### **Experiment 1: Baseline Model with Raw EEG Signal for "HandStart" Event**

**1. Research Question**

This experiment aims to establish a baseline performance for event prediction using raw EEG signals without any feature engineering. The central question is: Does the unprocessed EEG signal from a single channel contain sufficient information to predict the "HandStart" event with an accuracy significantly better than random chance? This baseline will serve as a benchmark to evaluate the effectiveness of future feature engineering and modeling improvements.

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
| 1 | 0.5440 |
| 2 | 0.6346 |
| 3 | 0.5984 |
| 4 | 0.5839 |
| 5 | 0.5851 |
| 6 | 0.5318 |
| 7 | 0.5303 |
| 8 | 0.5981 |
| 9 | 0.5192 |
| 10 | 0.5833 |
| 11 | 0.5889 |
| 12 | 0.5711 |

The results indicate that even with raw signals, most subjects show an average AUC score significantly above 0.5, suggesting that there is some predictive information present in the unprocessed EEG data. However, the performance is generally low and inconsistent across subjects, highlighting the need for more advanced signal processing.

**4. Conclusion & Next Steps**

This experiment successfully established a baseline for the "HandStart" event. The key conclusion is that while raw EEG signals contain some predictive power, they are not sufficient for building a robust and accurate prediction model.

Based on these findings, the next logical step is to investigate the impact of feature engineering. The subsequent experiment, **feature_filterbank_v1**, will apply a filter bank to the raw signals to extract frequency-based features and evaluate if this technique can significantly improve upon the baseline AUC scores.
