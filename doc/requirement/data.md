# Dataset Details and Rules

## 1. Data Source

Detailed descriptions of this dataset can be found in the following paper:

> Luciw MD, Jarocka E, Edin BB (2014) Multi-channel EEG recordings during 3,936 grasp and lift trials with varying weight and friction. *Scientific Data* 1:140047.
> [www.nature.com/articles/sdata201447](https://www.nature.com/articles/sdata201447)

## 2. Data Structure

-   **Subjects**: A total of 12 subjects.
-   **Series**: Each subject has 10 series of trials.
-   **Trials**: Each series contains approximately 30 trials; the exact number varies.
-   **Data Split**:
    -   **Training Set**: Includes the first 8 series (`series1` to `series8`) for each subject.
    -   **Test Set**: Includes the last 2 series (`series9` and `series10`) for each subject.

## 3. Target Events

In each Grasp-and-Lift task, you need to detect the following 6 events:

1.  `HandStart` (Hand movement begins)
2.  `FirstDigitTouch` (First digit contacts the object)
3.  `BothStartLoadPhase` (Both digits begin to apply force)
4.  `LiftOff` (Object lifts off)
5.  `Replace` (Object is replaced)
6.  `BothReleased` (Both digits are released)

These events always occur **sequentially**.

## 4. File Description

For each subject and series in the training set, two corresponding files are provided:

-   `*_data.csv`: Contains raw 32-channel EEG data, sampled at **500Hz**.
-   `*_events.csv`: Contains frame-by-frame ground truth labels.

**The `*_events.csv` file for the test set is not provided; you need to predict it.**

## 5. Label Definition

-   **ID**: Each time frame has a unique `id`, concatenated as `subject_series_frame`.
-   **Label Window**: The label fields (`1` or `0`) for the six events are determined by whether the event occurs within **+/- 150 milliseconds (ms)** of that time frame.
    -   Given a sampling rate of 500Hz, this corresponds to **+/- 75 frames**, totaling a 300ms window.
    -   A perfect prediction model should predict a probability of `1` for all frames within this window.

---

## 6. Important Rule: No Future Data

This is the **strictest rule** of this project, designed to simulate real-world application scenarios.

-   **Core Principle**: When making a prediction for any time point `t`, your model **must not** use any data from after time `t`.
    -   **Example**: When predicting the label for `subj1_series9_11`, you cannot use any information from `subj1` `series9` **after** frame 11.

-   **Prevent Data Leakage**:
    -   You must be very careful to avoid data leakage. For example, when standardizing the signal for `subj1_series9_11`, you cannot use the mean or standard deviation of the **entire series** `subj1_series9`. You can only use data from frame 0 to frame 10 to calculate statistics.
    -   The organizers will check models to ensure this rule is not violated. It is strongly recommended that you clearly reflect this in your code structure.

-   **Allowed Operations**:
    -   You are free to use data from other subjects or series outside the prediction target for training. For example, when predicting `subj1_series5`, you can use all data from `subj2_series6`.

## 7. Electrode Spatial Information

The fields in the data files are named according to their corresponding electrode channels. You can use the spatial relationships between electrodes to assist your model design.
