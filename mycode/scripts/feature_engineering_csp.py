# -*- coding: utf-8 -*-
"""
This module contains a CSP (Common Spatial Pattern) feature extractor for EEG data.
"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import mne
from mne.decoding import CSP

class CSPFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    CSP Feature Extractor TransformerMixin.
    Applies Common Spatial Pattern (CSP) to epoched EEG data.
    """

    def __init__(self, n_components=4, reg=None, log=True, norm_trace=False, sfreq=500.0, tmin=-1.0, tmax=3.0):
        """
        Initializes the CSPFeatureExtractor.

        Args:
            n_components (int): Number of CSP components to extract.
            reg (float or None): Regularization parameter for CSP.
            log (bool): If True, apply log transform to the CSP features.
            norm_trace (bool): If True, normalize the trace of the covariance matrices.
            sfreq (float): Sampling frequency of the EEG data.
            tmin (float): Start time of epoch relative to event (in seconds).
            tmax (float): End time of epoch relative to event (in seconds).
        """
        self.n_components = n_components
        self.reg = reg
        self.log = log
        self.norm_trace = norm_trace
        self.sfreq = sfreq
        self.tmin = tmin
        self.tmax = tmax
        self.csp = None
        self.ch_names = None

    def fit(self, X, y=None, event_data=None, event_id=None):
        """
        Fits the CSP model.

        Args:
            X (pd.DataFrame): The raw continuous EEG data of shape (n_samples, n_channels).
            y (pd.Series): The target labels for classification (e.g., 0 or 1).
                           This is used to define the classes for CSP.
            event_data (pd.DataFrame): DataFrame containing event markers.
            event_id (dict): Dictionary mapping event names to event IDs.
        """
        if event_data is None or event_id is None:
            raise ValueError("Event data and event_id must be provided for CSP fitting.")

        self.ch_names = X.columns.tolist()
        info = mne.create_info(ch_names=self.ch_names, sfreq=self.sfreq, ch_types='eeg')
        raw = mne.io.RawArray(X.T, info, verbose=False)

        # MNE events array: (n_events, 3) where columns are [sample, duration, event_id]
        # We need to convert our event_data (which is y) into MNE events format
        # Assuming y contains 0s and 1s, and 1 indicates an event.
        # We need to find the sample indices where y changes from 0 to 1 (or is 1 for a duration)
        # For simplicity, let's assume y=1 marks the event onset for now.
        # This part might need refinement based on actual event data format.
        
        # Find event onsets (where y changes from 0 to 1, or is 1)
        # This is a simplified event detection. A more robust solution might be needed.
        event_samples = y[y == 1].index.values
        # MNE events array needs sample index, duration (usually 0), and event_id
        # Assuming event_id for the positive class is 1
        mne_events = np.array([[s, 0, 1] for s in event_samples])
        
        # Filter out events that are too close to the beginning or end of the raw data
        # to ensure full epoch can be extracted.
        valid_mne_events = []
        for event_s, duration, event_id_val in mne_events:
            if (event_s + self.tmin * self.sfreq >= 0) and (event_s + self.tmax * self.sfreq <= raw.n_times):
                valid_mne_events.append([event_s, duration, event_id_val])
        mne_events = np.array(valid_mne_events)

        if len(mne_events) == 0:
            raise ValueError("No valid events found for epoching. Check event data and tmin/tmax.")

        epochs = mne.Epochs(raw, mne_events, event_id, self.tmin, self.tmax,
                            proj=False, baseline=None, preload=True, verbose=False)

        # Ensure epochs have at least two classes for CSP
        if len(np.unique(epochs.events[:, 2])) < 2:
            raise ValueError("CSP requires at least two classes for fitting.")

        # Initialize and fit CSP
        self.csp = CSP(n_components=self.n_components, reg=self.reg,
                       log=self.log, norm_trace=self.norm_trace)
        self.csp.fit(epochs.get_data(), epochs.events[:, 2]) # epochs.get_data() returns (n_epochs, n_channels, n_times)

        return self

    def transform(self, X, y=None):
        """
        Transforms the raw EEG data into CSP features.

        Args:
            X (pd.DataFrame): The raw continuous EEG data of shape (n_samples, n_channels).
            y (pd.Series): The target labels for classification (e.g., 0 or 1).
                           This is used to define the classes for CSP.

        Returns:
            np.ndarray: The CSP features of shape (n_epochs, n_components).
        """
        if self.csp is None:
            raise RuntimeError("CSP model has not been fitted yet. Call fit() first.")
        if self.ch_names is None:
            raise RuntimeError("Channel names were not stored during fit. Call fit() first.")

        info = mne.create_info(ch_names=self.ch_names, sfreq=self.sfreq, ch_types='eeg')
        raw = mne.io.RawArray(X.T, info, verbose=False)

        # For transform, we need to re-epoch the data based on the same events used in fit.
        # However, in a typical prediction scenario, we might not have 'y' (labels) for the test set.
        # If y is provided, we can use it to re-create events.
        # If not, we need a way to define epochs for prediction.
        # For now, let's assume y is always provided for simplicity in this framework.
        
        event_samples = y[y == 1].index.values
        mne_events = np.array([[s, 0, 1] for s in event_samples])

        valid_mne_events = []
        for event_s, duration, event_id_val in mne_events:
            if (event_s + self.tmin * self.sfreq >= 0) and (event_s + self.tmax * self.sfreq <= raw.n_times):
                valid_mne_events.append([event_s, duration, event_id_val])
        mne_events = np.array(valid_mne_events)

        if len(mne_events) == 0:
            # If no events, return an empty array of appropriate shape
            return np.empty((0, self.n_components))

        epochs = mne.Epochs(raw, mne_events, {'event': 1}, self.tmin, self.tmax,
                            proj=False, baseline=None, preload=True, verbose=False)

        # Transform epochs using the fitted CSP
        csp_features = self.csp.transform(epochs.get_data())

        return csp_features