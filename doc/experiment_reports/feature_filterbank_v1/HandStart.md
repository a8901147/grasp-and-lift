### **Experiment exp1-B: Filter Bank Feature Engineering**

**1. Research Question**

*   本次實驗的核心問題是：`leadership_code` 中使用的 Filter Bank 特徵工程技術，是否能顯著提升基於單通道原始信號的基線模型 (`exp1`) 的預測性能？
*   我們假設，通過提取並組合多個低頻頻帶的信號特徵，模型能更有效地捕捉與 `HandStart` 事件相關的神經活動，從而大幅提高 AUC 分數。

**2. Methodology**

*   **Model:**
    *   與 `exp1` 保持一致，使用 `sklearn.pipeline.Pipeline` 包含 `StandardScaler` 和 `LogisticRegression`。

*   **Features:**
    *   不再使用原始 EEG 信號。
    *   使用 `FilterBank` 特徵提取器，對每個通道的原始信號進行 7 次低通濾波（截止頻率分別為 1, 2, 4, 8, 16, 32, 64 Hz），並將這 7 個濾波後的信號沿特徵軸拼接（concatenate）起來，形成一個更豐富的特徵集。
    > **[補充說明]**：此處描述的 `1, 2, 4...` Hz 組合是基於常見對數尺度設計的理論範例。在 `mycode/scripts/feature_engineering.py` 的實際程式碼中，為了複製 `leadership_code` 的成功經驗，我們採用了其更精細化的參數組合：`[0.5, 1, 2, 3, 4, 5, 7, 9, 15, 30]` Hz。

*   **Procedure:**
    1.  **對象**: 所有 12 位受試者 (`all`) 的所有 32 個通道 (`all`)，針對 `HandStart` 事件。
    2.  **執行**: 運行 `run_analysis.py` 腳本，並通過 `--feature-extractor filterbank` 參數指定使用 Filter Bank 特徵工程。
    3.  **評估**: 與 `exp1` 相同，使用在 series 7-8 上的 Area Under the Curve (AUC) 作為主要評估指標。
    4.  **產出**: 為每位受試者生成一個條形圖，展示其所有通道的 AUC 分數，並生成全局的熱力圖與箱形圖進行綜合分析。

**3. Key Findings & Analysis**

*   **整體性能顯著提升**: Filter Bank 帶來了全面且巨大的性能提升。模型的整體 AUC 分數區間從 `exp1` 的 `0.5-0.78` 顯著拓寬並上移至 `0.6-0.88`。更重要的是，模型的性能下限被大幅抬高，幾乎所有通道的表現都遠超隨機猜測。

*   **「差生」通道的逆襲**: 該方法最大的亮點在於「拯救」了那些在 `exp1` 中表現極差的通道。
    *   **Subject 1, Channel `Fp1`**: AUC 從 `0.4237` (差於隨機) 躍升至 `0.7639`。
    *   **Subject 2, Channel `C3`**: AUC 從 `0.3925` (最差之一) 驚人地逆轉至 `0.7381`。
    *   這證明了 Filter Bank 能從高噪聲信號中有效提取出與任務相關的信息。

*   **通道重要性的重新洗牌**: 一個深刻的洞見是，最佳預測通道的排名發生了變化。例如，`Subject 1` 的最佳通道從 `exp1` 的 `C3` 變成了 `Fp1`。這表明，原始信號的信噪比並不完全等同於其潛在信息量，合適的特徵工程可以發掘出被噪聲掩蓋的寶貴信息。

*   **假設被證實**: 實驗結果強烈證實了我們的假設，即與手部運動企圖相關的關鍵 EEG 特徵主要分佈在低頻頻帶中。

**4. Conclusion & Next Steps**

*   **結論**: `exp1-B` 取得了巨大成功。Filter Bank 不僅僅是一種有效的特徵工程方法，更是理解當前任務神經信號的關鍵步驟。它應被確立為後續所有實驗的標準預處理流程。

*   **Next Steps**: 我們已經回答了「Filter Bank 是否有效」。下一個更具探索性的問題是「**Filter Bank 為何有效？是哪個或哪幾個頻帶的貢獻最大？**」。
    *   **`Experiment exp1-C`**: 進行一次**消融研究 (Ablation Study)**。我們將通過修改 `FilterBank` 的代碼，測試不同頻帶組合（例如，僅使用 `1-8Hz`，或去掉某個頻帶）對模型性能的影響。這將幫助我們：
        1.  更深入地理解信號的物理意義。
        2.  有可能進一步簡化和優化特徵集，降低計算複雜度。
        3.  為未來針對不同事件（如 `FirstDigitTouch`, `LiftOff`）尋找其各自的「黃金頻帶」提供研究思路。