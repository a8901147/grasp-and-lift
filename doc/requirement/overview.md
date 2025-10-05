# 專案概述與評估標準

## 1. 專案目標

想像一下，如果沒有雙手，我們將如何完成早晨起床、穿衣、刷牙、泡咖啡等一系列日常活動。對於因截肢或神經系統疾病而失去手部功能的患者來說，這就是他們每天面臨的現實。

本專案的最終目標是推動**腦機介面 (Brain-Computer Interface, BCI)** 技術的發展，以開發出能夠讓患者透過大腦活動直接控制的義肢設備。這將極大地提升他們的獨立生活能力與生活品質。

## 2. 挑戰任務

EEG (腦電圖) 信號是頭皮上記錄到的大腦活動電信號，但其與大腦活動之間的關係非常複雜。本次競賽的核心挑戰是：

> **利用健康受試者在執行「抓取、提起、放回」物體等一系列動作時所記錄的 EEG 數據，準確識別出其手部正處於哪個特定事件階段。**

透過更好地理解 EEG 信號與手部運動之間的關係，我們才能為開發出更可靠、低風險且非侵入性的 BCI 設備奠定基礎。

## 3. 評估指標 (Evaluation Metric)

提交結果將使用 **平均欄位 AUC (Mean Column-wise AUC)** 進行評估。

具體來說，評估系統會計算您預測的**每一個事件欄位**（如 `HandStart`, `FirstDigitTouch` 等）各自的 ROC 曲線下面積 (Area Under the ROC Curve)，然後將所有欄位的 AUC 分數取平均值。

由於預測涵蓋多位受試者和多個系列，您提交的機率值應該經過校準，以確保它們在一個統一的尺度上。

## 4. 提交檔案格式 (Submission File Format)

您必須為測試集中的每一個 `id`（對應一個時間幀）預測六個事件的發生機率。`id` 由 `subject_series_frame` 拼接而成。

提交的 `.csv` 檔案必須包含一個標頭，並遵循以下格式：

```csv
id,HandStart,FirstDigitTouch,BothStartLoadPhase,LiftOff,Replace,BothReleased
subj1_series9_0,0,0,0,0,0,0
subj1_series9_1,0,0,0,0,0,0
subj1_series9_2,0,0,0,0,0,0
...
```

## 5. 致謝 (Acknowledgements)

本次競賽由 **WAY Consortium** (Wearable interfaces for hAnd function recoverY; FP7-ICT-288551) 贊助。
