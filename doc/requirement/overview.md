# Project Overview and Evaluation Criteria

## 1. Project Goal

Imagine how we would accomplish a series of daily activities like waking up, dressing, brushing teeth, and making coffee without hands. For patients who have lost hand function due to amputation or neurological diseases, this is their daily reality.

The ultimate goal of this project is to advance **Brain-Computer Interface (BCI)** technology to develop prosthetic devices that patients can control directly through brain activity. This will greatly enhance their independent living capabilities and quality of life.

## 2. Challenge Task

EEG (Electroencephalography) signals are electrical signals of brain activity recorded from the scalp, but their relationship with brain activity is very complex. The core challenge of this competition is:

> **Using EEG data recorded from healthy subjects performing a series of actions such as "grasping, lifting, and replacing" an object, accurately identify which specific event phase their hand is in.**

By better understanding the relationship between EEG signals and hand movements, we can lay the foundation for developing more reliable, low-risk, and non-invasive BCI devices.

## 3. Evaluation Metric

Submission results will be evaluated using **Mean Column-wise AUC (Area Under the ROC Curve)**.

Specifically, the evaluation system will calculate the AUC for **each event column** (e.g., `HandStart`, `FirstDigitTouch`, etc.) independently, and then average all AUC scores.

Since predictions cover multiple subjects and series, your submitted probability values should be calibrated to ensure they are on a unified scale.

## 4. Submission File Format

You must predict the probability of occurrence for six events for each `id` (corresponding to a time frame) in the test set. The `id` is concatenated as `subject_series_frame`.

The submitted `.csv` file must include a header and follow this format:

```csv
id,HandStart,FirstDigitTouch,BothStartLoadPhase,LiftOff,Replace,BothReleased
subj1_series9_0,0,0,0,0,0,0
subj1_series9_1,0,0,0,0,0,0
subj1_series9_2,0,0,0,0,0,0
...
```

## 5. Acknowledgements

This competition is sponsored by the **WAY Consortium** (Wearable interfaces for hAnd function recoverY; FP7-ICT-288551).
