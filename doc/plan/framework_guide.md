### **Experimentation Framework Guide**

This document outlines the standardized framework for all experiments, ensuring consistency and reproducibility.

---

#### **Core Architecture: Launcher -> Engine -> Module**

Our framework separates concerns into three distinct layers:

1.  **Launcher (`run_exp.sh`)**:
    *   **Role**: The user's entry point.
    *   **Responsibilities**: Provides usage instructions, validates user input (e.g., subject ID), and executes the Python engine with those parameters.

2.  **Engine (`run_analysis.py`)**:
    *   **Role**: The experiment's central controller.
    *   **Responsibilities**: Parses arguments from the launcher, orchestrates the experimental flow (e.g., loops through subjects/channels), calls modules to perform tasks, aggregates results, and formats the final report.

3.  **Modules (`train.py`, `evaluate.py`, etc.)**:
    *   **Role**: Reusable toolkits for specific tasks.
    *   **Responsibilities**: Contain core functions (e.g., `train_model`, `evaluate_model`) that are imported and called by the engine. They handle the actual model training, evaluation, or feature engineering logic.

---

#### **Creating New Experiments**

To create a new experiment (e.g., `exp3`), simply **copy the `exp2` directory** and modify the Python scripts (`run_analysis.py`, `train.py`, etc.) to implement the new logic. The `run_exp.sh` launcher can be updated with new instructions but should otherwise remain unchanged.