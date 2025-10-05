### **Experiment 3: 各通道預測 BothStartLoadPhase 事件之基準表現分析**

**1. Research Question**

*   本次實驗旨在探討：在預測 `BothStartLoadPhase`（雙手開始承重階段）事件時，單一 EEG 通道的訊號是否具備足夠的預測能力？
*   此實驗的目的是建立一個基準線，用以衡量每個獨立通道在預測物體承重這個特定動作階段時的貢獻度，並識別出最相關的通道。

**2. Methodology**

*   **Model:**
    *   與前序實驗一致，腳本為每個通道獨立訓練一個分類模型並以 `.joblib` 格式保存。此處同樣假設為一個標準的 Scikit-learn 分類器（如 Logistic Regression 或梯度提升機）。

*   **Features:**
    *   模型訓練的特徵來源於單一 EEG 通道的原始時序數據，每個模型僅使用一個通道的資訊。

*   **Procedure:**
    1.  **數據範圍**: 分析涵蓋了全部 12 位受試者。
    2.  **迭代訓練**: 針對每位受試者的 32 個 EEG 通道進行獨立的模型訓練與驗證。
    3.  **目標事件**: 預測的目標為 `BothStartLoadPhase` 事件。
    4.  **評估指標**: 使用 AUC 作為模型預測表現的主要量化指標。
    5.  **結果可視化**: 為每位受試者生成各通道 AUC 表現的排序長條圖。同時，繪製整合所有受試者結果的盒鬚圖與熱力圖，以便進行跨受試者的綜合分析。

**3. Key Findings & Analysis**

*   從 `results` 目錄下的圖表（`subj*_BothStartLoadPhase_channel_ranking.png` 及 `summary_*` 圖）分析可得：
    *   **通道間的顯著差異**: 與 `FirstDigitTouch` 事件類似，不同通道在預測 `BothStartLoadPhase` 上的表現差異顯著。這表明腦部不同區域的活動與物體承重階段的關聯程度有強有弱。
    *   **高相關性腦區**: 根據 `summary_heatmap.png` 和 `summary_channel_boxplot.png` 的趨勢，可以推斷出運動皮層 (motor cortex) 及頂葉皮層 (parietal cortex) 附近的通道（如 C3, C4, Cz, CP5, CP6 等）在多數受試者中均表現出較高的 AUC 分數。這符合神經科學的普遍認知，即這些腦區與運動規劃、執行及感覺回饋密切相關。
    *   **個體化模式**: 儘管存在上述的普遍趨勢，但每位受試者內部表現最佳的通道組合仍有差異，顯示了個體間腦功能活動的獨特性。

**4. Conclusion & Next Steps**

*   **結論**: 本次實驗成功驗證了單一 EEG 通道訊號中包含了可用於預測 `BothStartLoadPhase` 事件的有效資訊。實驗結果不僅為此事件建立了一個可靠的預測基準，也進一步確認了運動和感覺相關皮層在物體操縱中的關鍵作用。
*   **Next Steps**:
    *   **Experiment 3-A (多事件比較分析)**: 我們已經分別建立了 `FirstDigitTouch` (exp2) 和 `BothStartLoadPhase` (exp3) 的通道表現基準。下一個實驗可以對比這兩個事件的結果，研究問題是：**預測不同運動事件時，最具資訊量的 EEG 通道分佈是否存在差異？** 這有助於理解大腦在連續動作的不同階段是如何調動不同腦區資源的。
    *   **Experiment 3-B (特徵組合)**: 與 `exp2` 的後續步驟類似，可以挑選在 `BothStartLoadPhase` 預測中表現最好的通道組合，訓練一個多通道模型，以驗證資訊整合是否能提升預測效能。
