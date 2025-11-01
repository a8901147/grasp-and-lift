### **Experiment 1: Baseline Model with Raw EEG Signal for "BothStartLoadPhase" Event**

**1. Research Question**

This experiment aims to establish a baseline performance for event prediction using raw EEG signals without any feature engineering. The central question is: Does the unprocessed EEG signal from a single channel contain sufficient information to predict the "BothStartLoadPhase" event with an accuracy significantly better than random chance? This baseline will serve as a benchmark to evaluate the effectiveness of future feature engineering and modeling improvements.

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
        Full Channel Ranking per Subject for Event: BothStartLoadPhase
###########################################################
| Subject    | Average AUC | All Channels Sorted by AUC (Channel | AUC Score) |
|------------|-------------|----------------------------------------------------|
| subj1      | 0.5797      | CP6(0.6635) O2(0.6606) PO10(0.6499) C4(0.6495) FC6(0.6487) F8(0.6411) Oz(0.6382) CP2(0.6368) T8(0.6341) P4(0.6262) Pz(0.6236) P8(0.6189) TP9(0.6167) FC2(0.6148) TP10(0.6112) P3(0.6110) T7(0.6017) F4(0.5960) CP5(0.5925) P7(0.5866) O1(0.5694) FC5(0.5515) CP1(0.5511) Fz(0.5486) Cz(0.5200) Fp1(0.5193) FC1(0.4776) PO9(0.4742) F7(0.4667) C3(0.4618) F3(0.4581) Fp2(0.4310) |
| subj2      | 0.5484      | CP1(0.6407) P3(0.6100) Cz(0.6061) Fp1(0.5968) CP2(0.5956) P4(0.5892) P7(0.5882) CP5(0.5785) FC1(0.5758) CP6(0.5738) Pz(0.5664) Oz(0.5617) PO9(0.5603) O1(0.5578) Fp2(0.5572) TP9(0.5565) C4(0.5562) T8(0.5554) TP10(0.5509) P8(0.5370) O2(0.5368) F7(0.5341) FC2(0.5323) PO10(0.5289) F3(0.5282) FC5(0.5202) FC6(0.5198) F8(0.5140) Fz(0.4818) F4(0.4756) T7(0.4474) C3(0.4149) |
| subj3      | 0.6625      | CP5(0.7460) FC6(0.7336) T8(0.7328) CP6(0.7257) P8(0.7222) C4(0.7214) F4(0.7163) PO10(0.7158) T7(0.7085) FC5(0.7071) FC2(0.7044) F8(0.7017) P7(0.6979) F3(0.6969) C3(0.6940) P4(0.6927) PO9(0.6774) O2(0.6773) O1(0.6725) TP10(0.6609) TP9(0.6556) P3(0.6481) Fp1(0.6471) Fp2(0.6467) Oz(0.6458) CP2(0.6335) CP1(0.6138) Pz(0.5931) Fz(0.5797) FC1(0.5555) Cz(0.4996) F7(0.3759) |
| subj4      | 0.5530      | F7(0.6350) O2(0.6205) CP6(0.6084) Oz(0.6057) FC6(0.5973) P4(0.5967) CP2(0.5967) O1(0.5920) PO10(0.5875) P8(0.5783) C4(0.5777) T8(0.5765) F8(0.5700) F4(0.5639) Fp1(0.5585) TP10(0.5564) F3(0.5488) FC5(0.5473) Pz(0.5460) PO9(0.5422) P3(0.5353) P7(0.5348) Cz(0.5303) T7(0.5297) Fz(0.5270) C3(0.5115) FC2(0.5078) TP9(0.5067) CP1(0.4872) CP5(0.4843) FC1(0.4757) Fp2(0.4608) |
| subj5      | 0.5367      | FC6(0.6408) F8(0.6222) CP6(0.5968) Oz(0.5922) T8(0.5879) PO10(0.5816) P8(0.5795) O2(0.5795) O1(0.5698) F4(0.5667) C4(0.5594) Pz(0.5588) PO9(0.5562) P7(0.5427) P4(0.5421) FC2(0.5408) TP9(0.5398) TP10(0.5298) CP2(0.5292) P3(0.5217) Fp2(0.5178) Fp1(0.5109) Cz(0.5091) CP1(0.4979) FC1(0.4964) F3(0.4903) CP5(0.4879) F7(0.4802) Fz(0.4739) FC5(0.4606) C3(0.4594) T7(0.4510) |
| subj6      | 0.5278      | Fp2(0.6274) Fp1(0.6119) F4(0.6116) CP1(0.5924) Fz(0.5789) Pz(0.5722) F8(0.5668) P3(0.5612) FC6(0.5494) C3(0.5470) FC1(0.5465) Oz(0.5381) F3(0.5377) PO9(0.5293) F7(0.5224) FC5(0.5201) CP5(0.5194) FC2(0.5156) TP9(0.5088) TP10(0.5053) C4(0.5052) T8(0.5042) CP6(0.5036) P8(0.5009) P7(0.5008) PO10(0.5002) T7(0.4871) Cz(0.4766) O1(0.4662) O2(0.4649) P4(0.4619) CP2(0.4562) |
| subj7      | 0.5907      | O2(0.6962) C4(0.6726) FC2(0.6674) F8(0.6674) FC6(0.6658) P4(0.6637) T8(0.6609) P8(0.6594) TP10(0.6553) PO10(0.6548) Oz(0.6522) CP2(0.6305) P3(0.6242) Fp2(0.6137) O1(0.5989) PO9(0.5981) CP6(0.5893) F4(0.5874) P7(0.5868) Pz(0.5867) F7(0.5727) TP9(0.5664) CP1(0.5560) FC1(0.5517) Fz(0.5309) Fp1(0.5104) FC5(0.5046) C3(0.5026) Cz(0.4993) F3(0.4903) CP5(0.4525) T7(0.4336) |
| subj8      | 0.5385      | Fp1(0.6654) Fp2(0.6646) P7(0.6052) TP10(0.6016) CP1(0.5850) C3(0.5743) PO9(0.5725) P3(0.5713) FC6(0.5676) F4(0.5617) Fz(0.5571) P8(0.5562) TP9(0.5546) Pz(0.5464) FC2(0.5462) CP5(0.5461) F3(0.5452) Cz(0.5418) FC5(0.5169) F7(0.5124) PO10(0.5095) F8(0.5087) P4(0.5071) O2(0.5031) T8(0.4931) T7(0.4909) Oz(0.4853) CP6(0.4809) FC1(0.4774) O1(0.4655) C4(0.4595) CP2(0.4590) |
| subj9      | 0.5432      | C3(0.6370) TP9(0.6053) Fp2(0.6034) T7(0.5993) CP5(0.5980) P7(0.5838) PO9(0.5788) P3(0.5786) FC1(0.5760) FC5(0.5736) F7(0.5681) O1(0.5679) F8(0.5635) F4(0.5581) Oz(0.5581) FC6(0.5528) PO10(0.5472) TP10(0.5409) Pz(0.5284) Cz(0.5195) T8(0.5151) P8(0.5110) CP2(0.5099) F3(0.5071) CP6(0.5040) Fz(0.4964) P4(0.4913) C4(0.4895) O2(0.4855) FC2(0.4820) CP1(0.4804) Fp1(0.4704) |
| subj10     | 0.5873      | C4(0.7362) Fp1(0.6983) F8(0.6831) F7(0.6822) FC6(0.6633) FC2(0.6454) T8(0.6219) F4(0.6196) O1(0.6125) P3(0.6079) Pz(0.6035) Oz(0.5995) CP2(0.5976) FC5(0.5936) O2(0.5900) P8(0.5868) CP6(0.5862) F3(0.5810) TP10(0.5686) PO9(0.5555) P4(0.5553) CP1(0.5544) FC1(0.5526) Fp2(0.5518) Fz(0.5511) P7(0.5421) C3(0.5364) PO10(0.5325) Cz(0.5162) TP9(0.5157) CP5(0.4920) T7(0.4604) |
| subj11     | 0.5356      | FC1(0.6657) Fz(0.6452) CP5(0.6381) P3(0.6328) C4(0.5923) CP1(0.5914) P4(0.5898) F8(0.5848) FC2(0.5832) Fp2(0.5760) Cz(0.5703) F4(0.5627) F3(0.5412) O2(0.5387) CP6(0.5333) Fp1(0.5262) TP9(0.5246) CP2(0.5245) F7(0.5098) Oz(0.5069) TP10(0.5004) T8(0.4971) FC5(0.4908) Pz(0.4889) PO10(0.4838) O1(0.4812) PO9(0.4721) P8(0.4683) C3(0.4643) T7(0.4625) P7(0.4462) FC6(0.4459) |
| subj12     | 0.5129      | CP1(0.5577) P4(0.5445) C3(0.5433) O2(0.5379) P3(0.5369) Oz(0.5357) CP2(0.5337) P8(0.5307) Cz(0.5286) C4(0.5270) F3(0.5259) Pz(0.5239) CP6(0.5200) O1(0.5171) CP5(0.5164) PO10(0.5162) Fp1(0.5157) TP10(0.5119) FC1(0.5087) FC6(0.5073) FC5(0.5024) T8(0.4985) FC2(0.4969) F7(0.4955) F4(0.4943) P7(0.4941) F8(0.4926) PO9(0.4882) Fp2(0.4882) T7(0.4806) TP9(0.4789) Fz(0.4647) |
###########################################################

Similar to other events, the performance of the baseline model on "BothStartLoadPhase" is modest. Most subjects' average AUC scores are above 0.5, confirming the presence of some predictive signal. Subject 3 stands out with a significantly higher AUC, indicating that for this individual, the raw signal is more informative for this specific event.

**4. Conclusion & Next Steps**

A performance baseline for the "BothStartLoadPhase" event has been established. The results reinforce the conclusion from other baseline experiments: raw EEG signals alone are insufficient for building a high-performance, generalizable model.

The next step is to proceed with the **feature_filterbank_v1** experiment. This will involve applying filter bank feature extraction to the signals before training the models, with the hypothesis that this will lead to a significant improvement in AUC scores across all subjects.