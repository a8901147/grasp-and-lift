### **Experiment 1: Baseline Model with Raw EEG Signal for "Replace" Event**

**1. Research Question**

This experiment aims to establish a baseline performance for event prediction using raw EEG signals without any feature engineering. The central question is: Does the unprocessed EEG signal from a single channel contain sufficient information to predict the "Replace" event with an accuracy significantly better than random chance? This baseline will serve as a benchmark to evaluate the effectiveness of future feature engineering and modeling improvements.

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
        Full Channel Ranking per Subject for Event: Replace
###########################################################
| Subject    | Average AUC | All Channels Sorted by AUC (Channel | AUC Score) |
|------------|-------------|----------------------------------------------------|
| subj1      | 0.5612      | Fp2(0.8312) Fp1(0.8147) Fz(0.6897) F3(0.6764) F7(0.6543) F4(0.6459) F8(0.6326) PO9(0.5974) O2(0.5838) FC1(0.5796) FC5(0.5756) CP2(0.5601) Pz(0.5533) CP1(0.5512) Oz(0.5438) O1(0.5360) Cz(0.5322) FC2(0.5285) C3(0.5141) TP10(0.5094) P3(0.5087) PO10(0.5058) C4(0.5025) P4(0.4934) P8(0.4884) TP9(0.4874) P7(0.4798) FC6(0.4785) CP5(0.4783) T8(0.4780) T7(0.4740) CP6(0.4733) |
| subj2      | 0.6187      | Fp1(0.8434) Fp2(0.8337) Cz(0.6711) TP10(0.6680) TP9(0.6629) PO9(0.6606) P7(0.6562) PO10(0.6495) P8(0.6483) CP6(0.6468) T8(0.6408) CP1(0.6387) O1(0.6370) CP2(0.6326) CP5(0.6145) FC1(0.6141) P3(0.6138) FC6(0.6105) Oz(0.6103) O2(0.6099) F7(0.6093) C4(0.6090) T7(0.6081) P4(0.6081) FC2(0.5854) F8(0.5821) F3(0.5795) Pz(0.5707) FC5(0.5333) Fz(0.4806) F4(0.4789) C3(0.3897) |
| subj3      | 0.5189      | Fp1(0.6423) T7(0.6362) F3(0.6326) CP5(0.6267) F7(0.6176) FC5(0.6160) T8(0.5990) TP9(0.5862) C4(0.5833) PO9(0.5729) O2(0.5695) P7(0.5524) Oz(0.5513) P4(0.5478) O1(0.5458) C3(0.5444) Pz(0.5426) Cz(0.5292) CP2(0.5045) FC1(0.5034) Fz(0.4954) P3(0.4761) CP1(0.4547) FC6(0.4283) Fp2(0.4247) F8(0.4183) FC2(0.4183) TP10(0.4161) F4(0.4123) CP6(0.3999) P8(0.3789) PO10(0.3775) |
| subj4      | 0.5155      | C4(0.6145) F7(0.6086) Fp1(0.6061) F3(0.6026) Fp2(0.5791) CP1(0.5743) FC5(0.5721) CP2(0.5648) Fz(0.5584) Cz(0.5560) T7(0.5538) TP9(0.5475) F8(0.5408) CP5(0.5326) Pz(0.4975) C3(0.4937) FC2(0.4917) P3(0.4826) FC6(0.4815) P8(0.4809) FC1(0.4800) T8(0.4796) P7(0.4775) O2(0.4695) F4(0.4643) PO9(0.4632) TP10(0.4624) O1(0.4622) Oz(0.4594) P4(0.4501) CP6(0.4444) PO10(0.4443) |
| subj5      | 0.5010      | CP6(0.6123) O2(0.5803) T7(0.5766) Oz(0.5682) FC5(0.5672) C3(0.5652) PO9(0.5571) F7(0.5503) F8(0.5333) Fz(0.5331) FC2(0.5281) FC1(0.5272) F4(0.5226) Cz(0.5193) TP10(0.5187) Fp2(0.5145) F3(0.5053) Fp1(0.4982) P3(0.4824) TP9(0.4742) CP1(0.4700) CP5(0.4574) FC6(0.4552) P7(0.4505) T8(0.4484) C4(0.4433) PO10(0.4404) CP2(0.4361) Pz(0.4326) P4(0.4297) O1(0.4250) P8(0.4082) |
| subj6      | 0.5883      | Fp1(0.7574) Fp2(0.6831) Pz(0.6711) CP2(0.6688) P4(0.6430) CP1(0.6414) F3(0.6312) Fz(0.6302) T8(0.6148) P3(0.6136) O2(0.6090) Oz(0.6086) F7(0.6029) C4(0.6007) CP6(0.5962) P8(0.5943) O1(0.5913) F8(0.5885) Cz(0.5754) PO10(0.5742) TP10(0.5728) FC6(0.5617) FC5(0.5521) CP5(0.5497) FC2(0.5478) TP9(0.5431) P7(0.5421) FC1(0.5251) T7(0.5230) PO9(0.5124) C3(0.4606) F4(0.4402) |
| subj7      | 0.5412      | Fp1(0.6702) F7(0.6376) Fp2(0.6366) T7(0.6170) F8(0.6111) F3(0.5991) FC5(0.5912) Fz(0.5718) O2(0.5584) P3(0.5580) FC6(0.5518) P4(0.5436) CP5(0.5417) FC1(0.5401) C3(0.5396) T8(0.5305) P7(0.5278) Pz(0.5172) CP2(0.5142) C4(0.5129) Cz(0.5124) O1(0.5121) FC2(0.5115) TP10(0.5083) CP1(0.5042) F4(0.5040) PO10(0.4960) CP6(0.4951) PO9(0.4910) P8(0.4782) TP9(0.4689) Oz(0.4651) |
| subj8      | 0.5314      | Fp1(0.6494) Fp2(0.6400) P3(0.5936) C3(0.5911) Pz(0.5859) CP1(0.5855) P7(0.5818) C4(0.5656) CP2(0.5635) P8(0.5628) F3(0.5485) TP10(0.5484) CP6(0.5425) F8(0.5389) CP5(0.5383) PO9(0.5341) P4(0.5305) F7(0.5291) O2(0.5236) TP9(0.5108) FC5(0.5078) Oz(0.5039) PO10(0.5032) Cz(0.4965) O1(0.4938) T8(0.4901) T7(0.4646) FC1(0.4620) FC6(0.4599) FC2(0.4577) F4(0.4528) Fz(0.4484) |
| subj9      | 0.5366      | Fp1(0.6365) Fp2(0.6021) T7(0.5644) F7(0.5638) O1(0.5608) PO9(0.5592) TP9(0.5582) P7(0.5554) CP5(0.5528) Oz(0.5521) T8(0.5520) P3(0.5519) P4(0.5510) P8(0.5488) C3(0.5462) Pz(0.5456) FC6(0.5455) CP6(0.5451) FC2(0.5449) TP10(0.5448) F3(0.5292) F8(0.5271) CP1(0.5237) O2(0.5237) FC5(0.5130) Cz(0.5115) Fz(0.5081) F4(0.4924) FC1(0.4855) PO10(0.4817) C4(0.4739) CP2(0.4213) |
| subj10     | 0.5827      | Fp1(0.7587) Fp2(0.7175) F7(0.6399) T8(0.6382) F3(0.6318) CP2(0.6164) TP10(0.6154) O2(0.6140) CP1(0.6078) PO9(0.6064) C4(0.6054) FC6(0.6025) P4(0.6013) F8(0.5816) PO10(0.5795) P7(0.5768) FC5(0.5763) O1(0.5693) CP6(0.5674) Cz(0.5667) TP9(0.5654) P8(0.5628) CP5(0.5616) Pz(0.5587) Oz(0.5461) T7(0.5398) FC1(0.5378) Fz(0.5304) C3(0.5273) P3(0.5039) FC2(0.4737) F4(0.4664) |
| subj11     | 0.5611      | Fz(0.7136) Fp2(0.6844) Fp1(0.6556) Cz(0.6377) F3(0.6274) Pz(0.6212) FC2(0.6123) Oz(0.6000) CP2(0.5737) O1(0.5712) T8(0.5693) CP5(0.5669) O2(0.5631) F4(0.5571) F7(0.5567) PO9(0.5552) FC1(0.5507) P8(0.5428) FC5(0.5406) CP6(0.5405) FC6(0.5360) CP1(0.5348) TP10(0.5343) PO10(0.5294) TP9(0.5274) C4(0.5256) P4(0.5147) P3(0.4979) P7(0.4946) T7(0.4878) C3(0.4857) F8(0.4478) |
| subj12     | 0.5618      | TP9(0.6419) O1(0.6192) PO9(0.6153) Fz(0.6107) P7(0.6083) Oz(0.6003) T7(0.5973) C3(0.5923) F4(0.5913) P3(0.5869) Cz(0.5811) FC5(0.5729) TP10(0.5705) Pz(0.5696) PO10(0.5665) O2(0.5658) CP5(0.5646) CP6(0.5581) CP1(0.5541) P8(0.5493) P4(0.5490) CP2(0.5469) C4(0.5380) T8(0.5337) F7(0.5336) FC2(0.5234) Fp1(0.5233) Fp2(0.5185) F8(0.5113) FC1(0.5053) FC6(0.4923) F3(0.4871) |
###########################################################

The results for the "Replace" event are consistent with other baseline experiments. The average AUC scores hover above 0.5, indicating some level of predictive capability from the raw signal, but the performance is not strong enough for a reliable model.

**4. Conclusion & Next Steps**

This experiment establishes a performance baseline for the "Replace" event. As with the other events, the raw EEG signal alone is not sufficient for high-performance prediction.

The next step is to proceed with the **feature_filterbank_v1** experiment to see if feature engineering can improve these results.
