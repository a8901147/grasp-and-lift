# 核心腳本框架說明

本文檔旨在說明 `mycode/scripts/` 目錄下核心腳本的使用方法與設計理念。

---

## 1. 核心引擎：`run_analysis.py`

`run_analysis.py` 是整個專案的中央執行引擎。所有的實驗流程，包括模型訓練、評估、特徵工程以及超參數最佳化，都是由這個腳本統一調度的。

**直接執行此腳本通常不是推薦的做法。** 為了確保實驗的可重複性與一致性，請一律使用位於 `mycode/experiment/` 各個子目錄下的 `run_exp1.sh` 啟動腳本來間接執行它。

---

## 2. 標準分析模式

此模式用於對指定的 `(個體, 通道, 事件)` 組合進行一次完整的模型訓練與評估。

### 如何使用

1.  **複製實驗模板**: 從 `mycode/scripts/run_exp2_template.sh` 複製一份到新的實驗目錄（例如 `mycode/experiment/my_new_exp/`），並將其命名為 `run_exp2.sh`。
2.  **配置 `run_exp.sh`**:
    *   修改 `FEATURE_EXTRACTOR` 變數來指定要使用的特徵工程方法（例如 `""` 代表原始信號，`"filterbank"` 代表 Filter Bank 特徵）。
3.  **執行實驗**:
    ```bash
    # 進入你的實驗目錄
    cd mycode/experiment/my_new_exp/

    # 執行單一目標
    ./run_exp.sh 1 C3 HandStart

    # 執行所有個體的所有通道
    ./run_exp.sh all all HandStart
    ```
4.  **查看產出**:
    *   `run_exp.log`: 包含詳細的執行日誌。
    *   `results/`: 包含所有產出的圖表與數據。
    *   `model/`: 包含所有訓練好的模型檔案 (`.joblib`)。

---

## 3. 超參數最佳化模式

此模式專門用於為 `Filter Bank` 特徵工程尋找一組最佳的截止頻率組合。它利用貝葉斯優化 (`scikit-optimize`) 來高效地搜索參數空間。

### 如何使用

1.  **進入專屬實驗目錄**: 此功能已經被整合到 `optimize_filterbank_freqs` 實驗中。
    ```bash
    cd mycode/experiment/optimize_filterbank_freqs/
    ```
2.  **執行優化腳本**:
    `run_exp.sh` 腳本已經被預先配置為啟動優化模式。你只需要傳入想優化的目標即可。
    ```bash
    # 為 subject 1 的 C4 通道尋找 HandStart 事件的最佳頻率
    ./run_exp.sh 1 C4 HandStart

    # 為 subject 1 的所有通道尋找 HandStart 事件的最佳頻率
    # 注意：這會為每一個通道獨立訓練與評估，並使用所有通道的平均 AUC 作為優化目標
    ./run_exp.sh 1 all HandStart
    ```
    *   腳本預設會執行 50 次迭代，你可以在 `run_exp.sh` 中修改 `--n_calls` 參數來調整。

3.  **查看產出**:
    *   `run_exp.log`: 詳細記錄了每一次迭代測試的頻率組合與其對應的平均 AUC 分數。
    *   `optimization_results.txt`: 優化完成後，此檔案會記錄下找到的**最佳平均 AUC**以及對應的**最佳頻率組合**。
    *   `temp_models/`: 在優化過程中，所有被訓練的暫時性模型都會存放在此。
