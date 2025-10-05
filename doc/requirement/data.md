# 數據集詳解與規則

## 1. 數據來源

本數據集的詳細描述可參見以下論文：

> Luciw MD, Jarocka E, Edin BB (2014) Multi-channel EEG recordings during 3,936 grasp and lift trials with varying weight and friction. *Scientific Data* 1:140047.
> [www.nature.com/articles/sdata201447](https://www.nature.com/articles/sdata201447)

## 2. 數據結構

-   **受試者 (Subjects)**: 共 12 位。
-   **系列 (Series)**: 每位受試者有 10 個系列（series）的試驗。
-   **試驗 (Trials)**: 每個系列約包含 30 次試驗，具體次數不定。
-   **數據劃分**:
    -   **訓練集**: 包含每位受試者的前 8 個系列 (`series1` 至 `series8`)。
    -   **測試集**: 包含每位受試者的後 2 個系列 (`series9` 和 `series10`)。

## 3. 目標事件 (Target Events)

在每一次的抓取與提起 (Grasp-and-Lift) 任務中，您需要偵測以下 6 個事件：

1.  `HandStart` (手部開始移動)
2.  `FirstDigitTouch` (手指首次接觸物體)
3.  `BothStartLoadPhase` (雙指開始共同施力)
4.  `LiftOff` (物體抬離)
5.  `Replace` (物體放回)
6.  `BothReleased` (雙指均釋放)

這些事件總是**依序發生**。

## 4. 檔案說明

對於訓練集中的每一位受試者和每一個系列，都提供了兩個對應的檔案：

-   `*_data.csv`: 包含原始的 32 通道 EEG 數據，採樣率為 **500Hz**。
-   `*_events.csv`: 包含逐幀的真實標籤 (ground truth)。

**測試集的 `*_events.csv` 檔案不被提供，需要由您來預測。**

## 5. 標籤定義 (Label Definition)

-   **ID**: 每個時間幀都有一個唯一的 `id`，由 `subject_series_frame` 拼接而成。
-   **標籤窗口**: 六個事件的標籤欄位 (`1` 或 `0`) 是根據事件是否發生在該時間幀的 **前後 150 毫秒 (ms)** 內來決定的。
    -   由於採樣率為 500Hz，這相當於 **前後 75 幀 (frames)**，總計構成一個 300ms 的窗口。
    -   一個完美的預測模型應該能對這個窗口內的所有幀都預測出機率 `1`。

---

## 6. 重要規則：禁止使用未來數據 (No Future Data)

這是本專案**最嚴格的規則**，旨在模擬真實世界的應用場景。

-   **核心原則**: 在為任何時間點 `t` 進行預測時，您的模型**絕對不能**使用 `t` 時刻之後的任何數據。
    -   **範例**: 當預測 `subj1_series9_11` 的標籤時，您不能使用來自 `subj1` `series9` 的第 11 幀**之後**的任何資訊。

-   **避免數據洩漏**:
    -   您必須非常小心以避免數據洩漏。例如，在對 `subj1_series9_11` 的信號進行標準化時，您不能使用 `subj1_series9` **整個系列**的均值或標準差。您只能使用從第 0 幀到第 10 幀的數據來計算統計量。
    -   主辦方會檢查模型以確保此規則不被違反。強烈建議您在程式碼結構上清晰地體現出這一點。

-   **允許的操作**:
    -   您可以自由使用預測目標之外的其他受試者或其他系列的數據進行訓練。例如，在預測 `subj1_series5` 時，您可以使用 `subj2_series6` 的全部數據。

## 7. 電極空間資訊

數據檔案中的欄位根據其對應的電極通道進行命名。您可以利用電極之間的空間位置關係來輔助您的模型設計。
