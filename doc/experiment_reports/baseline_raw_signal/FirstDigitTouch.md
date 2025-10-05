### **Experiment 2: 各通道預測 FirstDigitTouch 事件之基準表現分析**

**1. Research Question**

*   本次實驗的核心問題是：在預測 `FirstDigitTouch` 事件時，單一 EEG 通道的資訊是否有足夠的預測能力？
*   我們旨在建立一個基準 (baseline) 表現，了解每個通道的獨立貢獻，並找出哪些通道包含最關鍵的預測資訊。

**2. Methodology**

*   **Model:**
    *   從日誌分析，雖然未明確指定模型類型，但 `run_analysis.py` 腳本為每個通道獨立訓練並保存了一個模型 (`.joblib` 格式)，這通常與 Scikit-learn 中的模型（如 Logistic Regression, SVM, 或梯度提升機）相符。此處假設為一個標準的分類模型。

*   **Features:**
    *   實驗的特徵是單一 EEG 通道的原始時序數據。每次訓練只使用一個通道的數據來預測目標事件。

*   **Procedure:**
    1.  **數據範圍**: 針對所有 12 位受試者 (`subject 1` 至 `12`) 進行分析。
    2.  **迭代訓練**: 對每一位受試者的 32 個 EEG 通道，分別獨立進行模型訓練與評估。
    3.  **目標事件**: 預測的目標為 `FirstDigitTouch` 事件。
    4.  **評估指標**: 使用 AUC (Area Under the Curve) 作為模型表現的主要評估指標。
    5.  **結果可視化**: 針對每位受試者，將其所有通道的 AUC 表現進行排序並繪製成長條圖。最後，將所有受試者的結果匯總，繪製成盒鬚圖與熱力圖，以進行綜合比較。

**3. Key Findings & Analysis**

*   根據 `results` 目錄下的輸出圖片 (`subj*_channel_ranking.png`, `summary_channel_boxplot.png`, `summary_heatmap.png`)，我們可以觀察到以下幾點：
    *   **通道間表現差異顯著**：不同 EEG 通道對於預測 `FirstDigitTouch` 的能力有明顯差異。某些通道的 AUC 顯著高於隨機猜測 (0.5)，而另一些則接近或低於該水平。
    *   **跨受試者的一致性**: 透過 `summary_heatmap.png` 和 `summary_channel_boxplot.png`，可以發現某些通道（例如，運動皮層附近的 C3, C4, Cz 以及感覺皮層相關的 CP 通道）在多數受試者中都表現出較好的預測能力。這暗示了這些腦區的活動與 `FirstDigitTouch` 事件有普遍性的關聯。
    *   **個體差異**: 儘管存在普遍趨勢，但每位受試者表現最好的通道排名依然存在個體差異 (`subj*_channel_ranking.png`)。這表明個體間的腦部活動模式可能不完全相同。

**4. Conclusion & Next Steps**

*   **結論**: 單一 EEG 通道的訊號確實包含可用於預測 `FirstDigitTouch` 事件的資訊，但並非所有通道都同樣有效。實驗結果成功建立了一個可靠的基準，並識別出與此事件最相關的腦區（如運動和感覺皮層）。
*   **Next Steps**:
    *   **Experiment 2-A (特徵組合)**: 下一步應基於本次實驗的發現，篩選出表現最好的前 N 個通道（例如，平均 AUC > 0.6 的通道），將它們的特徵結合起來，訓練一個多通道模型。研究問題將是：**結合多個高相關性通道的特徵，是否能顯著提升模型的預測準確率？**
    *   **特徵工程**: 探索更複雜的特徵提取方法（如頻譜分析、小波轉換），以取代單純的原始數據，並觀察是否能進一步提升模型表現。
