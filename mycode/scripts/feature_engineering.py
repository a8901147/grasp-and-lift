# -*- coding: utf-8 -*-
"""
This module contains classes and functions for feature engineering on EEG data.
"""
import numpy as np
import pandas as pd # Added for DataFrame handling
from sklearn.base import BaseEstimator, TransformerMixin
from scipy.signal import butter, lfilter
import mne
from mne.decoding import CSP

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

class CSPFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    CSP Feature Extractor TransformerMixin.
    Applies Common Spatial Pattern (CSP) to epoched EEG data.
    """

    def __init__(self, n_components=4, reg=None, log=True, norm_trace=False, sfreq=500.0, tmin=-4.0, tmax=0.0, event_id={'event': 1}):
        self.n_components = n_components
        self.reg = reg
        self.log = log
        self.norm_trace = norm_trace
        self.sfreq = sfreq
        self.tmin = tmin
        self.tmax = tmax
        self.event_id = event_id
        self.csp = None
        self.ch_names = None

    def fit(self, X, y=None):
        self.ch_names = X.columns.tolist()
        info = mne.create_info(ch_names=self.ch_names, sfreq=self.sfreq, ch_types='eeg')
        raw = mne.io.RawArray(X.T, info, verbose=False)

        event_samples_str = y[y == 1].index.values
        event_samples = np.unique([int(idx.split('_')[-1]) for idx in event_samples_str])

        mne_events = np.array([[s, 0, 1] for s in event_samples])
        
        valid_mne_events = []
        for event_s, duration, event_id_val in mne_events:
            # Ensure the epoch window (tmin to tmax relative to event_s) is within raw data bounds
            epoch_start_sample = event_s + int(self.tmin * self.sfreq)
            epoch_end_sample = event_s + int(self.tmax * self.sfreq)
            if (epoch_start_sample >= 0) and (epoch_end_sample <= raw.n_times):
                valid_mne_events.append([event_s, duration, event_id_val])
        mne_events = np.array(valid_mne_events)

        if len(mne_events) == 0:
            raise ValueError("No valid events found for epoching. Check event data and tmin/tmax.")

        epochs = mne.Epochs(raw, mne_events, self.event_id, self.tmin, self.tmax,
                            proj=False, baseline=None, preload=True, verbose=False, event_repeated='drop')

        if len(np.unique(epochs.events[:, 2])) < 2:
            print("Warning: Only one class found in epochs. CSP may not be effective.")
            self.csp = None
            return self

        self.csp = CSP(n_components=self.n_components, reg=self.reg,
                       log=self.log, norm_trace=self.norm_trace)
        self.csp.fit(epochs.get_data(), epochs.events[:, 2])

        return self

    def transform(self, X, y=None):
        if self.csp is None:
            return pd.DataFrame(np.zeros((X.shape[0], self.n_components)), index=X.index, columns=[f'csp_{i}' for i in range(self.n_components)])

        csp_features_df = pd.DataFrame(index=X.index, columns=[f'csp_{i}' for i in range(self.n_components)])

        # Calculate window duration in samples
        window_duration_samples = int((self.tmax - self.tmin) * self.sfreq)

        # Apply spatial filters to the entire continuous data
        # X.values has shape (n_samples, n_channels)
        # self.csp.filters_ has shape (n_components, n_channels)
        # Spatially filtered data will have shape (n_samples, n_components)
        spatially_filtered_data = np.dot(X.values, self.csp.filters_.T)

        # Iterate through each time point to calculate log-variance in a sliding window
        for i in range(X.shape[0]):
            current_features = np.zeros(self.n_components)
            
            # Ensure enough past data for a full window ending at current sample 'i'
            if i >= window_duration_samples - 1:
                window_data = spatially_filtered_data[i - window_duration_samples + 1 : i + 1, :]
                # Calculate log-variance for each component within the window
                # Add a small epsilon to avoid log(0) if variance is zero
                current_features = np.log(np.var(window_data, axis=0) + 1e-6)
            
            csp_features_df.iloc[i] = current_features

        return csp_features_df
