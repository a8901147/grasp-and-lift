### **Experiment 1: Baseline Model with Raw EEG Signal for "FirstDigitTouch" Event**

**1. Research Question**

This experiment aims to establish a baseline performance for event prediction using raw EEG signals without any feature engineering. The central question is: Does the unprocessed EEG signal from a single channel contain sufficient information to predict the "FirstDigitTouch" event with an accuracy significantly better than random chance? This baseline will serve as a benchmark to evaluate the effectiveness of future feature engineering and modeling improvements.

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
| 1 | 0.5905 |
| 2 | 0.5980 |
| 3 | 0.6590 |
| 4 | 0.5721 |
| 5 | 0.5332 |
| 6 | 0.5219 |
| 7 | 0.5864 |
| 8 | 0.5395 |
| 9 | 0.5266 |
| 10 | 0.6017 |
| 11 | 0.5293 |
| 12 | 0.4998 |

The results show a wide range of performance across subjects. While some subjects (e.g., Subject 3) achieve a respectable average AUC, others are much closer to the random-chance baseline of 0.5. This variability suggests that the raw signal's predictive power for "FirstDigitTouch" is highly subject-dependent.

**4. Conclusion & Next Steps**

This experiment successfully established a baseline for the "FirstDigitTouch" event. The conclusion is that raw EEG signals alone are not reliable for creating a generalized model, although they do contain some predictive information for certain individuals.

The clear next step is to apply feature engineering to determine if a more sophisticated representation of the signal can improve performance and reduce the variability between subjects. The subsequent experiment, **feature_filterbank_v1**, will address this by using a filter bank to extract frequency-based features.