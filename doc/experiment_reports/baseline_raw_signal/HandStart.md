### **Experiment 1: Baseline Model with Raw EEG Signal for "HandStart" Event**

**1. Research Question**

This experiment aims to establish a baseline performance for event prediction using raw EEG signals without any feature engineering. The central question is: Does the unprocessed EEG signal from a single channel contain sufficient information to predict the "HandStart" event with an accuracy significantly better than random chance? This baseline will serve as a benchmark to evaluate the effectiveness of future feature engineering and modeling improvements.

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
        Full Channel Ranking per Subject for Event: HandStart
###########################################################
| Subject    | Average AUC | All Channels Sorted by AUC (Channel | AUC Score) |
|------------|-------------|----------------------------------------------------|
| subj1      | 0.5440      | F7(0.6722) O2(0.6107) PO9(0.6105) CP5(0.6012) FC5(0.6003) P3(0.5995) T7(0.5956) F3(0.5882) P4(0.5792) Oz(0.5777) F4(0.5686) P7(0.5575) FC1(0.5554) CP6(0.5479) C3(0.5477) CP1(0.5460) C4(0.5439) FC2(0.5364) Cz(0.5332) Fz(0.5316) O1(0.5303) Pz(0.5290) TP9(0.5188) CP2(0.5154) T8(0.5086) P8(0.5062) FC6(0.4988) F8(0.4984) Fp2(0.4738) TP10(0.4502) PO10(0.4498) Fp1(0.4237) |
| subj2      | 0.6346      | T7(0.7104) P7(0.7063) TP9(0.6981) Fp2(0.6974) Fp1(0.6908) P4(0.6904) P3(0.6885) Oz(0.6876) CP5(0.6868) PO9(0.6805) P8(0.6790) CP2(0.6787) CP6(0.6742) O1(0.6739) PO10(0.6697) FC5(0.6646) T8(0.6619) O2(0.6569) CP1(0.6536) TP10(0.6523) Cz(0.6493) C4(0.6347) F7(0.6212) FC6(0.6172) Pz(0.6056) FC1(0.5775) FC2(0.5761) F8(0.5348) F4(0.5033) Fz(0.4988) F3(0.4948) C3(0.3925) |
| subj3      | 0.5984      | T7(0.6827) FC5(0.6734) CP5(0.6665) F4(0.6588) F3(0.6578) F8(0.6567) P8(0.6555) F7(0.6501) FC6(0.6494) Fp1(0.6475) T8(0.6444) CP6(0.6347) C4(0.6275) PO10(0.6154) O2(0.6108) Oz(0.6043) TP10(0.6012) P4(0.5969) Fp2(0.5928) O1(0.5923) P7(0.5915) P3(0.5884) FC2(0.5765) PO9(0.5746) C3(0.5708) CP1(0.5390) Pz(0.5276) Fz(0.5212) Cz(0.5168) CP2(0.5131) FC1(0.5102) TP9(0.3987) |
| subj4      | 0.6031      | O1(0.7097) Oz(0.6972) P3(0.6927) CP1(0.6862) P4(0.6829) O2(0.6660) P7(0.6634) CP6(0.6540) PO10(0.6461) CP5(0.6367) PO9(0.6362) Fp2(0.6304) Cz(0.6293) Pz(0.6224) Fp1(0.6210) TP9(0.6131) P8(0.6086) T7(0.6023) CP2(0.5984) FC5(0.5935) TP10(0.5880) T8(0.5824) FC6(0.5790) C3(0.5635) F7(0.5453) Fz(0.5413) F3(0.5401) FC2(0.5357) FC1(0.5022) C4(0.4880) F8(0.4773) F4(0.4659) |
| subj5      | 0.5451      | T7(0.6206) F7(0.6205) P7(0.6150) FC5(0.5954) CP5(0.5932) O1(0.5879) C3(0.5864) CP6(0.5730) P8(0.5697) Oz(0.5634) O2(0.5582) Fp1(0.5529) F3(0.5525) PO9(0.5516) FC6(0.5470) T8(0.5446) Fp2(0.5314) CP2(0.5308) C4(0.5294) PO10(0.5260) Pz(0.5213) CP1(0.5184) TP10(0.5174) P3(0.5164) TP9(0.5140) P4(0.5118) Cz(0.5103) F4(0.5048) F8(0.5033) FC1(0.5008) FC2(0.4883) Fz(0.4876) |
| subj6      | 0.5347      | CP5(0.6122) F4(0.6071) PO9(0.5987) Fp2(0.5984) T7(0.5952) P3(0.5880) P7(0.5756) FC5(0.5724) Pz(0.5643) TP9(0.5614) C3(0.5569) O1(0.5527) CP1(0.5508) P4(0.5494) Oz(0.5453) Fz(0.5448) O2(0.5437) F7(0.5431) Cz(0.5412) CP2(0.5369) TP10(0.5269) PO10(0.5260) Fp1(0.5233) P8(0.5232) CP6(0.5115) FC1(0.5033) T8(0.4808) F3(0.4799) C4(0.4733) FC6(0.4443) FC2(0.4320) F8(0.3488) |
| subj7      | 0.6637      | P3(0.7840) Pz(0.7784) CP5(0.7711) CP1(0.7648) T7(0.7641) P4(0.7518) O2(0.7511) Oz(0.7428) P7(0.7256) CP2(0.7205) TP9(0.7202) O1(0.7121) P8(0.7093) PO10(0.7061) FC5(0.6885) PO9(0.6875) F7(0.6677) TP10(0.6659) C3(0.6551) CP6(0.6495) T8(0.6488) C4(0.6478) Fp2(0.6336) FC6(0.6096) Fp1(0.6045) FC1(0.5906) Fz(0.5602) FC2(0.5563) F3(0.5359) F4(0.5190) Cz(0.4749) F8(0.4412) |
| subj8      | 0.5278      | FC6(0.5983) T8(0.5805) O1(0.5704) F7(0.5691) F8(0.5665) FC2(0.5593) PO9(0.5559) Oz(0.5541) F4(0.5507) T7(0.5489) PO10(0.5488) Fp2(0.5400) P3(0.5358) FC5(0.5351) P4(0.5281) CP5(0.5233) TP10(0.5188) P7(0.5178) Cz(0.5169) O2(0.5145) F3(0.5079) Fp1(0.5079) P8(0.5064) Pz(0.5060) CP6(0.5048) TP9(0.5047) CP1(0.5003) C4(0.4970) CP2(0.4946) Fz(0.4809) C3(0.4735) FC1(0.4727) |
| subj9      | 0.5924      | O1(0.7075) Oz(0.6950) Fp2(0.6874) P7(0.6788) PO10(0.6747) TP10(0.6648) Fp1(0.6483) CP6(0.6481) T7(0.6476) P4(0.6390) TP9(0.6328) O2(0.6326) P3(0.6257) CP5(0.6223) PO9(0.6196) Pz(0.6122) FC5(0.6110) C3(0.6031) P8(0.5986) CP2(0.5840) T8(0.5743) F7(0.5625) FC6(0.5425) CP1(0.5400) F4(0.5378) C4(0.5171) FC2(0.4909) F8(0.4898) F3(0.4897) Cz(0.4738) FC1(0.4707) Fz(0.4332) |
| subj10     | 0.6093      | Oz(0.7469) O2(0.7439) O1(0.7358) P8(0.7347) P3(0.7172) Fp2(0.6950) CP1(0.6924) P4(0.6890) PO9(0.6703) CP2(0.6667) Pz(0.6645) F7(0.6630) FC5(0.6606) P7(0.6482) CP5(0.6317) T7(0.6145) PO10(0.6129) CP6(0.6018) TP9(0.5948) TP10(0.5909) C4(0.5845) FC1(0.5718) C3(0.5696) Cz(0.5643) Fz(0.5630) Fp1(0.5452) F3(0.5154) T8(0.5027) FC2(0.4811) F4(0.4368) FC6(0.4335) F8(0.3554) |
| subj11     | 0.6316      | Oz(0.7667) P7(0.7520) Pz(0.7497) CP5(0.7363) O1(0.7358) P3(0.7184) P8(0.7099) PO9(0.6956) O2(0.6942) CP6(0.6869) PO10(0.6699) P4(0.6503) TP9(0.6482) Fp2(0.6420) C4(0.6368) T8(0.6289) T7(0.6223) F8(0.6189) FC5(0.6184) TP10(0.6137) C3(0.6010) FC6(0.5934) Fp1(0.5921) CP1(0.5834) Cz(0.5651) F3(0.5493) F7(0.5441) FC2(0.5434) CP2(0.5397) FC1(0.5381) F4(0.4995) Fz(0.4668) |
| subj12     | 0.5970      | P3(0.7148) O1(0.7038) Oz(0.6718) Pz(0.6705) O2(0.6609) T7(0.6598) CP1(0.6589) C3(0.6584) FC5(0.6499) CP5(0.6385) P4(0.6353) PO9(0.6225) TP9(0.6215) P7(0.6194) CP2(0.6083) P8(0.6053) PO10(0.5943) F3(0.5884) C4(0.5749) Fz(0.5695) FC2(0.5660) CP6(0.5650) F7(0.5601) TP10(0.5564) T8(0.5449) F4(0.5437) Cz(0.5286) FC6(0.5201) FC1(0.5052) Fp1(0.5032) F8(0.4921) Fp2(0.4908) |
###########################################################

The results indicate that even with raw signals, most subjects show an average AUC score significantly above 0.5, suggesting that there is some predictive information present in the unprocessed EEG data. However, the performance is generally low and inconsistent across subjects, highlighting the need for more advanced signal processing.

**4. Conclusion & Next Steps**

This experiment successfully established a baseline for the "HandStart" event. The key conclusion is that while raw EEG signals contain some predictive power, they are not sufficient for building a robust and accurate prediction model.

Based on these findings, the next logical step is to investigate the impact of feature engineering. The subsequent experiment, **feature_filterbank_v1**, will apply a filter bank to the raw signals to extract frequency-based features and evaluate if this technique can significantly improve upon the baseline AUC scores.
