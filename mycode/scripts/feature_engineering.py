# -*- coding: utf-8 -*-
"""
This module contains classes and functions for feature engineering on EEG data.
"""
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from scipy.signal import butter, lfilter

class FilterBank(BaseEstimator, TransformerMixin):
    """
    A FilterBank transformer that applies a bank of Butterworth filters to the data.
    This is inspired by the successful approach in the Grasp-and-Lift EEG Detection challenge.
    """

    def __init__(self, filters='LowpassBank'):
        """
        Initializes the FilterBank.

        Args:
            filters (str or list): 
                - If 'LowpassBank', a default bank of low-pass filters is used.
                - If a list, it should contain frequency pairs for bandpass or lowpass filters.
                  e.g., [[0.5], [1], [2]] for lowpass, [[7, 15], [15, 30]] for bandpass.
        """
        if filters == 'LowpassBank':
            # Default filter bank from the leadership code
            self.freqs_pairs = [[0.5], [1], [2], [3], [4], [5], [7], [9], [15], [30]]
        else:
            if not isinstance(filters, list):
                raise ValueError("filters must be 'LowpassBank' or a list of frequency pairs.")
            self.freqs_pairs = filters
        
        self.sfreq = 500.0  # Sampling frequency of the EEG data

    def fit(self, X, y=None):
        """
        Fit method, required by TransformerMixin, does nothing here.
        """
        return self

    def transform(self, X, y=None):
        """
        Applies the bank of filters to the input data X.

        Args:
            X (np.ndarray): The input EEG data of shape (n_samples, n_channels).

        Returns:
            np.ndarray: The transformed data with features from all filters concatenated.
                        Shape will be (n_samples, n_channels * n_filters).
        """
        X_tot = []
        for freqs in self.freqs_pairs:
            if len(freqs) == 1:  # Low-pass filter
                b, a = butter(5, freqs[0] / (self.sfreq / 2.0), btype='lowpass')
            else:  # Band-pass filter
                # Use a lower order for narrow bands to avoid instability
                order = 3 if (freqs[1] - freqs[0]) < 3 else 5
                b, a = butter(order, np.array(freqs) / (self.sfreq / 2.0), btype='bandpass')
            
            # Apply the filter along the time axis (axis=0)
            X_filtered = lfilter(b, a, X, axis=0)
            X_tot.append(X_filtered)

        # Concatenate along the feature axis (axis=1)
        return np.concatenate(X_tot, axis=1)
