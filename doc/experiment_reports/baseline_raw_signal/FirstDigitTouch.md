### **Experiment 1: Baseline Model with Raw EEG Signal for "FirstDigitTouch" Event**

**1. Research Question**

This experiment aims to establish a baseline performance for event prediction using raw EEG signals without any feature engineering. The central question is: Does the unprocessed EEG signal from a single channel contain sufficient information to predict the "FirstDigitTouch" event with an accuracy significantly better than random chance? This baseline will serve as a benchmark to evaluate the effectiveness of future feature engineering and modeling improvements.

**2. Methodology**

*   **Model:**
    *   Logistic Regression. This model was chosen for its simplicity and efficiency as a baseline classifier. It is configured with balanced class weights to handle imbalanced data.

*   **Features:**
    *   Raw EEG signal data from a single channel at a time. No transformations or feature extraction methods were applied.

*   **Procedure:**
    1.  **Data Splitting:** For each subject, data from series 1-6 were used for training, and series 7-8 were used for validation.
    2.  **Training:** A separate model was trained for each of the 32 EEG channels for each of the 12 subjects. The training process involved a pipeline that first standardized the data using `StandardScaler` and then fed it to the `LogisticRegression` classifier.
    3.  **Evaluation:** The performance of each model was evaluated using the Area Under the Receiver Operating Characteristic Curve (AUC). An average AUC score was then calculated across all 32 channels for each subject to provide a summary of overall performance.

**3. Key Findings & Analysis**

The experiment was executed for all 12 subjects across all 32 channels. The average AUC scores for each subject are summarized below:

###########################################################
        Full Channel Ranking per Subject for Event: FirstDigitTouch
###########################################################
| Subject    | Average AUC | All Channels Sorted by AUC (Channel | AUC Score) |
|------------|-------------|----------------------------------------------------|
| subj1      | 0.5905      | CP6(0.6642) O2(0.6632) Oz(0.6437) C4(0.6433) PO10(0.6429) CP2(0.6408) FC6(0.6377) Pz(0.6354) T8(0.6341) P4(0.6324) F8(0.6214) P3(0.6207) P8(0.6193) TP9(0.6168) T7(0.6164) FC2(0.6118) TP10(0.6111) CP5(0.5992) P7(0.5908) F4(0.5856) O1(0.5718) CP1(0.5644) FC5(0.5632) Fp1(0.5567) F7(0.5553) C3(0.5431) Fz(0.5354) Cz(0.5338) PO9(0.5296) Fp2(0.4809) FC1(0.4699) F3(0.4597) |
| subj2      | 0.5980      | Fp1(0.7872) Fp2(0.7851) CP1(0.6807) Cz(0.6749) T7(0.6610) P7(0.6607) TP9(0.6552) FC1(0.6477) CP5(0.6414) P3(0.6406) CP2(0.6388) PO9(0.6354) P4(0.6229) TP10(0.6190) CP6(0.6117) FC5(0.6095) O1(0.6063) Oz(0.6024) T8(0.5992) PO10(0.5957) C4(0.5821) P8(0.5819) Pz(0.5816) O2(0.5699) FC2(0.5631) FC6(0.5358) F3(0.5320) F8(0.4889) F7(0.4737) Fz(0.4647) F4(0.4277) C3(0.3594) |
| subj3      | 0.6590      | CP5(0.7417) FC6(0.7326) T8(0.7266) F4(0.7220) P8(0.7198) CP6(0.7173) PO10(0.7138) T7(0.7111) C4(0.7099) FC5(0.7058) F8(0.7044) FC2(0.7015) F3(0.6976) P7(0.6943) P4(0.6826) C3(0.6799) O2(0.6758) PO9(0.6741) O1(0.6683) TP10(0.6616) TP9(0.6540) Fp1(0.6490) Fp2(0.6463) Oz(0.6453) P3(0.6428) CP2(0.6086) CP1(0.5982) Pz(0.5832) Fz(0.5811) FC1(0.5504) Cz(0.5190) F7(0.3710) |
| subj4      | 0.5721      | F7(0.6453) Oz(0.6408) O2(0.6403) Fp1(0.6313) O1(0.6254) CP2(0.6251) P4(0.6243) CP6(0.6241) Fp2(0.6089) FC6(0.6037) C4(0.5930) PO10(0.5923) T8(0.5867) P8(0.5822) P3(0.5796) Pz(0.5769) TP10(0.5674) P7(0.5673) F8(0.5644) PO9(0.5584) Fz(0.5570) Cz(0.5565) F3(0.5521) C3(0.5364) F4(0.5355) CP1(0.5310) TP9(0.5303) CP5(0.5177) FC2(0.5020) T7(0.4945) FC1(0.4878) FC5(0.4684) |
| subj5      | 0.5332      | FC6(0.6331) F8(0.6139) Oz(0.5908) CP6(0.5851) T8(0.5840) O2(0.5745) O1(0.5725) PO10(0.5722) P8(0.5701) F4(0.5613) PO9(0.5538) Pz(0.5477) C4(0.5465) P7(0.5415) FC2(0.5381) TP9(0.5360) P4(0.5348) TP10(0.5279) Fp1(0.5204) P3(0.5138) CP2(0.5135) Cz(0.5118) Fp2(0.5073) CP1(0.5071) FC1(0.4984) CP5(0.4936) F3(0.4918) F7(0.4780) Fz(0.4689) C3(0.4637) FC5(0.4592) T7(0.4518) |
| subj6      | 0.5219      | Fp2(0.6267) Fp1(0.6134) F4(0.6074) CP1(0.6073) Pz(0.5955) Fz(0.5871) P3(0.5842) F8(0.5639) Oz(0.5632) C3(0.5492) F3(0.5449) FC6(0.5399) FC1(0.5387) CP5(0.5303) TP10(0.5205) TP9(0.5164) P7(0.5156) FC5(0.5136) F7(0.5097) FC2(0.5066) PO9(0.5022) T8(0.4870) T7(0.4845) CP6(0.4743) C4(0.4740) P8(0.4728) PO10(0.4716) Cz(0.4687) O2(0.4396) O1(0.4365) P4(0.4313) CP2(0.4249) |
| subj7      | 0.5864      | O2(0.6865) FC6(0.6752) F8(0.6680) FC2(0.6668) PO10(0.6576) C4(0.6575) P8(0.6536) P4(0.6488) T8(0.6457) TP10(0.6382) Oz(0.6367) P3(0.6057) CP2(0.6041) F4(0.5978) Fp2(0.5956) O1(0.5868) PO9(0.5854) F7(0.5814) P7(0.5766) T7(0.5696) CP6(0.5687) Pz(0.5596) TP9(0.5513) FC1(0.5377) CP1(0.5353) Fz(0.5294) Fp1(0.5022) C3(0.4974) FC5(0.4970) F3(0.4952) Cz(0.4913) CP5(0.4613) |
| subj8      | 0.5395      | Fp2(0.6434) Fp1(0.6272) P7(0.6095) TP10(0.5910) CP1(0.5864) C3(0.5807) FC6(0.5774) PO9(0.5729) P3(0.5709) F4(0.5633) TP9(0.5573) P8(0.5551) FC2(0.5539) CP5(0.5502) Fz(0.5469) Pz(0.5433) Cz(0.5399) F3(0.5285) F7(0.5251) F8(0.5251) FC5(0.5248) CP6(0.5175) PO10(0.5109) T8(0.5056) P4(0.5033) O2(0.5031) T7(0.4911) Oz(0.4893) FC1(0.4796) O1(0.4726) C4(0.4608) CP2(0.4576) |
| subj9      | 0.5266      | C3(0.6226) F7(0.5795) FC1(0.5761) TP9(0.5737) CP5(0.5724) T7(0.5698) FC5(0.5637) P3(0.5539) PO9(0.5519) F8(0.5496) FC6(0.5491) P7(0.5487) F4(0.5390) O1(0.5368) Oz(0.5343) PO10(0.5255) Fp1(0.5200) F3(0.5161) TP10(0.5110) Pz(0.5105) Cz(0.5031) T8(0.5008) P8(0.4983) O2(0.4960) CP2(0.4948) P4(0.4894) CP1(0.4890) C4(0.4880) CP6(0.4838) FC2(0.4804) Fz(0.4730) Fp2(0.4501) |
| subj10     | 0.6017      | Fp1(0.7501) C4(0.7414) F7(0.6853) F8(0.6704) FC6(0.6584) FC2(0.6431) O1(0.6354) T8(0.6302) Oz(0.6263) Pz(0.6249) Fp2(0.6239) P3(0.6236) CP2(0.6166) O2(0.6086) F3(0.6065) F4(0.6034) P8(0.5934) CP6(0.5930) FC5(0.5880) TP10(0.5857) PO9(0.5770) CP1(0.5730) Fz(0.5714) P4(0.5697) P7(0.5618) FC1(0.5481) PO10(0.5427) TP9(0.5423) C3(0.5419) Cz(0.5289) CP5(0.5079) T7(0.4809) |
| subj11     | 0.5293      | FC1(0.6560) CP5(0.6481) P3(0.6320) Fz(0.6246) C4(0.5886) CP1(0.5867) P4(0.5836) F8(0.5836) FC2(0.5809) Cz(0.5537) C3(0.5403) F4(0.5379) CP6(0.5338) O2(0.5325) F3(0.5235) CP2(0.5157) TP9(0.5150) F7(0.5111) Fp2(0.5085) Oz(0.5045) TP10(0.4949) T8(0.4949) Pz(0.4870) FC5(0.4826) PO10(0.4813) Fp1(0.4777) O1(0.4733) P8(0.4712) PO9(0.4661) T7(0.4545) FC6(0.4537) P7(0.4394) |
| subj12     | 0.4998      | F3(0.5324) Fp1(0.5280) O2(0.5263) CP1(0.5231) Oz(0.5222) Cz(0.5201) C3(0.5180) P4(0.5144) P8(0.5137) F7(0.5128) PO10(0.5126) FC5(0.5104) TP10(0.5066) CP2(0.5027) CP5(0.5014) FC6(0.5012) CP6(0.4957) T8(0.4956) P3(0.4956) C4(0.4950) Pz(0.4929) O1(0.4924) T7(0.4917) FC1(0.4886) F8(0.4885) FC2(0.4828) TP9(0.4810) PO9(0.4785) P7(0.4782) Fp2(0.4781) F4(0.4716) Fz(0.4410) |
###########################################################

The results show a wide range of performance across subjects. While some subjects (e.g., Subject 3) achieve a respectable average AUC, others are much closer to the random-chance baseline of 0.5. This variability suggests that the raw signal's predictive power for "FirstDigitTouch" is highly subject-dependent.

**4. Conclusion & Next Steps**

This experiment successfully established a baseline for the "FirstDigitTouch" event. The conclusion is that raw EEG signals alone are not reliable for creating a generalized model, although they do contain some predictive information for certain individuals.

The clear next step is to apply feature engineering to determine if a more sophisticated representation of the signal can improve performance and reduce the variability between subjects. The subsequent experiment, **feature_filterbank_v1**, will address this by using a filter bank to extract frequency-based features.