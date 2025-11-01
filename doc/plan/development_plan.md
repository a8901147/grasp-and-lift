### Development Plan: An Iterative Strategy from Foundational Analysis to Advanced Models

This plan aims to progressively build a high-accuracy EEG event detection model capable of handling individual differences through a clear, iterative process.

---

### **Core Experimental Philosophy: Decoupling Feature and Model Evaluation**

To ensure the efficiency and reliability of our experiments, we adopt a **Parallel Workflow** that decouples the evaluation of "feature engineering effectiveness" from "model algorithm complexity."

**The advantages of this design are:**

1.  **Fast Baseline Establishment**: We use a simple, fast, and stable model (like **Logistic Regression**) as a "sensor" to evaluate the quality of features. This allows us to quickly determine if a feature engineering strategy is effective without waiting for the lengthy training of complex models.
2.  **Avoid Wasted Efforts**: If we directly use a complex model (like a CNN) on unverified features, it becomes difficult to ascertain whether poor results stem from the features or the model. This methodology prevents wasting significant time on model tuning with ineffective features.
3.  **Systematic Iteration**:
    *   **Feature Pipeline**: Focuses on comparing the performance of different features (raw signal, filter banks, etc.) on the same simple baseline model to prove the value of the features.
    *   **Model Pipeline**: On a fixed set of validated, effective features, we compare the performance of models with varying complexity (SVM, CNN, RNN, etc.) to measure the improvements brought by the models themselves.

**Summary: First, validate features with a simple model, then pair the best features with advanced models.** The entire development plan will adhere to this core principle.

---

#### **Phase 1: Foundational Analysis & Feature Engineering**

**Goal**: Following the core experimental philosophy, find the most effective data features and hyperparameter combinations for a single `(subject, event, channel)` model to establish a robust modeling methodology.

1.  **Baseline Establishment**
    *   **Objective**: To verify if the raw EEG signal from a single channel contains sufficient predictive information and to establish an objective benchmark for future improvements.
    *   **Corresponding Experiment**: `@doc/experiment_reports/baseline_raw_signal/`
    *   **Completed**: This phase has confirmed that even raw signals from specific channels have some predictive power for certain events.

2.  **Feature Engineering Evaluation**
    *   **Objective**: To evaluate whether the Filter Bank feature engineering technique used in the `leadership_code` can significantly improve the baseline model's performance.
    *   **Corresponding Experiment**: `@doc/experiment_reports/feature_filterbank_v1/`
    *   **Completed**: This phase has demonstrated that the Filter Bank can substantially increase the model's AUC score and should be adopted as a standard procedure for subsequent experiments.

3.  **Hyperparameter Optimization**
    *   **Objective**: To systematically find a set of cutoff frequency combinations for the Filter Bank feature extractor that is superior to the default parameters, maximizing the predictive potential of a single model.
    *   **Corresponding Experiment**: `@doc/experiment_reports/optimize_filterbank_freqs/`
    *   **In Progress**: This stage aims to find the optimal, dedicated frequencies for each individual `(subject, event, channel)` model.

**Phase Conclusion**: Upon completion of this phase, we will have a validated and optimized methodology for training any given `(subject, event, channel)` model.

---

#### **Phase 2: Generalization & Model Scaling**

**Goal**: Apply the optimal modeling method established in Phase 1 to all targets, systematically analyze model performance differences across various events and subjects, and formulate the final prediction strategy.

1.  **Event Generalization Analysis**
    *   **Process**: Select a single subject (e.g., `subj1`) and use the optimal method from Phase 1 to train models for all **6 events** separately.
    *   **Analysis**: Compare the model's performance on different events for the same subject to understand which events are inherently easier or harder to predict.

2.  **Subject Generalization Analysis**
    *   **Process**: Apply the optimal method from Phase 1 to **all 32 channels** and **all 6 events** for **all 12 subjects**.
    *   **Analysis**: Compare model performance across different subjects. If significant performance differences are observed, it confirms the necessity of creating Subject-Specific Models.

3.  **Final Strategy Formulation**
    *   **Decision**: Based on the analysis, decide on the final modeling strategy.
        *   **Strategy A (Most Likely)**: Train a dedicated set of models for each subject.
        *   **Strategy B**: If inter-subject variability is low, attempt to train a universal model applicable to all subjects.

---

#### **Phase 3: Advanced Modeling & Prediction**

**Goal**: Based on the conclusions from the first two phases, build high-performance models for final prediction and generate the submission file.

1.  **Multi-Channel Models**
    *   **Process**: Based on the analysis from Phase 2, select the top-N performing channels for each `(subject, event)` combination. Combine their features to train a multi-channel model.
    *   **Research Question**: Can combining features from multiple highly relevant channels significantly improve prediction accuracy?

2.  **Ensembling**
    *   **Process**: Attempt to combine the predictions of different models (e.g., from different channels or using different feature sets) through weighted averaging or stacking to further enhance stability and accuracy.

3.  **Prediction & Submission**
    *   **Process**: Use the final selected model to make predictions on the test set (`series9`, `series10`) and generate the `submission.csv` file in the required format.

---

#### **Phase 4: Advanced Optimization & Generalization Enhancement**

**Goal**: While pursuing peak performance, establish a rigorous validation and optimization framework to ensure the model not only excels on the known validation set but also generalizes robustly to future, unseen data, effectively controlling the risk of overfitting.

1.  **Establish a More Robust Validation Strategy**
    *   **Problem**: The current optimization approach, which relies on a fixed validation set (`series 7-8`), is at risk of overfitting to that specific dataset.
    *   **Strategy: Time Series Cross-Validation**
        *   **Implementation**: Shift the optimization objective from "maximizing AUC on a single validation set" to "maximizing the average AUC across multiple cross-validation folds." For example, the folds could be designed as follows:
            *   **Fold 1**: Train on `series 1-4`, validate on `series 5-6`
            *   **Fold 2**: Train on `series 1-6`, validate on `series 7-8`
        *   **Benefit**: This ensures that the found hyperparameters are robust across different data subsets, leading to the learning of more generalizable patterns.

2.  **Iterative Search Space Refinement**
    *   **Problem**: An overly free and complex search space (e.g., allowing an arbitrary number and type of filters) would significantly increase the risk of overfitting.
    *   **Strategy: From Simple to Complex, Constraining Model Complexity with Prior Knowledge**
        *   **Limit Frequency Range**: Based on neuroscience knowledge, constrain the frequency search upper limit to a meaningful brainwave range (e.g., 45-60 Hz) to prevent the model from fitting to high-frequency noise.
        *   **Structured Iteration**: Gradually increase the degrees of freedom in the filter design. For example, the next step could be to change the optimization target from `exp1-C`'s "10 low-pass filters" to "the upper and lower bounds of **5 independent band-pass filters**." This grants the model more flexibility while keeping the search space manageable.

3.  **Integrate Multi-Level Regularization**
    *   **Problem**: A mechanism is needed to actively "penalize" unnecessary complexity during the optimization process.
    *   **Strategy: Introduce Regularization at Both the Model and Objective Function Levels**
        *   **Model Level**: In the underlying classification model (e.g., Logistic Regression), always enable L2 regularization to penalize large model weights, reducing dependency on single features.
        *   **Objective Function Level (Advanced)**: In the Bayesian optimization objective function, introduce a penalty term for complexity. For example, `Objective = Average AUC - λ * (Number of Filters)`. This will guide the optimizer to find the best balance between "performance gain" and "model simplicity."