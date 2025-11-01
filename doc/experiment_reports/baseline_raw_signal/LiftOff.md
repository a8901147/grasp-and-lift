### **Experiment 1: Baseline Model with Raw EEG Signal for "LiftOff" Event**

**1. Research Question**

This experiment aims to establish a baseline performance for event prediction using raw EEG signals without any feature engineering. The central question is: Does the unprocessed EEG signal from a single channel contain sufficient information to predict the "LiftOff" event with an accuracy significantly better than random chance? This baseline will serve as a benchmark to evaluate the effectiveness of future feature engineering and modeling improvements.

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
        Full Channel Ranking per Subject for Event: LiftOff
###########################################################
| Subject    | Average AUC | All Channels Sorted by AUC (Channel | AUC Score) |
|------------|-------------|----------------------------------------------------|
| subj1      | 0.5822      | PO10(0.6927) CP6(0.6836) F8(0.6693) O2(0.6627) P8(0.6555) FC6(0.6509) C4(0.6488) T8(0.6398) Oz(0.6386) CP2(0.6355) P4(0.6318) TP10(0.6292) TP9(0.6288) Pz(0.6097) P7(0.5998) FC2(0.5975) P3(0.5961) F4(0.5892) O1(0.5826) CP5(0.5788) T7(0.5771) Fz(0.5609) CP1(0.5349) FC5(0.5325) F7(0.5163) Cz(0.5125) Fp1(0.5023) FC1(0.4797) PO9(0.4720) C3(0.4673) F3(0.4616) Fp2(0.3926) |
| subj2      | 0.5485      | F7(0.6366) Fp2(0.6365) FC5(0.6273) T7(0.6215) CP5(0.6092) P7(0.5905) C3(0.5896) TP9(0.5823) O1(0.5782) CP1(0.5722) P3(0.5718) FC1(0.5700) Oz(0.5633) Cz(0.5622) O2(0.5590) PO9(0.5583) F4(0.5501) Fp1(0.5486) PO10(0.5472) CP2(0.5450) P4(0.5404) F3(0.5355) Pz(0.5333) F8(0.5307) Fz(0.5120) FC2(0.4838) C4(0.4734) TP10(0.4726) FC6(0.4697) T8(0.4686) CP6(0.4577) P8(0.4561) |
| subj3      | 0.6338      | T8(0.7064) CP6(0.7047) CP5(0.7023) FC6(0.7014) C4(0.7006) P8(0.7002) PO10(0.7002) FC2(0.6969) F4(0.6833) P4(0.6812) F3(0.6806) F8(0.6739) FC5(0.6673) P7(0.6646) T7(0.6605) PO9(0.6570) O2(0.6545) O1(0.6474) C3(0.6456) CP2(0.6439) TP10(0.6398) Fp1(0.6335) Fp2(0.6334) Oz(0.6181) P3(0.6029) Pz(0.5852) CP1(0.5746) Fz(0.5700) FC1(0.5483) Cz(0.5194) F7(0.4076) TP9(0.3759) |
| subj4      | 0.5323      | F7(0.6257) CP1(0.6006) CP5(0.5938) T7(0.5679) FC5(0.5668) PO10(0.5626) O2(0.5575) F4(0.5544) F8(0.5518) F3(0.5518) P8(0.5464) FC6(0.5459) CP6(0.5447) T8(0.5438) C3(0.5436) TP9(0.5395) TP10(0.5324) Oz(0.5319) Fp1(0.5290) P4(0.5254) O1(0.5212) Fp2(0.5102) CP2(0.5098) FC2(0.5084) PO9(0.5054) C4(0.5005) Fz(0.5003) Cz(0.4984) Pz(0.4808) FC1(0.4795) P7(0.4647) P3(0.4390) |
| subj5      | 0.5406      | Oz(0.6195) O2(0.6073) O1(0.5963) PO10(0.5919) Pz(0.5901) CP6(0.5847) F8(0.5847) FC6(0.5845) P8(0.5792) PO9(0.5725) T8(0.5610) P4(0.5559) TP9(0.5509) P3(0.5397) CP2(0.5364) F7(0.5363) F4(0.5301) TP10(0.5296) P7(0.5249) Fp1(0.5242) FC2(0.5199) C4(0.5179) F3(0.5144) CP5(0.5071) Cz(0.5059) FC1(0.5023) C3(0.5013) FC5(0.5010) Fp2(0.4914) CP1(0.4914) T7(0.4859) Fz(0.4602) |
| subj6      | 0.5378      | CP1(0.6332) P3(0.6146) Pz(0.6092) F4(0.5922) C3(0.5856) CP5(0.5796) F7(0.5699) FC1(0.5674) P4(0.5599) F8(0.5592) O1(0.5576) Oz(0.5548) FC6(0.5542) FC5(0.5526) O2(0.5510) Fp2(0.5487) Fz(0.5346) T7(0.5328) T8(0.5290) P7(0.5191) P8(0.5169) FC2(0.5160) PO10(0.5157) C4(0.5095) TP9(0.5051) F3(0.5023) TP10(0.4874) CP6(0.4852) Fp1(0.4821) Cz(0.4782) PO9(0.4720) CP2(0.4351) |
| subj7      | 0.5653      | O2(0.6718) F7(0.6360) Oz(0.6306) P4(0.6288) FC2(0.6262) CP2(0.6111) C4(0.6107) P8(0.6030) PO10(0.6002) P3(0.5900) F8(0.5889) Pz(0.5862) TP10(0.5754) T8(0.5703) FC6(0.5696) FC1(0.5654) O1(0.5625) FC5(0.5546) Fp2(0.5528) C3(0.5468) F4(0.5432) TP9(0.5361) PO9(0.5358) Fz(0.5329) CP6(0.5298) CP5(0.5233) Fp1(0.5223) F3(0.5116) T7(0.5092) CP1(0.4922) Cz(0.4904) P7(0.4833) |
| subj8      | 0.5341      | Fp1(0.6411) Fp2(0.6280) TP10(0.5929) C3(0.5927) CP1(0.5887) P7(0.5884) P3(0.5626) O1(0.5614) FC6(0.5612) PO9(0.5559) Fz(0.5496) F4(0.5454) Pz(0.5425) FC2(0.5379) F3(0.5345) Cz(0.5322) CP5(0.5321) F7(0.5316) TP9(0.5216) P4(0.5202) FC5(0.5136) O2(0.5109) CP6(0.5095) T8(0.4951) FC1(0.4937) PO10(0.4925) T7(0.4922) Oz(0.4759) F8(0.4744) CP2(0.4725) C4(0.4722) P8(0.4691) |
| subj9      | 0.5659      | C3(0.6751) T7(0.6505) CP5(0.6400) P7(0.6328) TP9(0.6237) O1(0.6208) P3(0.6193) FC5(0.6113) Oz(0.6086) F7(0.6085) PO9(0.5964) FC1(0.5790) Fp2(0.5763) Pz(0.5700) TP10(0.5610) CP2(0.5585) PO10(0.5581) P4(0.5575) CP6(0.5516) F4(0.5429) T8(0.5413) CP1(0.5387) Cz(0.5380) O2(0.5369) F8(0.5192) P8(0.5185) F3(0.5169) FC6(0.5082) C4(0.5014) Fp1(0.4893) Fz(0.4877) FC2(0.4722) |
| subj10     | 0.5576      | F7(0.6960) F8(0.6826) FC2(0.6439) FC6(0.6416) C4(0.6414) FC5(0.6392) Fp1(0.6345) F4(0.6121) FC1(0.5985) T7(0.5932) Pz(0.5875) T8(0.5874) CP2(0.5651) F3(0.5643) CP6(0.5639) TP9(0.5521) Fp2(0.5475) P8(0.5452) P3(0.5364) TP10(0.5337) Cz(0.5322) O1(0.5303) C3(0.5250) CP1(0.4965) P4(0.4933) PO10(0.4859) O2(0.4847) Oz(0.4789) P7(0.4701) PO9(0.4665) Fz(0.4617) CP5(0.4518) |
| subj11     | 0.5436      | FC1(0.7177) Fz(0.6550) Cz(0.6352) Fp2(0.6248) Pz(0.6183) FC2(0.6118) Oz(0.5938) F4(0.5868) P4(0.5722) Fp1(0.5625) F8(0.5597) O1(0.5510) TP9(0.5487) C4(0.5425) CP1(0.5414) FC5(0.5363) C3(0.5305) F7(0.5303) T8(0.5173) P7(0.5142) PO10(0.5076) CP2(0.5068) CP6(0.5065) TP10(0.5056) PO9(0.5020) T7(0.5004) O2(0.5000) P8(0.4941) F3(0.4751) FC6(0.4738) CP5(0.4389) P3(0.4348) |
| subj12     | 0.5441      | T7(0.6497) C3(0.6344) TP9(0.6342) FC5(0.6103) P3(0.6073) P7(0.5990) PO9(0.5978) O1(0.5975) CP5(0.5858) CP1(0.5843) Oz(0.5704) CP6(0.5687) CP2(0.5675) P4(0.5672) O2(0.5600) PO10(0.5470) TP10(0.5462) F3(0.5427) F7(0.5385) Fz(0.5259) F4(0.5204) FC1(0.5181) Fp2(0.5120) Fp1(0.5066) FC2(0.4932) F8(0.4903) Cz(0.4853) FC6(0.4845) P8(0.4709) T8(0.4539) C4(0.4290) Pz(0.4119) |
###########################################################

The results for the "LiftOff" event are consistent with other baseline experiments. The average AUC scores hover above 0.5, indicating some level of predictive capability from the raw signal, but the performance is not strong enough for a reliable model.

**4. Conclusion & Next Steps**

This experiment establishes a performance baseline for the "LiftOff" event. As with the other events, the raw EEG signal alone is not sufficient for high-performance prediction.

The next step is to proceed with the **feature_filterbank_v1** experiment to see if feature engineering can improve these results.
