# EEG 分析腳本使用指南

## 概覽

本目錄包含用於 EEG 訊號分析、模型訓練、評估與超參數最佳化的核心 Python 腳本。主要的分析流程可以透過 `run_analysis.py` 來驅動。

## 主要腳本說明

-   `run_analysis.py`: **(主要使用)** 用於執行完整的分析流程，包括訓練、評估，並產生所有 channels 的 AUC 分數排名圖表與總結圖表。
-   `train.py`: 用於訓練單一 subject、單一 channel、單一 event 的模型。
-   `evaluate.py`: 用於評估一個已訓練好的模型。
-   `search_hyperparameters.py`: 用於執行貝氏最佳化，尋找 Filterbank 特徵提取器的最佳截止頻率組合。通常由 `@mycode/experiment/optimize_filterbank_freqs/run_optimization.sh` 呼叫。

---

## 主要分析流程: `run_analysis.py`

這是執行分析最主要的腳本。它會自動化處理多個 subjects 和 channels 的訓練與評估。

### 基本語法

```bash
python run_analysis.py <subject> <channel> <event> [OPTIONS]
```

### 必要參數

-   `<subject>`: Subject ID。可以是單一 ID (例如 `1`)、多個 ID (例如 `'1,2,5'`)、一個範圍 (例如 `'1-8'`) 或 `all` (代表所有 12 位 subjects)。
-   `<channel>`: Channel 名稱。可以是單一 channel (例如 `C3`) 或 `all` (代表所有 32 個 channels)。
-   `<event>`: 事件名稱 (例如 `HandStart`, `LiftOff` 等)。

### 重要可選參數

-   `--feature-extractor <name>`: 指定要使用的特徵提取器。
    -   `filterbank`: 使用 Filterbank 進行特徵工程。
    -   若不指定，則直接使用原始訊號進行訓練。
-   `--filterbank-freqs "<freqs>"`: **(僅在 `--feature-extractor filterbank` 時有效)**
    -   提供一組自訂的 Filterbank 截止頻率。
    -   頻率必須是一個用逗號分隔的字串，例如 `'0.5,1,2,4,8,15,30'`。
    -   若使用 `filterbank` 但不提供此參數，腳本會使用內建的預設頻率。

### 使用範例

1.  **基本分析 (原始訊號):**
    -   對 Subject 1 的所有 channels 進行 `HandStart` 事件的分析。
    ```bash
    python run_analysis.py 1 all HandStart
    ```

2.  **使用預設 Filterbank:**
    -   對 Subject 1-3 的 `C3` channel 進行 `LiftOff` 事件的分析，並啟用預設的 Filterbank。
    ```bash
    python run_analysis.py 1-3 C3 LiftOff --feature-extractor filterbank
    ```

3.  **使用自訂 Filterbank 頻率:**
    -   對所有 subjects 的所有 channels 進行 `HandStart` 事件的分析，並使用一組自訂的截止頻率。
    ```bash
    python run_analysis.py all all HandStart --feature-extractor filterbank --filterbank-freqs "0.1,1,3,5,7,10,14,20,28,38"
    ```
    *(提示: 這組頻率可能是透過最佳化腳本找到的)*

---

## 實驗管理與日誌紀錄 (`run_exp_template.sh`)

當你需要進行一系列正式的、可追蹤的實驗時，建議使用 `run_exp_template.sh` 來執行分析。這是一個包裝腳本，提供了標準化的實驗流程。

### 為何使用此樣板？

-   **自動化日誌**: 腳本會自動將所有螢幕輸出（包括進度、結果與錯誤訊息）儲存到一個 `run_exp.log` 檔案中，方便日後追蹤與除錯。
-   **結構化輸出**: 它會將每次實驗的結果（圖表、模型、日誌）都存放在一個獨立的目錄中，避免與其他實驗結果混淆，有利於版本控制與結果比較。
-   **可重複性**: 透過複製此樣板來建立新的實驗，可以確保每次執行的環境與流程都是一致的。

### 如何使用

`run_exp_template.sh` 的主要用途是作為一個樣板。一個標準的流程如下：

1.  **複製樣板**: 在 `@mycode/experiment/` 目錄下，為你的新實驗建立一個資料夾 (例如 `my_first_exp`)。
2.  **貼上並改名**: 將 `mycode/scripts/run_exp_template.sh` 複製到你新建立的資料夾中，並將其改名為 `run_exp.sh`。
3.  **修改腳本 (可選)**: 你可以直接在新的 `run_exp.sh` 中修改參數，例如預設的 `--feature-extractor` 或加上 `--filterbank-freqs`。
4.  **執行實驗**: 在你的實驗資料夾中執行腳本。所有參數都會被傳遞給 `run_analysis.py`。

```bash
# 假設你已經在 mycode/experiment/my_first_exp/ 中
bash run_exp.sh <subject> <channel> <event> [ADDITIONAL_OPTIONS]
```

### 使用範例

假設你已經按照上述步驟建立了 `mycode/experiment/feature_filterbank_v2/`，並準備好 `run_exp.sh`。

-   **執行一個使用自訂 Filterbank 的實驗:**
    ```bash
    # 位於 mycode/experiment/feature_filterbank_v2/
    bash run_exp.sh all all HandStart --feature-extractor filterbank --filterbank-freqs "0.1,1,3,5,7,10,14,20,28,38"
    ```

### 輸出結果

使用此樣板執行的所有輸出，都會被完整地存放在該實驗的資料夾內，例如：

`mycode/experiment/feature_filterbank_v2/`
-   `run_exp.log`: 完整的執行日誌。
-   `results/`: 存放所有 AUC 分數圖表 (.png)。
-   `model/`: 存放每個 channel 訓練好的模型檔案 (.joblib)。

這與直接執行 `run_analysis.py` 將結果放在根目錄的 `out/` 資料夾不同，提供了更好的實驗隔離性。

---

## 超參數最佳化流程

如果你想找到最佳的 Filterbank 截止頻率，而不是手動指定，你可以使用最佳化腳本。

1.  **執行最佳化:**
    -   切換到實驗目錄並執行 `run_optimization.sh`。
    -   這個腳本會呼叫 `search_hyperparameters.py` 來尋找最佳參數組合。
    ```bash
    # 位於 mycode/experiment/optimize_filterbank_freqs/
    ./run_optimization.sh <subject> <channel> <event>
    ```
    -   例如，對所有 subjects 執行最佳化：
    ```bash
    ./run_optimization.sh all all HandStart
    ```

2.  **套用最佳化結果:**
    -   最佳化完成後，會在 `mycode/experiment/optimize_filterbank_freqs/` 目錄下產生一個 `optimization_results.txt` 檔案。
    -   你可以將檔案中找到的 "Best Frequency Combination" 複製出來，並透過 `--filterbank-freqs` 參數應用到你的 `run_analysis.py` 流程中，如上面的範例 3 所示。

---

## 輸出結果

所有執行 `run_analysis.py` 產生的結果 (圖表、模型) 都會被儲存在根目錄的 `out/` 資料夾下，並根據你的執行參數自動建立一個唯一的子目錄，例如：

`out/subj-1-3_chan-C3_evt-LiftOff_filterbank/`

-   `results/`: 存放所有 AUC 分數圖表 (.png)。
-   `model/`: 存放每個 channel 訓練好的模型檔案 (.joblib)。
