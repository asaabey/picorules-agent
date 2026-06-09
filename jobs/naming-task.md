# Picorules Attribute Dictionary

| # | Group Search Attribute | Ruleblock | Attribute Description |
|---|------------------------|-----------|----------------------|
| 1 | Absent ICPC Coding indicating Diabetes Mellitus | cd_dm_dx | Flag indicating diabetes diagnosed by lab (HbA1c ≥6.5%) or medication but missing formal ICPC2+ diagnostic coding in the EHR |
| 2 | Adult polycystic kidney disease | ckd_c_rnm | Binary flag for autosomal dominant polycystic kidney disease (ADPKD) identified via ICD Q61.2 coding |
| 3 | AKI in last 12 months | ad_aki | Acute kidney injury detected in the past 12 months, defined by creatinine-to-baseline ratio >4 with AKIN stage ≥2 and incomplete recovery, or ICD N17 code |
| 4 | Alert High Hb associated with ESA therapy | tg4810 | Clinical trigger: haemoglobin >130 g/L with a rising trend in a patient actively receiving ESA therapy, indicating cardiovascular/thrombotic risk |
| 5 | Alert Acute kidney injury in community | tg4100 | Clinical trigger: community-detected AKI based on creatinine slope analysis with AKIN staging ≥2 and incomplete resolution, excluding patients on RRT or with advanced CKD |
| 6 | Alert Medication safety concern | tg4660 | Clinical trigger: concurrent use of NSAIDs with biguanide or SGLT2i in a patient with CKD stage ≥3, flagging medication safety risk (triple whammy) |
| 7 | Alert Nephrotic range proteinuria in the absence of diabetes | tg4410 | Clinical trigger: two consecutive uACR readings >300 mg/mmol with sustained or worsening proteinuria in a non-diabetic patient not yet seen by renal services |
| 8 | Alert New commencement on RRT within 1 year | tg4722 | Clinical trigger: patient commenced haemodialysis (≥10 sessions) or peritoneal dialysis within the last 12 months |
| 9 | Alert New commencement on RRT within last 3 months | tg4720 | Clinical trigger: patient commenced haemodialysis (≥10 sessions) or peritoneal dialysis within the last 90 days |
| 10 | Alert No AVF with advanced CKD4+ with rapid progression | tg4620 | Clinical trigger: CKD stages 4–5 with rapid eGFR decline and no arteriovenous fistula formed, indicating need for timely vascular access planning |
| 11 | Alert Possible nephritic syndrome | tg4420 | Clinical trigger: urine RBC >100 with low leucocytes and uACR >30, suggesting active glomerulonephritis requiring further immunological workup |
| 12 | Alert Potentially untreated chronic disease | tg2610 | Clinical trigger: untreated CKD (elevated BP + normal K⁺ + no RAAS inhibitor) or untreated diabetes (HbA1c >8% with no DM medications) |
| 13 | Alert Potentially untreated proteinuric CKD | tg4630 | Clinical trigger: proteinuric CKD (albuminuria A2+) with gaps in guideline-recommended pharmacotherapy (RAAS inhibitor, SGLT2i, or MRA) |
| 14 | Alert Unmanaged possible CKD 4 | tg4122 | Clinical trigger: calculated CKD stage 4 with no documented renal service engagement despite recent primary care activity |
| 15 | Alert Unmanaged possible CKD 5 | tg4123 | Clinical trigger: calculated CKD stage 5 with no documented renal service engagement despite recent primary care activity within 180 days |
| 16 | Alert Unmanaged possible early CKD with rapid progression | tg4610 | Clinical trigger: CKD stages 1–2 with eGFR slope declining faster than −20 mL/min/year, eGFR <80, and albuminuria A3+, without renal engagement |
| 17 | AMI | cd_cardiac_cad | Binary flag for acute myocardial infarction (STEMI or NSTEMI) identified from ICD I21/I23 or ICPC K75/K76 coding |
| 18 | Anaemia in CKD without ESA | ckd_complications | Binary flag for haemoglobin <100 g/L in CKD stage ≥4 without current erythropoiesis-stimulating agent (ESA) therapy |
| 19 | Anterior Resection | sx_abdo | Binary flag for anterior resection procedure (high or low) identified from CARESYS procedure codes for colorectal surgery |
| 20 | Aortic Valve insufficiency | cd_cardiac_vhd | Binary flag for aortic valve regurgitation/insufficiency identified from ICD I06.1/I35.1 or ICPC K83 coding |
| 21 | Aortic valve replacement | cd_cardiac_vhd | Binary flag for surgical aortic valve replacement identified from ICPC K54005 coding |
| 22 | Aortic valve stenosis | cd_cardiac_vhd | Binary flag for aortic valve stenosis identified from ICD I06.0/I35.0 or ICPC K83/K71 coding |
| 23 | At risk for CKD | at_risk | Binary flag for patients without CKD or RRT but with at least one risk factor (diabetes, hypertension, CVD, obesity, AKI, RHD, or hepatitis B) |
| 24 | Attendance at oncology clinic | ca_careplan | Binary flag indicating the patient has attended an outpatient oncology clinic encounter |
| 25 | AV fistuloplasty | rrt_hd_acc_iv | Binary flag for presence of AV fistula surveillance or fistuloplasty procedure in a patient on haemodialysis or home HD |
| 26 | AV fistuloplasty last date | rrt_hd_acc_iv | Date of the most recent AV fistuloplasty or vascular access surveillance procedure |
| 27 | Benign Prostatic Hyperplasia | uro_bph | Binary flag for benign prostatic hyperplasia identified from ICD/ICPC urological coding |
| 28 | BMI | cd_obesity | Body mass index calculated from last recorded weight (kg) and height (m); used to classify obesity (BMI >30) |
| 29 | CABG | cd_cardiac_cad | Binary flag for coronary artery bypass graft surgery identified from ICD Z95.1 or ICPC K54007 coding |
| 30 | CABG-FDT | cd_cardiac_cad | First documented date of coronary artery bypass graft surgery |
| 31 | Cardiac outpatient encounter | cd_cardiac_enc | Binary flag indicating the patient has attended a cardiac outpatient clinic encounter |
| 32 | Charlson comorbidity index | cmid_charlson | Weighted comorbidity score (0–37) calculated across 17 disease categories using ICD/ICPC codes with standard Charlson weighting (1–6 per condition) |
| 33 | Chronic HepB | cd_hepb_master | Master binary flag for chronic hepatitis B, combining coded diagnosis status and serological evidence from HBsAg/HBeAg/HBV DNA results |
| 34 | Chronic HepB ALT Last result date | cd_hepb_master | Date of the most recent alanine aminotransferase (ALT) result for hepatitis B monitoring |
| 35 | Chronic HepB Antiviral Agent | cd_hepb_master | Name of the current HBV antiviral agent: Entecavir, Tenofovir, Lamivudine, or Adefovir (if prescribed) |
| 36 | Chronic HepB Coded Status Code | cd_hepb_master | Numeric code representing the EHR-coded hepatitis B diagnosis status (C+, C−, or unclassified) |
| 37 | Chronic HepB Coded Status Label | cd_hepb_master | Human-readable label for the coded hepatitis B diagnosis status (e.g., "C+ confirmed", "C− resolved") |
| 38 | Chronic HepB Coding Vrs Serology | cd_hepb_master | Concordance label comparing coded HBV diagnosis against serological test results to flag discrepancies |
| 39 | Chronic HepB HepB Viral Load Last result date | cd_hepb_master | Date of the most recent HBV DNA viral load test result |
| 40 | Chronic HepB Immune clearance phase | cd_hepb_master | Binary flag for immune clearance phase (phase 2): HBeAg-positive with elevated ALT and high viral load |
| 41 | Chronic HepB Immune control phase | cd_hepb_master | Binary flag for immune control phase (phase 3): HBeAg-negative with normal ALT and low/undetectable viral load |
| 42 | Chronic HepB Immune escape phase | cd_hepb_master | Binary flag for immune escape phase (phase 4): HBeAg-negative with elevated ALT and detectable viral load (reactivation) |
| 43 | Chronic HepB Immune Phase Code | cd_hepb_master | Numeric code (1–4) for the current HBV immune phase: 1=tolerance, 2=clearance, 3=control, 4=escape |
| 44 | Chronic HepB Immune Phase Date | cd_hepb_master | Date when the current HBV immune phase classification was determined |
| 45 | Chronic HepB Immune Phase label | cd_hepb_master | Human-readable label for the current HBV immune phase (e.g., "Immune tolerance", "Immune escape") |
| 46 | Chronic HepB Immune tolerance phase | cd_hepb_master | Binary flag for immune tolerance phase (phase 1): HBeAg-positive with normal ALT and high viral load |
| 47 | Chronic HepB Serological Status Code | cd_hepb_master | Numeric code (1–9) representing the serological HBV status derived from HBsAg, HBeAg, and HBV DNA results |
| 48 | Chronic HepB Serological Status Date | cd_hepb_master | Date when the serological HBV status was last assessed |
| 49 | Chronic HepB Serological Status Label | cd_hepb_master | Human-readable label for the serological HBV status (e.g., "S+ chronic infection", "S− resolved") |
| 50 | Chronic HepB Ultrasound Last Date | cd_hepb_master | Date of the most recent abdominal ultrasound for hepatocellular carcinoma surveillance in chronic HBV |
| 51 | CKD aetiology likely diabetes | ckd_cause | Binary flag indicating diabetes is the likely cause of CKD, based on coded diabetes in a patient with CKD or RRT |
| 52 | CKD aetiology likely hypertension | ckd_cause | Binary flag indicating hypertension is the likely CKD cause, based on coded hypertension in a CKD/RRT patient without diabetes |
| 53 | CKD aetiology likely Lupus nephritis | ckd_cause | Binary flag indicating lupus nephritis is the likely CKD cause, based on coded SLE in a CKD/RRT patient |
| 54 | CKD aetiology likely other GN | ckd_cause | Binary flag indicating other glomerulonephritis (non-lupus) as the likely CKD cause, based on ICD N00–N08 coding |
| 55 | CKD Anaemic ESA date | ckd_prog_vm | Date of the most recent erythropoiesis-stimulating agent (ESA) administration for CKD-related anaemia |
| 56 | CKD AVF formation date | ckd_prog_vm | Date when the arteriovenous fistula (AVF) was surgically created for haemodialysis access |
| 57 | CKD AVF present | ckd_prog_vm | Binary flag indicating a functioning arteriovenous fistula is present for haemodialysis access |
| 58 | CKD Blood pressure mean | ckd_prog_vm | Mean systolic blood pressure over the past 12 months, used for CKD progression monitoring |
| 59 | CKD Careplan | ckd_prog_vm | Numeric value extracted from the CKD component of the careplan_h9_v1 attribute, indicating careplan documentation status |
| 60 | CKD Careplan date | ckd_prog_vm | Date of the most recent CKD-specific careplan documentation |
| 61 | CKD CKD Education initial | ckd_prog_vm | Date of the patient's first CKD education session with renal services |
| 62 | CKD CKD Education Review | ckd_prog_vm | Date of the most recent CKD education review session |
| 63 | CKD CKD Stage | ckd_prog_vm | CKD stage label (G1–G5) per KDIGO 2012 classification based on eGFR and albuminuria persistence |
| 64 | CKD complications present | ckd_complications | Binary flag indicating at least one CKD complication in stage ≥3: anaemia, hyperkalaemia, hyperphosphataemia, secondary hyperparathyroidism, or hypoalbuminaemia |
| 65 | CKD Creatinine | ckd_prog_vm | Most recent serum creatinine value (umol/L) used for CKD monitoring |
| 66 | CKD Diabetes HbA1c | ckd_prog_vm | Most recent HbA1c value (%) for glycaemic monitoring in CKD patients with diabetes |
| 67 | CKD Diabetes HbA1c date | ckd_prog_vm | Date of the most recent HbA1c test for CKD patients with diabetes |
| 68 | CKD Diabetes Present | ckd_prog_vm | Binary flag indicating coexisting diabetes mellitus in a CKD patient |
| 69 | CKD eGFR | ckd_prog_vm | Most recent estimated glomerular filtration rate (mL/min/1.73m2) for CKD staging and progression tracking |
| 70 | CKD eGFR date | ckd_prog_vm | Date of the most recent eGFR measurement |
| 71 | CKD Haemoglobin | ckd_prog_vm | Most recent haemoglobin value (g/L) for anaemia monitoring in CKD |
| 72 | CKD Haemoglobin date | ckd_prog_vm | Date of the most recent haemoglobin measurement |
| 73 | CKD ipa_sep_id | ckd_prog_vm | Date of the most recent inpatient admission/separation for a CKD patient |
| 74 | CKD KFRE 2 year probability | kfre | Kidney Failure Risk Equation 2-year probability of progression to kidney failure (dialysis or transplant), using the 4-variable model (age, sex, eGFR, uACR) |
| 75 | CKD KFRE 5 year probability | kfre | Kidney Failure Risk Equation 5-year probability of progression to kidney failure, using the 4-variable model (age, sex, eGFR, uACR) |
| 76 | CKD KFRE eGFR value | kfre | eGFR value (mL/min/1.73m2) used as input to the KFRE calculation; applicable for CKD stages G3a–G4 |
| 77 | CKD KFRE uACR value | kfre | uACR value (mg/mmol) used as input to the KFRE calculation; converted to mg/g for the equation |
| 78 | CKD opa_sep_id | ckd_prog_vm | Date of the most recent outpatient clinic encounter for a CKD patient |
| 79 | CKD panel eGFR last date | ckd | Date of the most recent eGFR result from the CKD staging ruleblock |
| 80 | CKD panel eGFR last value | ckd | Most recent eGFR value (mL/min/1.73m2) from the CKD staging ruleblock |
| 81 | CKD panel uACR last date | ckd | Date of the most recent urine albumin-to-creatinine ratio (uACR) result |
| 82 | CKD panel uACR last value | ckd | Most recent uACR value (mg/mmol) from the CKD staging ruleblock |
| 83 | CKD stage 1 | ckd | Binary flag for CKD stage G1: eGFR ≥90 mL/min with persistent albuminuria (A2+) or structural/histological evidence |
| 84 | CKD stage 2 | ckd | Binary flag for CKD stage G2: eGFR 60–89 mL/min with persistent albuminuria (A2+) or structural evidence |
| 85 | CKD stage 3a | ckd | Binary flag for CKD stage G3a: eGFR 45–59 mL/min (mildly to moderately decreased), per KDIGO 2012 |
| 86 | CKD stage 3b | ckd | Binary flag for CKD stage G3b: eGFR 30–44 mL/min (moderately to severely decreased), per KDIGO 2012 |
| 87 | CKD stage 4 | ckd | Binary flag for CKD stage G4: eGFR 15–29 mL/min (severely decreased), per KDIGO 2012 |
| 88 | CKD stage 5 | ckd | Binary flag for CKD stage G5: eGFR <15 mL/min (kidney failure, not on RRT), per KDIGO 2012 |
| 89 | CKD TTEM : CKD-A1 date | ckd_ttem | Date when uACR first entered the A1 range (3–30 mg/mmol) -- time-to-event modelling for albuminuria progression |
| 90 | CKD TTEM : CKD-A1 val | ckd_ttem | uACR value (mg/mmol) at the time of first entering CKD albuminuria category A1 |
| 91 | CKD TTEM : CKD-A2 date | ckd_ttem | Date when uACR first entered the A2 range (30–300 mg/mmol) -- microalbuminuria onset |
| 92 | CKD TTEM : CKD-A2 val | ckd_ttem | uACR value (mg/mmol) at the time of first entering CKD albuminuria category A2 |
| 93 | CKD TTEM : CKD-A3 date | ckd_ttem | Date when uACR first exceeded 300 mg/mmol -- macroalbuminuria onset |
| 94 | CKD TTEM : CKD-A3 val | ckd_ttem | uACR value (mg/mmol) at the time of first entering CKD albuminuria category A3 |
| 95 | CKD TTEM : CKD-G1 date | ckd_ttem | Date when eGFR was first recorded ≥90 mL/min -- baseline for time-to-event CKD progression tracking |
| 96 | CKD TTEM : CKD-G1 val | ckd_ttem | eGFR value (mL/min/1.73m2) at the time of first G1 classification |
| 97 | CKD TTEM : CKD-G2 date | ckd_ttem | Date when eGFR first declined to 60–89 mL/min -- onset of CKD stage G2 |
| 98 | CKD TTEM : CKD-G2 val | ckd_ttem | eGFR value at the time of first G2 classification |
| 99 | CKD TTEM : CKD-G3a date | ckd_ttem | Date when eGFR first declined to 45–59 mL/min -- onset of CKD stage G3a |
| 100 | CKD TTEM : CKD-G3a val | ckd_ttem | eGFR value at the time of first G3a classification |
| 101 | CKD TTEM : CKD-G3b date | ckd_ttem | Date when eGFR first declined to 30–44 mL/min -- onset of CKD stage G3b |
| 102 | CKD TTEM : CKD-G3b val | ckd_ttem | eGFR value at the time of first G3b classification |
| 103 | CKD TTEM : CKD-G4 date | ckd_ttem | Date when eGFR first declined to 15–29 mL/min -- onset of CKD stage G4 |
| 104 | CKD TTEM : CKD-G4 val | ckd_ttem | eGFR value at the time of first G4 classification |
| 105 | CKD TTEM : CKD-G5 date | ckd_ttem | Date when eGFR first declined below 15 mL/min -- onset of CKD stage G5 (kidney failure) |
| 106 | CKD TTEM : CKD-G5 val | ckd_ttem | eGFR value at the time of first G5 classification |
| 107 | CKD TTEM : RRT start date | ckd_ttem | Date of first renal replacement therapy (HD or PD) procedure -- endpoint for CKD time-to-event modelling |
| 108 | CKD uACR | ckd_prog_vm | Most recent urine albumin-to-creatinine ratio (mg/mmol) for albuminuria monitoring in CKD |
| 109 | CKD uACR date | ckd_prog_vm | Date of the most recent uACR measurement |
| 110 | Composite indicating persistence and no assumption violation | ckd | Numeric composite asserting CKD diagnostic confidence: both eGFR and uACR show persistence without assumption violations per KDIGO criteria |
| 111 | Coronary artery disease | cd_cardiac_cad | Binary flag for CAD identified from AMI (STEMI/NSTEMI), other CAD codes, or CABG procedure history |
| 112 | CVA-FDT | cd_cardiac_cad | First documented date of cerebrovascular accident (stroke) used in cardiovascular disease timeline |
| 113 | cvra-legacy adjusted probability | cvra | 5-year cardiovascular risk probability (%) calculated using Framingham equations adjusted for age, sex, cholesterol, HDL, BP, smoking, and diabetes |
| 114 | cvra-legacy category | cvra | Cardiovascular risk category: 1=Low (<10%), 2=Moderate (10–15%), 3=High (≥15% or automatic overrides such as CKD ≥3, TC ≥7, SBP ≥180) |
| 115 | cvra-legacy override | cvra | Binary flag indicating automatic high cardiovascular risk classification due to override conditions (e.g., DM+age≥60, CKD≥3, prior CVD) |
| 116 | Date of birth | $tkc | Patient's date of birth from the demographic record |
| 117 | Date of death | $tkc | Patient's date of death from the demographic record (null if alive) |
| 118 | Default locality | dmg-loc | Numeric locality code derived from the most frequent health centre location over the past 2 years |
| 119 | Definitive Familial Hypercholesterolaemia based on modified DLS | cd_dyslip | Binary flag for definitive FH: modified Dutch Lipid Score >8 (based on LDL level + premature CAD/ASCVD weighting) |
| 120 | Demographic location | dmg_loc | Numeric 5-digit locality code extracted from the patient's most frequent health centre location over the past 2 years |
| 121 | Demographic location: most frequent | dmg_loc | The health centre location where the patient has been seen most frequently, used as the primary demographic locality |
| 122 | Demographic PHC source | dmg_loc | Numeric code identifying the primary health care source/organisation providing the majority of the patient's care |
| 123 | Demography: Aboriginal Ethnicity | dmg | Binary flag indicating Aboriginal ethnicity based on indigenous status code (1 or 3) |
| 124 | Demography: Age | dmg | Patient's age in years calculated as (current date - date of birth) / 365.25 |
| 125 | Demography: Alive with absent DOD | dmg | Binary flag indicating the patient is alive (date of death field is populated but used inversely) |
| 126 | Demography: Date of Birth | dmg | Patient's date of birth from the demographic attribute (dmg_dob) |
| 127 | Demography: Date of Death | dmg | Patient's date of death from the demographic attribute (dmg_dod), null if alive |
| 128 | Demography: Female gender | dmg | Binary flag for female gender (1 if gender=0 in the demographic record) |
| 129 | Demography: Gender [male=1 female=0] | dmg | Numeric gender value from the demographic record: male=1, female=0 |
| 130 | Demography: Potential duplicate client | dmg_eid_alt | Binary flag indicating a possible duplicate patient record exists based on alternative enterprise identifiers |
| 131 | Demography: Torres Strait Islander Ethnicity | dmg | Binary flag indicating Torres Strait Islander ethnicity based on indigenous status code (2 or 3) |
| 132 | Diabetes | cd_dm_dx | Binary flag for prevalent diabetes mellitus (Type 1, 2, or 3c) identified from ICD/ICPC coding, HbA1c ≥6.5%, or diabetic medication use |
| 133 | Diabetes biguanides | cd_dm_rx_rcm | Binary flag indicating the patient is currently prescribed metformin (biguanide, ATC A10BA) |
| 134 | Diabetes GLP1a | cd_dm_rx_rcm | Binary flag indicating the patient is currently prescribed a GLP-1 receptor agonist (ATC A10BJ) |
| 135 | Diabetes GLP1a use in 3 years | cd_dm_rx_rcm | Binary flag indicating the patient has used a GLP-1 receptor agonist within the past 3 years (1080 days) |
| 136 | Diabetes glycaemic control | cd_dm_gly_cntrl | Glycaemic control category based on last HbA1c: 1=<6% (tight), 2=6–8% (acceptable), 3=8–10% (suboptimal), 4=≥10% (poor) |
| 137 | Diabetes HbA1c delta | cd_dm_glyc_ctrl | Change in HbA1c (%) between the two most recent tests; positive=worsening, negative=improving |
| 138 | Diabetes intermittent acting insulin | cd_dm_rx_rcm | Binary flag indicating the patient is currently prescribed intermediate-acting insulin (ATC A10AC) |
| 139 | Diabetes Last HbA1c ngsp | cd_dm_glyc_cntrl | Most recent HbA1c value (NGSP %) within the past 360 days |
| 140 | Diabetes long acting insulin | cd_dm_glyc_cntrl | Binary flag indicating the patient is currently prescribed long-acting insulin (ATC A10AE) |
| 141 | Diabetes management plan | cd_dm_mx | Binary flag indicating documented diabetes management activity: careplan, podiatry review, or diabetes educator review |
| 142 | Diabetes Maximum HbA1c ngsp | cd_dm_glyc_cntrl | Highest recorded HbA1c value (NGSP %) across the patient's history |
| 143 | Diabetes mixed insulin | cd_dm_rx_rcm | Binary flag indicating the patient is currently prescribed mixed (biphasic) insulin preparations |
| 144 | Diabetes mx last careplan | cd_dm_mx | Date of the most recent diabetes-specific careplan documentation |
| 145 | Diabetes mx last diabetic educator review date | cd_dm_mx | Date of the most recent diabetic educator review (MBS item 10951) |
| 146 | Diabetes mx last podiatry review date | cd_dm_mx | Date of the most recent podiatry review for diabetic foot assessment (MBS item 10962) |
| 147 | Diabetes SGLT2i | cd_dm_rx_rcm | Binary flag indicating the patient is currently prescribed an SGLT2 inhibitor (ATC A10BK) |
| 148 | Diabetes short acting insulin | cd_dm_rx_rcm | Binary flag indicating the patient is currently prescribed short/rapid-acting insulin (ATC A10AB) |
| 149 | Diabetes sulphonylurea | cd_dm_rx_rcm | Binary flag indicating the patient is currently prescribed a sulphonylurea (ATC A10BB) |
| 150 | Diabetes Type 3c | cd_dm_dx | Binary flag for secondary (pancreatogenic) diabetes mellitus identified from ICD E09 or ICPC T89003/T89008 coding |
| 151 | Diabetic complications | cd_dm_comp | Binary flag indicating presence of at least one microvascular complication (retinopathy, neuropathy, foot ulcer) or DKA |
| 152 | Diabetic foot ulcer | cd_dm_comp | Binary flag for diabetic foot ulcer identified from ICD E11.73 coding |
| 153 | Diabetic neuropathy | cd_dm_comp | Binary flag for diabetic neuropathy identified from ICD E11.4x or ICPC neuropathy coding |
| 154 | Diabetic retinopathy | cd_dm_comp | Binary flag for diabetic retinopathy (non-proliferative or proliferative) from ICD E10/E11/E13 retinal suffix codes or ICPC F83 |
| 155 | Dialysis (HD) commencement date | rrt_panel_vm | Date of the patient's first haemodialysis session, marking RRT initiation |
| 156 | Dialysis panel 13105 last date | rrt_panel_vm | Date of the most recent MBS item 13105 (chronic disease management) claim for a dialysis patient |
| 157 | Dialysis panel access type | rrt_panel_vm | Numeric code indicating the current dialysis vascular access type (e.g., AVF, CVC, graft) |
| 158 | Dialysis panel attendance | rrt_panel_vm | Percentage attendance rate at scheduled dialysis sessions |
| 159 | Dialysis panel AV plasty | rrt_panel_vm | Date of the most recent arteriovenous fistuloplasty procedure |
| 160 | Dialysis panel diastolic bp mean | rrt_panel_vm | Mean diastolic blood pressure (mmHg) over the past 12 months for a dialysis patient |
| 161 | Dialysis panel HD recency flag | rrt_panel_vm | Binary flag indicating whether the patient has had a recent haemodialysis session |
| 162 | Dialysis panel Labs bicarb | rrt_panel_vm | Most recent serum bicarbonate value (mmol/L) for acid-base monitoring in dialysis |
| 163 | Dialysis panel Labs calcium | rrt_panel_vm | Most recent serum calcium value (mmol/L) for mineral bone disease monitoring in dialysis |
| 164 | Dialysis panel Labs CRP date | rrt_panel_vm | Date of the most recent C-reactive protein (CRP) test for inflammation monitoring in dialysis |
| 165 | Dialysis panel Labs CRP value | rrt_panel_vm | Most recent CRP value (mg/L) for inflammation monitoring in dialysis |
| 166 | Dialysis panel Labs ferritin | rrt_panel_vm | Most recent serum ferritin value (ug/L) for iron stores assessment in dialysis |
| 167 | Dialysis panel Labs Haemoglobin | rrt_panel_vm | Most recent haemoglobin value (g/L) for anaemia monitoring in dialysis |
| 168 | Dialysis panel Labs Haemoglobin change pct | rrt_panel_vm | Percentage change in haemoglobin between the two most recent measurements, indicating trend |
| 169 | Dialysis panel Labs magnesium | rrt_panel_vm | Most recent serum magnesium value (mmol/L) for electrolyte monitoring in dialysis |
| 170 | Dialysis panel Labs phosphate | rrt_panel_vm | Most recent serum phosphate value (mmol/L) for mineral bone disease monitoring in dialysis |
| 171 | Dialysis panel Labs platelets | rrt_panel_vm | Most recent platelet count (x10^9/L) for haematological monitoring in dialysis |
| 172 | Dialysis panel Labs potassium | rrt_panel_vm | Most recent serum potassium value (mmol/L) for electrolyte monitoring in dialysis |
| 173 | Dialysis panel Labs pth | rrt_panel_vm | Most recent parathyroid hormone value (pmol/L) for secondary hyperparathyroidism monitoring in dialysis |
| 174 | Dialysis panel Labs sodium | rrt_panel_vm | Most recent serum sodium value (mmol/L) for electrolyte monitoring in dialysis |
| 175 | Dialysis panel Labs spKTV | rrt_panel_vm | Single-pool Kt/V value measuring dialysis adequacy (target ≥1.2 per KDOQI guidelines) |
| 176 | Dialysis panel Labs tsat | rrt_panel_vm | Most recent transferrin saturation (%) for functional iron assessment in dialysis |
| 177 | Dialysis panel Labs URR | rrt_panel_vm | Urea reduction ratio (%) measuring dialysis adequacy (target ≥65%) |
| 178 | Dialysis panel last clinic | rrt_panel_vm | Date of the most recent outpatient clinic encounter for a dialysis patient |
| 179 | Dialysis panel last hd clinic | rrt_panel_vm | Date of the most recent haemodialysis clinic encounter |
| 180 | Dialysis panel last hospitalisation | rrt_panel_vm | Date of the most recent hospital admission for a dialysis patient |
| 181 | Dialysis panel Meds calcitriol | rrt_panel_vm | Date of the most recent calcitriol (active vitamin D) prescription for mineral bone disease management |
| 182 | Dialysis panel Meds cinacalcet | rrt_panel_vm | Date of the most recent cinacalcet (calcimimetic) prescription for secondary hyperparathyroidism management |
| 183 | Dialysis panel Meds phos_bind | rrt_panel_vm | Date of the most recent phosphate binder prescription for hyperphosphataemia management |
| 184 | Dialysis panel most dialysed satellite facility code | rrt_panel_vm | Facility code of the satellite unit where the patient receives the majority of their dialysis sessions (mode) |
| 185 | Dialysis panel parameter hours | rrt_panel_vm | Actual dialysis session duration (hours) from the most recent treatment |
| 186 | Dialysis panel parameter mode | rrt_panel_vm | Dialysis modality mode: conventional HD vs haemodiafiltration (HDF) |
| 187 | Dialysis panel prescription hours | rrt_panel_vm | Prescribed dialysis session duration (hours) per treatment |
| 188 | Dialysis panel prescription IBW | rrt_panel_vm | Prescribed ideal body weight (kg) used for dialysis adequacy calculations |
| 189 | Dialysis panel pth change pct | rrt_panel_vm | Percentage change in parathyroid hormone between the two most recent measurements |
| 190 | Dialysis panel remote facility code for 13105 | rrt_panel_vm | Facility code associated with the most recent MBS 13105 chronic disease management item for remote dialysis patients |
| 191 | Dialysis panel satellite facility code | rrt_panel_vm | Facility code of the current satellite dialysis unit where the patient receives treatment |
| 192 | Dialysis panel satellite facility location | rrt_panel_vm | Text name of the satellite dialysis facility location |
| 193 | Dialysis panel systolic bp max | rrt_panel_vm | Maximum systolic blood pressure (mmHg) recorded over the past 12 months for a dialysis patient |
| 194 | Dialysis panel systolic bp mean | rrt_panel_vm | Mean systolic blood pressure (mmHg) over the past 12 months for a dialysis patient |
| 195 | Dialysis panel years on dialysis | rrt_panel_vm | Number of years since the patient commenced haemodialysis (calculated from HD start date) |
| 196 | Distinct location over 1y with MBS 715 723 | dmg_loc | Count of distinct health centre locations where MBS 715 or 723 items were claimed in the past year |
| 197 | Encounter with renal services | engmnt_renal | Binary flag indicating the patient has had at least one encounter with renal specialist services |
| 198 | Evolocumab Prescribed | cd_dyslip | Binary flag indicating the patient is currently prescribed evolocumab (PCSK9 inhibitor) for lipid lowering |
| 199 | Ezetimibe Prescribed | cd_dyslip | Binary flag indicating the patient is currently prescribed ezetimibe for lipid lowering |
| 200 | Gender | $tkc | Patient's gender from the TKC demographic record (male=1, female=0) |
| 201 | Given names | $tkc | Patient's given name(s) from the TKC demographic record |
| 202 | Glomerulonephritis GN Acute or Chronic | ckd_c_gn | Binary flag for any glomerulonephritis (acute or chronic) identified from ICD N00–N08, ICPC U88, or M32.14 coding |
| 203 | Glomerulonephritis GN Chronic | ckd_c_gn | Binary flag for chronic glomerulonephritis identified from ICD N01–N08, ICPC U88, or M32.14 coding |
| 204 | Glomerulonephritis GN Nephritic | ckd_c_gn | Binary flag for nephritic presentation (haematuria-predominant) from ICD N00–N03, N05, N07 coding |
| 205 | Glomerulonephritis GN Nephrotic | ckd_c_gn | Binary flag for nephrotic presentation (proteinuria-predominant) from ICD N04 or N06 coding |
| 206 | Graft function known and therapy | rrt_tx | Binary flag indicating the transplant recipient has documented graft function (creatinine available) and is on immunosuppressive therapy |
| 207 | HDL cholesterol concentration | cd_dyslip | Most recent HDL cholesterol value (mmol/L) within the past 12 months |
| 208 | Health Centre (most frequent) | $tkc | The health centre where the patient has been seen most frequently across their history |
| 209 | Health Centre (most recent) | $tkc | The health centre where the patient was most recently seen |
| 210 | High CVR | cvra | Binary flag indicating the patient is classified as high cardiovascular risk (≥15% 5-year risk or automatic override criteria met) |
| 211 | HRN | $tkc | Patient's Hospital Registration Number, zero-padded to 7 digits |
| 212 | Hypercholesteraemia | cd_dyslip | Binary flag for hypercholesterolaemia: LDL >4.9 mmol/L, or LDL >1.8 with ASCVD, or coded dyslipidaemia (ICD E78/ICPC T93), or FH detected |
| 213 | Hyperkalaemia in CKD | ckd_complications | Binary flag for serum potassium ≥6.0 mmol/L in CKD stage ≥3 |
| 214 | Hyperphosphataemia due to CKD | ckd_complications | Binary flag for serum phosphate ≥2.0 mmol/L in CKD stage ≥3, indicating CKD-mineral bone disease |
| 215 | Hypertension | ckd_htn | Binary flag for hypertension from ICD I10/I15, ICPC K85–K87, or ≥3 systolic BP readings >140 mmHg within 2 years |
| 216 | Hypoalbuminaemia in CKD | ckd_complications | Binary flag for serum albumin <32 g/L in CKD stage ≥3, indicating protein-energy wasting or nephrotic losses |
| 217 | IHI | $tkc | Patient's Individual Healthcare Identifier (national identifier) |
| 218 | Incident Diabetes Mellitus | cd_dm_dx | Binary flag for newly diagnosed diabetes within the past 12 months (first diabetes evidence within last year) |
| 219 | Incident Haemodialysis | rrt | Binary flag for new haemodialysis commencement within the past 12 months (first HD date within last year and ≥10 sessions) |
| 220 | Incident Hypertension | cd_htn | Binary flag for newly diagnosed hypertension within the past 12 months |
| 221 | Incident Peritoneal Dialysis | rrt | Binary flag for new peritoneal dialysis commencement within the past 12 months |
| 222 | Incident Peritoneal or Haemodialysis | rrt | Binary flag for new commencement of any dialysis modality (HD or PD) within the past 12 months |
| 223 | Is Active in the last 2 years | at_risk | Binary flag indicating clinical activity (any ICD, ICPC, lab, medication, or observation data) within the past 2 years and not deceased |
| 224 | Is deceased | $tkc | Binary flag indicating the patient has a recorded date of death |
| 225 | Is location active | dmg_loc | Binary flag indicating the patient's demographic location has been active (mode location recorded) within the past 24 months |
| 226 | Last Fibroscan Date | cd_cirrhosis | Date of the most recent transient elastography (FibroScan) examination for liver fibrosis assessment |
| 227 | Last Fibroscan Value | cd_cirrhosis | Most recent FibroScan stiffness value (kPa) for non-invasive liver fibrosis staging |
| 228 | LDL cholesterol concentration | cd_dyslip | Most recent LDL cholesterol value (mmol/L) within the past 12 months |
| 229 | LDL gt 5 threshold | cd_dyslip | Count of LDL cholesterol values exceeding 5.0 mmol/L in the past 5 years, supporting familial hypercholesterolaemia assessment |
| 230 | Left or Right Hemicolectomy | sx_abdo | Binary flag for left or right hemicolectomy procedure identified from CARESYS surgical procedure codes |
| 231 | Likely secondary hyperparathyroidism due to CKD | ckd_complications | Binary flag for PTH ≥63 pmol/L in CKD stage ≥3, indicating secondary hyperparathyroidism due to CKD-mineral bone disease |
| 232 | Loss of Weight | cd_nutr_low | Binary flag for significant unintended weight loss: baseline BMI <20 with >10% weight loss over 6–24 months |
| 233 | MACE-FDT | cd_cardiac_cad | First documented date of a major adverse cardiovascular event (AMI, stroke, or cardiovascular death) |
| 234 | MBS 705 Long Health Assessment Last date | mbs_billing_history | Date of the most recent MBS item 705 (long health assessment) claim |
| 235 | MBS 715 Health Assessment Last date | mbs_billing_history | Date of the most recent MBS item 715 (Aboriginal and Torres Strait Islander health assessment) claim |
| 236 | MBS 721 GPMP Last date | mbs_billing_history | Date of the most recent MBS item 721 (GP Management Plan) claim |
| 237 | MBS 723 Team care arrangement Last date | mbs_billing_history | Date of the most recent MBS item 723 (Team Care Arrangement) claim |
| 238 | MBS 732 Review GPMP Last date | mbs_billing_history | Date of the most recent MBS item 732 (review of GP Management Plan) claim |
| 239 | Mean diastolic bp over 1 year | cd_htn_bp_control | Mean diastolic blood pressure (mmHg) calculated from all readings over the past 12 months |
| 240 | Mitral valve insufficiency | cd_cardiac_vhd | Binary flag for mitral valve regurgitation/insufficiency from ICD I05.1/I05.2/I34.0 or ICPC K83 coding |
| 241 | Mitral valve replacement | cd_cardiac_vhd | Binary flag for surgical mitral valve replacement identified from ICPC K54009 coding |
| 242 | Mitral valve stenosis | cd_cardiac_vhd | Binary flag for mitral valve stenosis from ICD I05.0/I05.2/I34.2 or ICPC K73/K83/K71 coding |
| 243 | Most Frequent Health Centre | global | The health centre where the patient has been seen most frequently, used as the default demographic location |
| 244 | Most recent Health Centre | global | The health centre where the patient was most recently seen across all encounters |
| 245 | Native kidney biopsy | ckd_diagnostics | Binary flag indicating a native kidney biopsy has been performed (histopathology result or imaging-guided biopsy documented) |
| 246 | Non-steroidal MRA | tg4630 | Binary flag indicating the patient is currently prescribed a non-steroidal mineralocorticoid receptor antagonist (e.g., finerenone) |
| 247 | Non-steroidal MRA Eligible for CKD | tg4630 | Binary flag indicating the patient with proteinuric CKD is eligible for non-steroidal MRA therapy per guideline criteria |
| 248 | NSTEMI-FDT | cd_cardiac_cad | First documented date of a non-ST-elevation myocardial infarction |
| 249 | Nursing home resident | dmg_residency | Binary flag indicating the patient is a nursing home resident, identified from MBS item 731 claims within the past 730 days |
| 250 | Obesity | cd_obesity | Binary flag for obesity defined as BMI >30 kg/m2, calculated from measured weight and height |
| 251 | Origin PHC District | dmg_loc_origin | Two-digit district code extracted from the patient's origin primary health care location (first MBS 715/723/13105 record) |
| 252 | Origin PHC Locality | dmg_loc_origin | One-digit locality code extracted from the patient's origin primary health care location |
| 253 | Origin PHC Location | dmg_loc_origin | Numeric location code for the patient's origin primary health care centre (where first MBS 715/723/13105 was claimed) |
| 254 | Origin PHC Location code | dmg_loc_origin | String location code for the patient's origin primary health care centre |
| 255 | Origin PHC Region | dmg_loc_origin | One-digit region code extracted from the patient's origin primary health care location |
| 256 | Origin PHC Source | dmg_loc_origin | Two-digit source code identifying the primary health care organisation at the patient's origin location |
| 257 | PD in the past | rrt | Binary flag indicating the patient has previously been on peritoneal dialysis but is no longer on PD (historical modality) |
| 258 | PD start date | rrt | Date of the patient's first peritoneal dialysis procedure |
| 259 | Possible Familial Hypercholesterolaemia based on modified DLS | cd_dyslip | Binary flag for possible FH: modified Dutch Lipid Score 3–5 (based on LDL level + premature CAD/ASCVD weighting) |
| 260 | Prescribed ARNI | cd_cardiac_ccf | Binary flag indicating the patient is prescribed sacubitril/valsartan (ARNI, ATC C09DX04) for heart failure |
| 261 | Presence of AF | cd_cardiac_af | Binary flag for atrial fibrillation from ICD I48 or ICPC K78 coding, with CHA2DS2-VASc score calculated if non-valvular |
| 262 | Presence of amputation | ortho_amputation | Binary flag for limb amputation from prosthetic clinic encounters, ICD Y83.5, ICPC A87010, or CARESYS amputation procedure codes |
| 263 | Presence of Antiphospholipid syndrome | cd_rheum_aps | Binary flag for antiphospholipid syndrome from ICD D68.61 or ICPC B83021 coding |
| 264 | Presence of breast carcinoma | ca_breast | Binary flag for breast carcinoma from ICD C50 or ICPC X76 coding (first occurrence date) |
| 265 | Presence of cardiac device | cd_cardiac_device | Binary flag for cardiac device (permanent pacemaker or ICD) from ICPC K54001 or CARESYS procedure codes |
| 266 | Presence of cardiac investigations | cd_cardiac_ix | Binary flag indicating the patient has had echocardiography or coronary angiography documented |
| 267 | Presence of CHF | cd_cardiac_chf | Binary flag for congestive heart failure or cardiomyopathy from ICD I42/I50, ICPC K77, or ARNI prescription |
| 268 | Presence of Chronic Hepatitis C | id_hcv | Binary flag for chronic hepatitis C from ICPC D72008 or ICD B18.2 coding |
| 269 | Presence of Cirrhosis | cd_cirrhosis | Binary flag for cirrhosis from ICD K70.3 (alcoholic), K71.7 (toxic), K74 (fibrosis/cirrhosis), or ICPC D97 coding |
| 270 | Presence of colorectal carcinoma | ca_crc | Binary flag for colorectal carcinoma from ICD C18/C19/C20 or ICPC D75 coding (first occurrence date) |
| 271 | Presence of covid 19 infection | id_covid19 | Binary flag for COVID-19 infection from ICPC R83015 coding |
| 272 | Presence of cryptococcal infection | id_cap | Binary flag for cryptococcal infection from ICD B45.0 coding |
| 273 | Presence of Dementia | cd_cns | Binary flag for dementia from ICD F01/F02/F03 or ICPC P70/P15 coding |
| 274 | Presence of dilated cardiomyopathy | cd_cardiac_chf | Binary flag for dilated cardiomyopathy from ICD I42.0 coding |
| 275 | Presence of endometrial carcinoma | ca_endometrial | Binary flag for endometrial carcinoma from ICD C54.1 coding (first occurrence date) |
| 276 | Presence of Epilepsy | cd_cns | Binary flag for epilepsy from ICD G40 or ICPC N88 coding |
| 277 | Presence of Extradural Haemorrhages | cd_cns_ch | Binary flag for extradural haemorrhage from ICPC N80010 or ICD I62.1 coding |
| 278 | Presence of fractures | ortho_fractures | Binary flag for pelvic fracture from ICD S32.1 coding |
| 279 | Presence of Gout | cd_rheum_gout | Binary flag for gout from ICD M10, ICPC T92001, or xanthine oxidase inhibitor (allopurinol) use |
| 280 | Presence of haematological disease | cd_haem | Binary flag for cytopenias: Hb <100 g/L, or WCC <1.5 x10^9/L, or platelets <100 x10^9/L |
| 281 | Presence of HTLV1-2 | id_htlv | Binary flag for HTLV-1/2 infection from positive serology (lab_bld_htlv=1) or ICD B97.33 coding |
| 282 | Presence of hypertrophic cardiomyopathy | cd_cardiac_chf | Binary flag for hypertrophic cardiomyopathy from ICD I42.1/I42.2 coding |
| 283 | Presence of intracerebral haemorrhage | cd_cns_ch | Binary flag for intracerebral haemorrhage from ICPC N80008/N80015 or ICD I61 coding |
| 284 | Presence of lung carcinoma | ca_lung | Binary flag for lung carcinoma from ICD C34 or ICPC R84 coding (first occurrence date) |
| 285 | Presence of melanoma | ca_skin_melanoma | Binary flag for melanoma from ICD C43 or ICPC S77003 coding (first occurrence date) |
| 286 | Presence of metastatic carcinoma | ca_mets | Binary flag for metastatic disease from ICD C77–C80 (bone, CNS, liver, lung, peritoneal, nodal) or ICPC A79009 |
| 287 | Presence of misc carcinoma | ca_misc | Binary flag for any malignancy (ICD C%) not captured by the specific organ carcinoma ruleblocks |
| 288 | Presence of Non Valvular AF | cd_cardiac_af | Binary flag for non-valvular AF (AF present without valvular heart disease), used for CHA2DS2-VASc scoring |
| 289 | Presence of ovarian carcinoma | ca_ovarian | Binary flag for ovarian carcinoma from ICD C56 or ICPC X77006 coding (first occurrence date) |
| 290 | Presence of Parkinsons disease | cd_cns | Binary flag for Parkinson's disease from ICPC N87 coding with N04 antiparkinsonian medication use |
| 291 | Presence of PD catheter | rrt_pd | Binary flag for peritoneal dialysis catheter in situ from CARESYS procedure codes 1310900/1310901 |
| 292 | Presence of prostate carcinoma | ca_prostate | Binary flag for prostate carcinoma from ICD C61 or ICPC Y77 coding (first occurrence date) |
| 293 | Presence of recurrent soft tissue infection | id_sti | Binary flag for recurrent soft tissue infection: ICD L0 or ICPC S10/S76 with multiple episodes spanning >1 year |
| 294 | Presence of recurrent UTI | id_uti | Binary flag for recurrent UTI: episodes spanning >90 days apart or recurrent UTI ICPC codes U71014/U71015 |
| 295 | Presence of renal cell carcinoma | ca_rcc | Binary flag for renal cell carcinoma from ICD C64 or ICPC U75003 coding (first occurrence date) |
| 296 | Presence of respiratory infection requiring hospitalisation | id_cap | Binary flag for CAP or severe respiratory infection requiring hospitalisation: viral (J09–J12), bacterial (J13–J14), NOS (J18), or melioidosis |
| 297 | Presence of restrictive cardiomyopathy | cd_cardiac_chf | Binary flag for restrictive cardiomyopathy from ICD I42.5 coding |
| 298 | Presence of Rheumatoid arthritis | cd_rheum_ra | Binary flag for rheumatoid arthritis from ICD M05 or ICPC L88004 coding |
| 299 | Presence of SLE | cd_rheum_sle | Binary flag for systemic lupus erythematosus from ICD M32 or ICPC L99056/L99065 coding |
| 300 | Presence of solid organ carcinoma | ca_solid | Binary flag for any solid organ carcinoma: composite of breast, prostate, RCC, CRC, lung, thyroid, endometrial, ovarian, or metastatic disease |
| 301 | Presence of Subdural Haemorrhage | cd_cns_ch | Binary flag for subdural haemorrhage from ICPC N80001/N80004 or ICD I62.0 coding |
| 302 | Presence of thyroid carcinoma | ca_thyroid | Binary flag for thyroid carcinoma from ICD C37 or ICPC T71 coding (first occurrence date) |
| 303 | Presence of tuberculosis | id_tb | Binary flag for active or latent TB from ICPC A700, ICD M49 (spinal TB), J65 (TB sequelae), or ICPC A70J99 (latent TB) |
| 304 | Presence of Vasculitis | cd_imm_vasculitis | Binary flag for systemic vasculitis: GPA (M31.3), giant cell arteritis (M31.5/M31.6), MPO-ANCA (M31.7), or Takayasu (M31.4) |
| 305 | Prevalent arteriovenous fistula for haemodialysis | ckd_access | Binary flag indicating a functioning AVF exists for haemodialysis access from CARESYS, ICD Z49.0, or ICPC K99049 |
| 306 | Prevalent Diabetes Mellitus | cd_dm_dx | Binary flag for prevalent (established) diabetes mellitus -- patient has existing DM diagnosis of any type |
| 307 | Prevalent Hypertension | cd_htn | Binary flag for prevalent (established) hypertension -- patient has existing hypertension diagnosis |
| 308 | Prevalent smoker | at_risk | Binary flag for current smoking status, derived from smoking status code ≥29 in the clinical record |
| 309 | Previous atherosclerotic vascular disease | cd_dyslip | Binary flag for prior ASCVD (CAD, stroke, or PVD), used to determine aggressive LDL targets (≤1.8 mmol/L) |
| 310 | Probable Familial Hypercholesterolaemia based on modified DLS | cd_dyslip | Binary flag for probable FH: modified Dutch Lipid Score 6–8 (based on LDL level + premature CAD/ASCVD weighting) |
| 311 | RAAS | tg4630 | Binary flag indicating the patient is currently prescribed a RAAS inhibitor (ACE inhibitor ATC C09AA or ARB ATC C09CA) |
| 312 | RAAS Eligible for CKD | tg4630 | Binary flag indicating the patient with proteinuric CKD is eligible for RAAS inhibitor therapy per guideline criteria |
| 313 | Renal Referral from Primary care | engmnt_renal | Binary flag indicating a referral to nephrology/renal services has been made from primary care |
| 314 | Renal services interaction | ckd_journey | Binary flag indicating meaningful interaction with renal services: initial education, review education, or first encounter documented (non-RRT patients) |
| 315 | Renal structural anatomical anomaly | ckd_c_rnm | Binary flag for structural or genetic renal anomalies: agenesis (Q60), cystic (Q61), obstructive (Q62), malformations (Q63/Q64), neoplasm (C64), or post-nephrectomy (Z90.5) |
| 316 | Renal supportive care | ckd_careplan | Binary flag indicating the patient is on a renal supportive (conservative) care pathway from ICPC U59011 |
| 317 | Renal supportive care Last date | ckd_careplan | Date of the most recent renal supportive care documentation |
| 318 | Renal Transplant multi-parity | rrt | Binary flag indicating the transplant recipient has had multiple transplants (>10 transplant-related procedure codes) |
| 319 | Renal Tubulo-interstitial disease chronic | ckd_c_tid | Binary flag for chronic tubulo-interstitial kidney disease from ICD N11–N16 or N25 coding |
| 320 | Rheumatic heart disease | cd_cardiac_rhd | Binary flag for rheumatic heart disease from ICD I05–I09 or ICPC K71 coding |
| 321 | Rheumatic heart disease (VHD) | cd_cardiac_vhd | Binary flag for rheumatic heart disease as the aetiology of valvular heart disease from ICD I05–I09 or ICPC K71 |
| 322 | RRT Haemodialysis | rrt | Binary flag indicating the patient is currently on in-centre haemodialysis (RRT modality = HD) |
| 323 | RRT Home Haemodialysis | rrt | Binary flag indicating the patient is currently on home haemodialysis (RRT modality = HHD) |
| 324 | RRT Peritoneal Dialysis | rrt | Binary flag indicating the patient is currently on peritoneal dialysis (RRT modality = PD) |
| 325 | RRT Transplant | rrt | Binary flag indicating the patient has a functioning renal transplant (RRT modality = TX) |
| 326 | Rx cardiac meds | cd_cardiac_rx | Binary flag indicating the patient is prescribed cardiac medications: statins, diuretics, chronotropes, anticoagulants, or antiplatelets |
| 327 | Screened by BP uACR and eGFR within last 1y as per recommendations | at_risk | Count (0–3) of recommended CKD screening tests (eGFR, uACR, blood pressure) completed within the past 12 months |
| 328 | Screened by blood pressure within last 1 year | at_risk | Binary flag indicating a blood pressure measurement within the past 12 months |
| 329 | Screened by eGFR within last 1 year | at_risk | Binary flag indicating an eGFR test within the past 12 months |
| 330 | Screened by HbA1c within the last 1y | at_risk | Binary flag indicating an HbA1c test within the past 12 months |
| 331 | Screened by uACR within last 1y | at_risk | Binary flag indicating a uACR test within the past 12 months |
| 332 | SGLT2i | tg4630 | Binary flag indicating the patient is currently prescribed an SGLT2 inhibitor (ATC A10BK) |
| 333 | SGLT2i Eligible for CKD | tg4630 | Binary flag indicating the patient with proteinuric CKD is eligible for SGLT2i therapy per guideline criteria |
| 334 | Smoking current NRT use | cd_smoking | Binary flag indicating the patient is currently using nicotine replacement therapy (NRT) |
| 335 | Smoking Status | cd_smoking | Numeric smoking status code from the clinical record, used to classify current/former/never smoker |
| 336 | Statin Prescribed | cd_dyslip | Binary flag indicating the patient is currently prescribed a statin for lipid-lowering therapy |
| 337 | STEMI-FDT | cd_cardiac_cad | First documented date of a ST-elevation myocardial infarction |
| 338 | Steroidal MRA | tg4630 | Binary flag indicating the patient is currently prescribed a steroidal MRA (e.g., spironolactone, ATC C03DA) |
| 339 | Stroke | cd_cva | Binary flag for cerebrovascular accident (haemorrhagic or thromboembolic) from ICD I60–I67 or ICPC K89/K90/K91 coding |
| 340 | Surname | $tkc | Patient's surname from the TKC demographic record |
| 341 | TKC category | at_risk | TKC population category: 1=CKD or RRT (kidney disease confirmed), 2=At risk (risk factors, no CKD), 3=Other |
| 342 | TKC Category 2 label | at_risk | Human-readable label for the TKC category (e.g., "At risk", "CKD stage 3a", "Haemodialysis", "Transplant") |
| 343 | TKC cohort | at_risk | Binary flag indicating the patient belongs to the TKC cohort: active within 2 years AND has CKD, RRT, or at-risk status |
| 344 | Total cholesterol concentration | cd_dyslip | Most recent total cholesterol value (mmol/L) within the past 12 months |
| 345 | Total cholesterol test date | cd_dyslip | Date of the most recent total cholesterol test |
| 346 | transplant_panel: active followup within 90 days | rrt_tx | Binary flag indicating the transplant recipient has had an outpatient clinic visit within the past 90 days |
| 347 | transplant_panel: last clinic date | rrt_tx | Date of the most recent outpatient clinic encounter for the transplant recipient |
| 348 | transplant_panel: last creatinine date | rrt_tx | Date of the most recent serum creatinine measurement for graft function monitoring |
| 349 | transplant_panel: last creatinine value | rrt_tx | Most recent serum creatinine value (umol/L) for transplant graft function monitoring |
| 350 | transplant_panel: last everolimus date | rrt_tx | Date of the most recent everolimus therapeutic drug monitoring (TDM) level |
| 351 | transplant_panel: last everolimus value | rrt_tx | Most recent everolimus trough level (ug/L) for immunosuppression monitoring |
| 352 | transplant_panel: last tacrolimus date | rrt_tx | Date of the most recent tacrolimus TDM level |
| 353 | transplant_panel: last tacrolimus value | rrt_tx | Most recent tacrolimus trough level (ug/L) for immunosuppression monitoring |
| 354 | transplant_panel: last transplant date | rrt_tx | Date of the patient's most recent renal transplant procedure |
| 355 | Treated with ACEi | cd_htn | Binary flag indicating the patient is prescribed an ACE inhibitor (ATC C09AA) for hypertension |
| 356 | Treated with ARB | cd_htn | Binary flag indicating the patient is prescribed an angiotensin receptor blocker (ATC C09CA) for hypertension |
| 357 | Treated with Beta blocker | cd_htn | Binary flag indicating the patient is prescribed a beta-blocker (ATC C07) for hypertension |
| 358 | Treated with Calcium channel blocker | cd_htn | Binary flag indicating the patient is prescribed a calcium channel blocker (ATC C08) for hypertension |
| 359 | Treated with Centrally acting agent | cd_htn | Binary flag indicating the patient is prescribed a centrally acting antihypertensive (ATC C02) |
| 360 | Treated with loop diuretic | cd_htn | Binary flag indicating the patient is prescribed a loop diuretic (ATC C03C) for hypertension/fluid management |
| 361 | Treated with thiazide diuretic | cd_htn | Binary flag indicating the patient is prescribed a thiazide diuretic (ATC C03AA) for hypertension |
| 362 | Triglyceride concentration | cd_dyslip | Most recent triglyceride value (mmol/L) within the past 12 months |
| 363 | Valvular Heart Disease | cd_cardiac_vhd | Binary flag for any valvular heart disease: mitral, aortic, or tricuspid valve pathology (stenosis, insufficiency, or replacement) |
| 364 | Visible in TKC app | global | Binary flag indicating the patient meets visibility criteria for display in the Territory Kidney Care application |
| 365 | VTE | cd_cardiac_vte | Binary flag for venous thromboembolism: PE (ICD I26), DVT (I82.2/I82.3/I82.9), Budd-Chiari (I82.0), or SVT (I82.8) |
