# Core Scripts Framework Guide

This document aims to explain the usage and design philosophy of the core scripts located in the `mycode/scripts/` directory.

---

## 1. Core Engine: `run_analysis.py`

`run_analysis.py` is the central execution engine for the entire project. All experimental workflows, including model training, evaluation, feature engineering, and hyperparameter optimization, are orchestrated by this script.

**Directly executing this script is generally not recommended.** To ensure the reproducibility and consistency of experiments, please always use the `run_exp.sh` launcher scripts located in the various subdirectories of `mycode/experiment/` to run it indirectly.

---

## 2. Standard Analysis Mode

This mode is used to perform a complete model training and evaluation for a specified `(subject, channel, event)` combination.

### How to Use

1.  **Copy the Experiment Template**: Copy `mycode/scripts/run_exp_template.sh` to a new experiment directory (e.g., `mycode/experiment/my_new_exp/`) and rename it to `run_exp.sh`.
2.  **Configure `run_exp.sh`**:
    *   Modify the `FEATURE_EXTRACTOR` variable to specify the feature engineering method to be used (e.g., `""` for raw signal, `"filterbank"` for Filter Bank features).
3.  **Run the Experiment**:
    ```bash
    # Navigate to your experiment directory
    cd mycode/experiment/my_new_exp/

    # Run for a single target
    ./run_exp.sh 1 C3 HandStart

    # Run for all channels of all subjects
    ./run_exp.sh all all HandStart
    ```
4.  **Review the Output**:
    *   `run_exp.log`: Contains detailed execution logs.
    *   `results/`: Contains all generated charts and data.
    *   `model/`: Contains all trained model files (`.joblib`).

---

## 3. Hyperparameter Optimization Mode

This mode is specifically designed to find the optimal set of cutoff frequencies for the `Filter Bank` feature engineering. It utilizes Bayesian Optimization (`scikit-optimize`) to efficiently search the parameter space.

### How to Use

1.  **Navigate to the Dedicated Experiment Directory**: This functionality has been integrated into the `optimize_filterbank_freqs` experiment.
    ```bash
    cd mycode/experiment/optimize_filterbank_freqs/
    ```
2.  **Execute the Optimization Script**:
    The `run_exp.sh` script is pre-configured to launch the optimization mode. You just need to pass the target you wish to optimize.
    ```bash
    # Find the optimal frequencies for subject 1, channel C4, for the HandStart event
    ./run_exp.sh 1 C4 HandStart

    # Find the optimal frequencies for all channels of subject 1 for the HandStart event
    # Note: This will train and evaluate each channel independently and use the average AUC of all channels as the optimization target
    ./run_exp.sh 1 all HandStart
    ```
    *   The script defaults to 50 iterations. You can modify the `--n_calls` parameter in `run_exp.sh` to adjust this.

3.  **Review the Output**:
    *   `run_exp.log`: Details every iteration's tested frequency combination and its corresponding average AUC score.
    *   `optimization_results.txt`: After optimization is complete, this file will record the **best average AUC** found and the corresponding **optimal frequency combination**.
    *   `temp_models/`: All temporary models trained during the optimization process are stored here.
