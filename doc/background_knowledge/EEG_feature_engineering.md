# EEG Feature Engineering: From Time Domain to Spatial Domain

EEG signals are inherently complex time-series data. To enable machine learning models to learn effectively from them, we need to transform the raw voltage fluctuations into meaningful, quantitative metrics—this is **feature engineering**.

EEG features can be extracted from different dimensions, primarily categorized into the following four types:

1.  **Time Domain**: Directly analyzing the signal's waveform and amplitude.
2.  **Frequency Domain**: Analyzing the composition of different brainwave frequencies within the signal.
3.  **Time-Frequency Domain**: Combining time and frequency to analyze when specific frequencies occur.
4.  **Spatial Domain**: Analyzing the spatial relationships between multiple electrodes (channels).

---

## 1. Time Domain Features

These features directly describe the signal's amplitude and shape over time. They are computationally fast and intuitive.

-   **Root Mean Square (RMS)**: A measure of the signal's activity level or energy; a simple estimate of the total signal power. A higher RMS indicates greater brainwave fluctuation.
-   **Standard Deviation (SD)**: Describes the dispersion of the signal's amplitude around its mean. Similar to RMS, it also reflects the signal's energy.
-   **Peak / Trough**: The maximum and minimum amplitude of the signal within a time window. Particularly important in Event-Related Potential (ERP) analysis.
-   **Zero Crossing Rate (ZCR)**: The number of times the signal waveform crosses the zero axis (baseline) within a time window. A higher ZCR often indicates a higher dominant frequency in the signal.

**Advantages**: Simple to compute, fast, and easy to understand.
**Limitations**: Cannot effectively capture the most critical frequency information in EEG (like Alpha/Beta waves), which is key to distinguishing between different brain states.

---

## 2. Frequency Domain Features

Frequency-domain analysis is the **core** of EEG feature extraction. It measures how the signal's power is distributed across different frequencies.

-   **Fast Fourier Transform (FFT)**: The fundamental tool for converting a signal from the time domain to the frequency domain, outputting the amplitude and phase for different frequencies.
-   **Power Spectral Density (PSD)**: Measures the distribution of signal power over frequency. Peaks on a PSD plot represent stronger brain activity at those frequencies.

From the PSD, we can extract two key types of features:

-   **Absolute Power**: The sum of power within a specific frequency band (e.g., Alpha waves, 8-13 Hz). It reflects the total energy of that band but is susceptible to individual physiological differences.
-   **Relative Power**: The **proportion** of power in a specific band relative to the total power. This is a more robust feature that effectively normalizes for individual differences and equipment gain, making it more commonly used in Brain-Computer Interface (BCI) applications.

---

## 3. Time-Frequency Domain Features

A drawback of FFT is that it loses all temporal information. Time-frequency analysis aims to answer the question, "**Which frequency appears at which point in time?**" This is crucial for analyzing transient, burst-like brain activity.

-   **Short-Time Fourier Transform (STFT)**: Slices a long signal into multiple short time windows and performs an FFT on each window individually. The result is a "spectrogram," which shows how frequencies change over time.
-   **Wavelet Transform (WT)**: A more advanced technique that uses "wavelets" of different scales to analyze the signal. It can use narrow windows to precisely capture high-frequency transient changes while using wide windows to observe long-term low-frequency trends, making it highly suitable for analyzing complex EEG signals.

From time-frequency analysis, features like **Event-Related Synchronization/Desynchronization (ERS/ERD)** can be extracted. This measures the increase (ERS) or decrease (ERD) in power over time in a specific frequency band following an event.

---

## 4. Spatial Domain Features

When multiple electrodes are available, we can analyze the coordinated activity between different brain regions.

-   **Common Spatial Pattern (CSP)**:
    -   **Objective**: CSP is a powerful **supervised** spatial filtering technique designed to find an optimal set of linear projections that maximizes the variance difference between two classes of brain activity (e.g., "imagine left-hand movement" vs. "imagine right-hand movement").
    -   **Principle**: It learns how to combine signals from multiple channels to amplify task-related brain activity patterns while suppressing irrelevant noise.
    -   **Application**: In motor imagery BCIs, CSP is one of the most effective and classic methods for extracting features related to the ERD/ERS phenomenon. Its output is typically log-variance features, which can be directly used for classification.
