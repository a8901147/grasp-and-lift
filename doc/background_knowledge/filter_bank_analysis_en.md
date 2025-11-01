# Technical Background: Filter Bank Feature Engineering Analysis

## 1. What is a Filter Bank?

A Filter Bank is a feature engineering technique widely used in signal processing and has proven to be highly effective, especially in the Brain-Computer Interface (BCI) field. The core idea is to decompose an original, wide-band signal (like EEG) into multiple sub-signals in different frequency bands. These sub-signals are then provided as a new feature set to a machine learning model.

In our project, we implement this using a set of **Low-pass Filters**. The original single-channel signal (1 feature) is duplicated several times, and each copy is passed through a low-pass filter with a different cutoff frequency (e.g., 1Hz, 2Hz, 4Hz...). Finally, these filtered signals are concatenated to form a richer feature set.

This method cleverly allows a simple linear model (like Logistic Regression) to independently evaluate information from different frequency bands and assign higher learning weights to those bands that contribute more to the prediction target.

## 2. Advantages and Trade-offs of a Filter Bank

### Pros

1.  **Significantly Improves Signal-to-Noise Ratio (SNR)**:
    *   EEG signals are often contaminated with a large amount of task-irrelevant noise. By using a series of low-pass filters, we can effectively isolate the low-frequency brainwaves related to motor intention (such as Mu and Beta rhythms), making it easier for the model to learn effective patterns. This is the primary reason for its substantial improvement in AUC scores.

2.  **Feature Enhancement and Information Decomposition**:
    *   Decomposing a single time-series signal into representations across multiple frequency bands greatly enriches the feature space. Instead of facing a jumble of mixed information, the model can clearly see "what's happening in the 0-4Hz band," "what's happening in the 4-8Hz band," etc., achieving information decoupling and fine-grained analysis.

3.  **High Computational Efficiency**:
    *   Compared to complex time-frequency analysis methods (like STFT or CWT), the implementation of a Filter Bank (typically based on IIR filters like Butterworth) is computationally very cheap, making it suitable for processing large datasets or for real-time applications.

4.  **Good Model Compatibility**:
    *   The features it generates can be directly fed into any standard machine learning model (e.g., Logistic Regression, SVM, Gradient Boosting Trees), serving as a plug-and-play feature enhancement module.

### Cons

1.  **Limited Frequency Resolution**:
    *   A Filter Bank provides a "coarse" view of frequency bands. It cannot provide the precise spectral information that a Fourier Transform can.

2.  **Loss of Time Resolution**:
    *   Any filtering process introduces a certain amount of "blurring" or "delay" in the time dimension (i.e., phase distortion).

3.  **Dependency on Parameter Selection**:
    *   The effectiveness is highly dependent on the choice of **cutoff frequencies**. If the selected bands are completely irrelevant to the task, it might introduce useless information and interfere with the model's learning.

4.  **Increased Feature Dimensionality**:
    *   It increases the number of features. If the original feature dimension is already high, this could increase model training time and the risk of overfitting.

## 3. Analysis of Filter Order

In our configuration, a **4th-order** Butterworth filter is used. The order of the filter determines the **width of the transition band**.

-   **Low-order Filters (e.g., 1st-2nd order)**:
    *   **Pros**: Computationally fast, minimal phase distortion.
    *   **Cons**: The transition band is very "gradual," meaning the frequency "cutoff" is not very sharp.

-   **High-order Filters (e.g., 8th order or higher)**:
    *   **Pros**: The transition band is very "steep," providing excellent frequency selectivity.
    *   **Cons**: Higher computational cost and introduces more significant phase distortion (time delay).

**Why is 4th-order a good choice?**

Choosing the **4th order** represents a classic trade-off between **frequency selectivity** and **phase distortion**. It is "steep" enough to cleanly separate frequency bands, while the phase distortion remains within an acceptable range, preventing excessive distortion of the signal's temporal characteristics. In BCI research, Butterworth filters of the 3rd to 5th order are the most common choices, representing a robust and empirically validated parameter range.
