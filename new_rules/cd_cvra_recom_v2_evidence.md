# cd_cvra_recom_v2 — evidence traceability table

Companion to [`cd_cvra_recom_v2.prb`](./cd_cvra_recom_v2.prb). One row per conditional branch in the rule, mapped to the primary trial / guideline source and a concordance flag.

**Concordance legend**
- ✓ **Aligned** — direct, unambiguous match to the cited guideline.
- ⚠ **Extrapolated** — defensible reading of guideline intent but the threshold or cut-off is not stated verbatim.
- ✗ **No direct guideline** — investigator / pragmatic choice; needs explicit clinician sign-off.
- 🔍 **Verify** — likely supported but I have not personally confirmed the citation; for committee review.

**Evidence-grade abbreviations**
- AU 2023: NHMRC grade A/B/C/D, or *Practice point* (PP).
- ESC / AHA-ACC: Class of recommendation (I, IIa, IIb, III) + Level of evidence (A/B/C).
- KDIGO: 1 = strong, 2 = weak; level A–D.
- *NS* = not stated in cited source.

References cited as short codes — full URLs at the bottom.

---

## 1. Risk reconciliation (auto-high overrides + uplift)

| # | Recommendation | Trigger / threshold | Picorules variable | Primary evidence | Guideline | LoE | Concordance |
|---|---|---|---|---|---|---|---|
| 1.1 | Auto-classify HIGH risk — established CVD | `cvd_prev = 1` | `clin_high_risk` cl.1 | Secondary-prevention paradigm; multiple meta-analyses (statin, antiplatelet) | AU 2023 Step 2; ESC 2021 CV Prevention | AU PP / ESC I-A | ✓ |
| 1.2 | Auto-classify HIGH risk — moderate-severe CKD | `ckd >= 3` (eGFR < 45 or persistent uACR) | `clin_high_risk` cl.2 | CKD as CHD-risk equivalent (Tonelli 2012 *Lancet*) | AU 2023 Step 2; KDIGO 2024 | AU PP / KDIGO 1B | ✓ |
| 1.3 | Auto-classify HIGH risk — familial hypercholesterolaemia | `fhc_prob >= 2` (Dutch Lipid Clinic Score ≥ possible) | `clin_high_risk` cl.3 | DLCN criteria (Nordestgaard 2013 *Eur Heart J*); SAFEHEART | AU 2023 Step 2; ESC/EAS 2019 | AU PP / ESC I-C | ⚠ — guideline says "confirmed FH"; rule fires on DLCN "possible" (≥2), which is a screening flag not a diagnosis. Consider raising threshold to `fhc_prob >= 3` (probable). |
| 1.4 | Auto-classify HIGH risk — T2DM + end-organ damage | `dm = 1 AND dm_eod = 1` | `clin_high_risk` cl.4 | UKPDS micro/macrovascular linkage; ADVANCE | ESC 2023 Diabetes; AU 2023 (DM + retinopathy/neuropathy as risk uplift) | ESC I-A | ⚠ — AU 2023 lists DM with end-organ damage as a *reclassification factor*, not a Step-2 auto-high. Behaviour is similar but the formal path differs. |
| 1.5 | Auto-classify HIGH risk — persistent albuminuria | uACR > 25 (M) / > 35 (F), ≥2 readings, span ≥ 90 days | `albuminuria_persistent_au` → `clin_high_risk` cl.5 | KDIGO heat-map; meta-analysis Matsushita 2010 | AU 2023 reclassification factor; KDIGO 2024 | AU C / KDIGO 1A | ✓ (sex-banded thresholds taken from AU 2023 calculator inputs) |
| 1.6 | Uplift +1 risk category | First Nations AND age 30–79 AND ensemble in Low/Intermediate | `fnp_uplift` | Cross-sectional FNP excess CVD risk (AIHW; D'Onise 2020) | AU 2023 reclassification factor (FNP) | AU PP | ⚠ — guideline specifies FNP-specific calculator, not a generic +1 uplift. Interim heuristic until FNP equation binding exists. |

---

## 2. Blood pressure — targets

| # | Recommendation | Trigger / threshold | Picorules variable | Primary evidence | Guideline | LoE | Concordance |
|---|---|---|---|---|---|---|---|
| 2.1 | SBP target **< 140** mmHg | age ≥ 80 | `sbp_target` cl.1 | HYVET 2008 *NEJM*; STEP 2021 | AHA/ACC 2025 (age ≥ 75 + frailty); AU 2023 silent on age carve-out | AHA IIa-B | ⚠ — AU 2023 does not specify an age-banded relaxation; AHA uses age 75 + frailty assessment. Rule uses age 80 as a numeric proxy. |
| 2.2 | SBP target **< 130 / 80** mmHg | everyone else | `sbp_target` else | SPRINT; ACCORD-BP follow-up; STEP; National Hypertension Taskforce (MJA 2024) | **AU 2023 ✓**; AHA/ACC 2025 | AU PP / AHA I-A | ✓ — verbatim AU 2023 endorsement: "less than 130/80 mmHg for most patients". |

## 3. Blood pressure — recommendation engine

### 3.A Overrides (treat irrespective of calculated risk)

| # | Recommendation | Trigger | Picorules variable | Primary evidence | Guideline | LoE | Concordance |
|---|---|---|---|---|---|---|---|
| 3.1 | **Initiate** BP Rx — override | SBP ≥ 160 OR DBP ≥ 100, no current Rx | `recom_rx_bp` cl.1 | Decades of RCT evidence in stage-2 HTN | AU 2023 Step 5; AHA 2025 | AHA I-A | ✓ |
| 3.2 | **Intensify** BP Rx — override | SBP ≥ 160 OR DBP ≥ 100, on Rx | `recom_rx_bp` cl.2 | Treat-to-target trials | AU 2023; AHA 2025 | I-A | ✓ |

### 3.B Decision matrix (`recom_rx_bp` clauses 3–8 + else)

Action emitted is a function of risk category × current therapy × target status. All cells share the same evidence base: **SPRINT (high-risk benefit), HOPE-3 (intermediate-risk benefit), AU 2023 / AHA 2025 treat-to-target principle**. Targets per Section 2.

|  | **No current Rx** | **On Rx · SBP above target** | **On Rx · SBP at target** |
|---|---|---|---|
| **High risk** (`cvra_cat_r = 3`) | Initiate | Intensify | Maintain |
| **Intermediate** (`cvra_cat_r = 2`) | Consider ⚠ | Intensify | Maintain |
| **Low risk** (`cvra_cat_r ≤ 1`) | Not indicated | — | — |

| Cell | Picorules clause | LoE | Notes |
|---|---|---|---|
| High · initiate | `recom_rx_bp` cl.3 | AU B (SPRINT) | ✓ |
| High · intensify | cl.4 | AU B | ✓ |
| High · maintain | cl.5 | — | ✓ status code |
| Intermediate · consider | cl.6 | AU C (HOPE-3) | ⚠ AU language is "consider *after* lifestyle"; rule has no lifestyle precondition |
| Intermediate · intensify | cl.7 | AU PP | ✓ |
| Intermediate · maintain | cl.8 | — | ✓ status code |
| Low · not indicated | else | AU PP | ✓ avoids polypharmacy harm in low-risk |

---

## 4. Lipid — targets

| # | Recommendation | Trigger / threshold | Picorules variable | Primary evidence | Guideline | LoE | Concordance |
|---|---|---|---|---|---|---|---|
| 4.1 | LDL target **< 1.8** mmol/L | established CVD (secondary prevention) | `ldl_target` cl.1 | IMPROVE-IT 2015 *NEJM*; FOURIER 2017 | AU 2023; AHA/ACC 2018 cholesterol | AHA I-A | ✓ |
| 4.2 | LDL target **< 2.0** mmol/L | high risk (primary prevention) | `ldl_target` cl.2 | JUPITER 2008; meta-analysis CTT 2010 | AU 2023 | AU B | ✓ — AU target; **ESC/EAS 2019/2025 is tighter (< 1.4 mmol/L)** with class I-A. |

## 5. Lipid — recommendation engine (extended ladder)

### 5.A Overrides (treat irrespective of calculated risk)

| # | Recommendation | Trigger | Picorules variable | Primary evidence | Guideline | LoE | Concordance |
|---|---|---|---|---|---|---|---|
| 5.1 | **Initiate** statin — override | TC ≥ 7.5 mmol/L, no statin | `recom_rx_lipid` cl.1 | Mendelian randomisation; statin trials in severe hypercholesterolaemia | AU 2023 Step 5 | AU PP | ✓ |
| 5.2 | **Intensify** (add ezetimibe) — override | TC ≥ 7.5, on statin | `recom_rx_lipid` cl.2 | IMPROVE-IT 2015 | AU 2023 | AU B | ✓ |

### 5.B Decision matrix (`recom_rx_lipid` clauses 3–8 + else)

The high-risk arm is a **ladder**: each step has its own pivotal trial. Intermediate/low arms are simpler. Targets per Section 4.

|  | **No lipid Rx** | **Statin only · above target** | **Statin + ezetimibe · above target** | **At target / on Rx** |
|---|---|---|---|---|
| **High risk** (`cvra_cat_r = 3`) | Initiate statin | Add ezetimibe | Add non-statin intensifier | Maintain |
| **Intermediate** (`cvra_cat_r = 2`) | Consider statin | (no formalised step) | (no formalised step) | Maintain |
| **Low risk** (`cvra_cat_r ≤ 1`) | Not indicated | — | — | — |

| Cell | Picorules clause (code) | Primary evidence | LoE | Concordance |
|---|---|---|---|---|
| High · initiate statin | cl.3 (code 1) | CTT meta-analyses; JUPITER | I-A | ✓ |
| High · add ezetimibe | cl.5 (code 3) | IMPROVE-IT 2015 | I-B | ✓ |
| High · add non-statin intensifier (bempedoic acid / PCSK9i / inclisiran) | cl.4 (code 5) | FOURIER (evolocumab); ODYSSEY OUTCOMES (alirocumab); ORION-10/11 (inclisiran); CLEAR Outcomes (bempedoic acid) | ESC I-A | ⚠ AU 2023 lists agents but does not specify the ladder order; sequencing extrapolated from ESC/EAS 2025. |
| High · maintain | cl.6 (code 4) | — | — | ✓ status code |
| Intermediate · consider statin | cl.7 (code 2) | HOPE-3 (rosuvastatin 10 mg) | AU B | ✓ |
| Intermediate · maintain | cl.8 (code 4) | — | — | ✓ status code |
| Low · not indicated | else (code 0) | — | AU PP | ✓ |

---

## 6. Antiplatelet — secondary prevention only

| # | Recommendation | Trigger / threshold | Picorules variable | Primary evidence | Guideline | LoE | Concordance |
|---|---|---|---|---|---|---|---|
| 6.1 | **Initiate** antiplatelet | established CVD, not on antiplatelet or anticoag | `recom_rx_antiplatelet` cl.1 | Antithrombotic Trialists' Collaboration 2009 *Lancet*; CAPRIE | AHA/ACC secondary-prevention; AU 2023 | I-A | ✓ |
| 6.2 | **Maintain** | established CVD, already on antiplatelet or anticoag | `recom_rx_antiplatelet` cl.2 | — | AHA/ACC | I-A | ✓ |

---

## 7. SGLT2i / GLP-1 RA — cardio-renal protection in T2DM

| # | Recommendation | Trigger / threshold | Picorules variable | Primary evidence | Guideline | LoE | Concordance |
|---|---|---|---|---|---|---|---|
| 7.1 | **Initiate** SGLT2i or GLP-1 RA | T2DM AND (established CVD OR CKD ≥ moderate) AND on neither | `recom_cardiometab_rx` cl.1 | EMPA-REG OUTCOME 2015 (empa); DAPA-HF; DAPA-CKD; LEADER 2016 (liraglutide); SUSTAIN-6; REWIND | AU 2023; ESC/EAS 2025; KDIGO 2024 | KDIGO 1A (SGLT2i in CKD) | ✓ |
| 7.2 | **Maintain** | eligible, already on at least one | `recom_cardiometab_rx` cl.2 | — | — | — | ✓ |
| 7.3 | **Not indicated** | not eligible | `recom_cardiometab_rx` else | — | — | — | ✓ |
| 7.4 | Eligibility threshold = `ckd >= 3` | rule maps this to KDIGO heatmap moderate+ | `cardiometab_eligible` | DAPA-CKD entry criteria: eGFR 25–75 + uACR 200–5000 | KDIGO 2024 | KDIGO 1A | 🔍 verify — KDIGO 2024 endorses SGLT2i down to eGFR 20 and in non-diabetics with proteinuria; rule may under-recommend. |

---

## 8. Smoking cessation

| # | Recommendation | Trigger / threshold | Picorules variable | Primary evidence | Guideline | LoE | Concordance |
|---|---|---|---|---|---|---|---|
| 8.1 | **Offer cessation Rx** | current smoker, no cessation Rx | `recom_smoking` cl.1 | Cochrane reviews — varenicline/NRT/bupropion | AU 2023; RACGP Smoking Cessation | AU A | ✓ |
| 8.2 | **Maintain Rx** | current smoker, on cessation Rx | `recom_smoking` cl.2 | — | AU 2023 | — | ✓ |
| 8.3 | **Sustain abstinence** | ex-smoker | `recom_smoking` cl.3 | Relapse-prevention literature | RACGP | PP | ✓ |
| 8.4 | Current-smoker code = `smoke0 >= 29` | EADV `status_smoking_h2_v1` value | `is_smoker` | — | — | — | ✗ — coding choice, not evidence-based; verify mapping against your dataset's smoking-status coding. |
| 8.5 | Ex-smoker code = `smoke0 = 20` | EADV value | `is_exsmoker` | — | — | — | ✗ — coding choice. |

---

## 9. Reassessment intervals

| # | Recommendation | Trigger | Picorules variable | Guideline | LoE | Concordance |
|---|---|---|---|---|---|---|
| 9.1 | Reassess **1 year** | First Nations OR high risk | `recom_reassess_yr` cl.1, cl.2 | AU 2023 | AU PP | ✓ |
| 9.2 | Reassess **2 years** | intermediate risk | `recom_reassess_yr` cl.3 | AU 2023 | AU PP | ✓ |
| 9.3 | Reassess **5 years** | low risk | `recom_reassess_yr` cl.4 | AU 2023 | AU PP | ✓ |
| 9.4 | No reassessment recommendation | all others (no calc done) | `recom_reassess_yr` else | — | — | ⚠ — silent default; consider returning a "screen first" flag instead of 0. |

---

## Items requiring clinician sign-off (✗ rows consolidated)

| ID | Issue | Suggested action |
|---|---|---|
| 8.4, 8.5 | Smoking codes `29` and `20` | Verify these match your EADV smoking-status code system; otherwise smoker classification will silently underfire. |

## Items requiring evidence verification (🔍 rows consolidated)

| ID | What to verify |
|---|---|
| 7.4 | KDIGO 2024 eligibility breadth — should we extend SGLT2i recommendation to `cga_g_val >= 2` with significant albuminuria (heart of DAPA-CKD)? |

## Items extrapolated from guideline intent (⚠ rows consolidated)

| ID | Gap from verbatim guideline | Recommended resolution |
|---|---|---|
| 1.3 | FH trigger fires on DLCN "possible" not "confirmed" | Raise threshold to `fhc_prob >= 3` (probable+) or add a clinician-confirmed-FH flag from EADV. |
| 1.4 | DM+EOD is reclassification, not Step 2 | Either move to FNP-style uplift OR document as deliberate strengthening. |
| 1.6 | Generic +1 uplift for FNP | Replace with FNP-specific calculator binding when available (already a TODO in `.prb`). |
| 2.2 | Age 80 vs guideline's age 75 + frailty | Either accept age proxy or add a frailty indicator binding. |
| 3.B (Intermediate · Consider) | Intermediate-risk "consider" without lifestyle precondition | Add a `lifestyle_attempted` flag, or document that lifestyle is assumed concurrent. |
| 5.B (High · add non-statin) | PCSK9i / inclisiran / bempedoic ladder order | Cite ESC/EAS 2025 explicitly in `#doc()`; current rule comment is non-specific. |
| 9.4 | Silent default reassessment | Emit explicit "uncalculated — assess at next visit" code. |

---

## Cited sources

- **AU 2023** — Nelson MR et al. *2023 Australian guideline for assessing and managing cardiovascular disease risk.* Med J Aust 2024;220(9):482–490. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11081742/) · [Heart Foundation portal](https://www.heartfoundation.org.au/for-professionals/guideline-for-managing-cvd) · [Calculator](https://www.cvdcheck.org.au/)
- **AHA/ACC 2025 BP** — DOI [10.1161/CIR.0000000000001356](https://doi.org/10.1161/CIR.0000000000001356)
- **ESC/EAS 2019** — DOI [10.1093/eurheartj/ehz455](https://doi.org/10.1093/eurheartj/ehz455)
- **ESC/EAS 2025 focused update** — DOI [10.1093/eurheartj/ehaf190](https://doi.org/10.1093/eurheartj/ehaf190)
- **KDIGO 2024 CKD** — [kdigo.org](https://kdigo.org/guidelines/ckd-evaluation-and-management/)
- **SPRINT** — N Engl J Med 2015;373:2103–2116. DOI [10.1056/NEJMoa1511939](https://doi.org/10.1056/NEJMoa1511939)
- **HYVET** — N Engl J Med 2008;358:1887–1898. DOI [10.1056/NEJMoa0801369](https://doi.org/10.1056/NEJMoa0801369)
- **HOPE-3** — N Engl J Med 2016;374:2009–2020. DOI [10.1056/NEJMoa1600175](https://doi.org/10.1056/NEJMoa1600175)
- **IMPROVE-IT** — N Engl J Med 2015;372:2387–2397. DOI [10.1056/NEJMoa1410489](https://doi.org/10.1056/NEJMoa1410489)
- **FOURIER** — N Engl J Med 2017;376:1713–1722. DOI [10.1056/NEJMoa1615664](https://doi.org/10.1056/NEJMoa1615664)
- **ODYSSEY OUTCOMES** — N Engl J Med 2018;379:2097–2107. DOI [10.1056/NEJMoa1801174](https://doi.org/10.1056/NEJMoa1801174)
- **CLEAR Outcomes** (bempedoic acid) — N Engl J Med 2023;388:1353–1364. DOI [10.1056/NEJMoa2215024](https://doi.org/10.1056/NEJMoa2215024)
- **EMPA-REG OUTCOME** — N Engl J Med 2015;373:2117–2128. DOI [10.1056/NEJMoa1504720](https://doi.org/10.1056/NEJMoa1504720)
- **DAPA-CKD** — N Engl J Med 2020;383:1436–1446. DOI [10.1056/NEJMoa2024816](https://doi.org/10.1056/NEJMoa2024816)
- **LEADER** — N Engl J Med 2016;375:311–322. DOI [10.1056/NEJMoa1603827](https://doi.org/10.1056/NEJMoa1603827)
- **ASPREE** — N Engl J Med 2018;379:1499–1508. DOI [10.1056/NEJMoa1805819](https://doi.org/10.1056/NEJMoa1805819)
- **ATC Collaboration 2009** (aspirin meta-analysis) — Lancet 2009;373:1849–1860. DOI [10.1016/S0140-6736(09)60503-1](https://doi.org/10.1016/S0140-6736(09)60503-1)
- **DLCN criteria** (Nordestgaard) — Eur Heart J 2013;34:3478–3490. DOI [10.1093/eurheartj/eht273](https://doi.org/10.1093/eurheartj/eht273)
