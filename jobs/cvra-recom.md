# CVRA Recommendation Ruleblock — Implementation Document

**Rule ID:** `cd_cvra_recom`
**Source guideline:** [Australian CVD Risk Calculator — Management Overview](https://www.cvdcheck.org.au/overview)
**Date:** 2026-04-14
**Status:** Draft

---

## 1. Purpose

Create a new ruleblock that **reconciles** two independent cardiovascular risk assessments and generates **management recommendations** based on the reconciled risk category.

Two upstream ruleblocks each produce a `cvra_cat` (1=Low, 2=Intermediate, 3=High):
- **`cvra`** — Framingham-based equations (currently `is_active:2`)
- **`cvra_predict1_aus`** — Australian PREDICT-1 model (currently `is_active:0`, to be activated)

Because these models use different equations and coefficients, they may assign **contradictory risk categories** to the same patient. This rule reconciles the two by taking the **higher (more conservative) risk category** — the clinically safer default — and then derives actionable outputs: pharmacotherapy flags, target thresholds, reassessment intervals, and override triggers.

## 2. Clinical Logic (from cvdcheck.org.au)

### 2.1 Risk Categories and Actions

| cvra_cat | Label | 5-yr CVD risk | BP-lowering Rx | Lipid-modifying Rx | Reassessment |
|----------|-------|--------------|----------------|--------------------|--------------| 
| 3 | High | >= 10% | Prescribe | Prescribe | Not routinely required |
| 2 | Intermediate | 5% to <10% | Consider | Consider | Every 2 years (if no Rx) |
| 1 | Low | <5% | Not routine | Not routine | Every 5 years |

### 2.2 Override Criteria (Rx regardless of calculated risk)

These conditions warrant pharmacotherapy **independent** of the calculated risk category:

| Override | Condition | Already in `cvra.prb`? |
|----------|-----------|----------------------|
| Very high BP | SBP >= 160 **or** DBP >= 100 | Partially (sbp180 uses >=180) |
| Very high TC | Total cholesterol >= 7.5 mmol/L | Partially (tc7 uses >=7) |

The new rule should apply the **guideline-aligned thresholds** (SBP>=160, DBP>=100, TC>=7.5) rather than the legacy thresholds.

### 2.3 Lifestyle — Universal

All patients regardless of risk category receive lifestyle recommendations (smoking cessation, diet, exercise, weight, alcohol). This is a constant output flag.

## 3. Risk Reconciliation

### 3.1 Dual-source binding

| Variable | Source ruleblock | Binding | Purpose |
|----------|-----------------|---------|---------|
| `cvra_cat_fram` | `rout_cvra` | `.cvra_cat.val.bind()` | Framingham risk category |
| `cvra_cat_aus` | `rout_cvra_predict1_aus` | `.cvra_cat.val.bind()` | PREDICT-1 risk category |

### 3.2 Reconciliation rule

```
// Clinically-determined high-risk: bypass calculator entirely
// Guideline: CKD stage >=3 (eGFR <45) or FHC (probable/definitive) => automatic high risk
clin_high_risk : { nvl(ckd,0) >= 3 => 1 },         // moderate-to-severe CKD
                 { nvl(fhc_prob,0) >= 2 => 1 },     // probable or definitive FHC
                 { => 0 };

// Take highest of: clinical override (always 3), Framingham, PREDICT-1
cvra_cat_r : { clin_high_risk = 1 => 3 },
             { greatest(nvl(cvra_cat_fram,0), nvl(cvra_cat_aus,0)) > 0 
               => greatest(nvl(cvra_cat_fram,0), nvl(cvra_cat_aus,0)) },
             { => 0 };

// Track agreement between sources (for audit/reporting)
cvra_agree : { clin_high_risk = 1 => 2 },                          // clinically overridden
             { cvra_cat_fram = cvra_cat_aus => 1 },                // concordant
             { cvra_cat_fram !? and cvra_cat_aus !? => 0 },        // discordant
             { => -1 };                                              // single-source only

// Track which source drove the reconciled value
cvra_src :  { clin_high_risk = 1 and nvl(ckd,0) >= 3 => `CKD` },
            { clin_high_risk = 1 and nvl(fhc_prob,0) >= 2 => `FHC` },
            { nvl(cvra_cat_fram,0) > nvl(cvra_cat_aus,0) => `FRAM` },
            { nvl(cvra_cat_aus,0) > nvl(cvra_cat_fram,0) => `AUS` },
            { cvra_cat_fram = cvra_cat_aus => `BOTH` },
            { => `NONE` };
```

### 3.3 Rationale

- **Higher-of-two** is the safest reconciliation strategy — under-treating high-risk patients carries more harm than over-treating intermediate-risk patients
- **`cvra_agree`** flags discordant assessments for clinical review (e.g., Framingham says Low but PREDICT-1 says High)
- **`cvra_src`** provides audit traceability — which model was the binding constraint

All downstream logic in this rule uses **`cvra_cat_r`** (the reconciled category), never the individual source categories.

## 4. Inputs (Cross-Ruleblock Bindings)

### 4.1 Risk assessment sources

| Variable | Source ruleblock | Binding | Purpose |
|----------|-----------------|---------|---------|
| `cvra_cat_fram` | `rout_cvra` | `.cvra_cat.val.bind()` | Framingham risk category |
| `cvra_cat_aus` | `rout_cvra_predict1_aus` | `.cvra_cat.val.bind()` | PREDICT-1 risk category |
| `cvd_prev` | `rout_cvra` | `.cvd_prev.val.bind()` | Prior CVD event flag |
| `age` | `rout_cvra` | `.age.val.bind()` | Age (for target selection) |
| `ckd` | `rout_ckd` | `.ckd.val.bind()` | CKD stage (>=3 = clinically high-risk) |
| `fhc_prob` | `rout_cd_dyslip` | `.fhc_prob.val.bind()` | FHC probability (>=2 = clinically high-risk) |
| `eth_aboriginal` | `rout_dmg` | `.eth_aboriginal.val.bind()` | Aboriginal/Torres Strait Islander (reassessment modifier) |

### 4.2 Current BP medication state (from `cd_htn`)

| Variable | Source ruleblock | Binding | Purpose |
|----------|-----------------|---------|---------|
| `htn` | `rout_cd_htn` | `.cd_htn.val.bind()` | Known hypertension diagnosis |
| `rx_bp` | `rout_cd_htn` | `.htn_rxn.val.bind()` | On any BP-lowering med (binary) |
| `rx_bp_raas` | `rout_cd_htn` | `.htn_rxn_raas.val.bind()` | On ACEi or ARB |
| `rx_bp_acei` | `rout_cd_htn` | `.htn_rxn_acei.val.bind()` | On ACEi specifically |
| `rx_bp_arb` | `rout_cd_htn` | `.htn_rxn_arb.val.bind()` | On ARB specifically |
| `rx_bp_ccb` | `rout_cd_htn` | `.htn_rxn_ccb.val.bind()` | On calcium channel blocker |
| `rx_bp_bb` | `rout_cd_htn` | `.htn_rxn_bb.val.bind()` | On beta-blocker |
| `rx_bp_thiaz` | `rout_cd_htn` | `.htn_rxn_diuretic_thiaz.val.bind()` | On thiazide diuretic |
| `rx_bp_loop` | `rout_cd_htn` | `.htn_rxn_diuretic_loop.val.bind()` | On loop diuretic |
| `sbp_mu_1` | `rout_cd_htn_bp_control` | `.sbp_mu_1.val.bind()` | Mean SBP over past year |
| `sbp_tir_1y` | `rout_cd_htn_bp_control` | `.sbp_tir_1y.val.bind()` | BP time-in-range (%) over past year |

### 4.3 Current lipid medication state (from `cd_dyslip`)

| Variable | Source ruleblock | Binding | Purpose |
|----------|-----------------|---------|---------|
| `rx_statin` | `rout_cd_dyslip` | `.rx_statin.val.bind()` | On statin |
| `rx_ezet` | `rout_cd_dyslip` | `.rx_ezet.val.bind()` | On ezetimibe |
| `rx_evolocumab` | `rout_cd_dyslip` | `.rx_evolocumab.val.bind()` | On PCSK9 inhibitor |
| `ldl_val` | `rout_cd_dyslip` | `.ldl_val.val.bind()` | Latest LDL value |

### 4.4 Antiplatelet / anticoagulant state (from `cd_cardiac_rx`)

| Variable | Source ruleblock | Binding | Purpose |
|----------|-----------------|---------|---------|
| `rx_antiplatelet` | `rout_cd_cardiac_rx` | `.rxn_ap.val.bind()` | On antiplatelet agent |
| `rx_anticoag` | `rout_cd_cardiac_rx` | `.rxn_anticoag.val.bind()` | On anticoagulant |

### 4.5 Smoking status (from `at_risk`)

| Variable | Source ruleblock | Binding | Purpose |
|----------|-----------------|---------|---------|
| `smoker` | `rout_at_risk` | `.smoker.val.bind()` | Current/recent smoker (status_smoking_h2_v1 >= 29) |

### 4.6 Weight / obesity (from `cd_obesity`)

| Variable | Source ruleblock | Binding | Purpose |
|----------|-----------------|---------|---------|
| `bmi` | `rout_cd_obesity` | `.bmi.val.bind()` | Latest BMI value |
| `obesity` | `rout_cd_obesity` | `.cd_obesity.val.bind()` | Obesity diagnosis flag |

## 5. Inputs (Direct EADV Lookups)

| Variable | EADV attribute(s) | Aggregation | Filter | Notes |
|----------|-------------------|-------------|--------|-------|
| `sbp` | `obs_bp_systolic` | `lastdv()` | `dt > sysdate-365` | |
| `dbp` | `obs_bp_diastolic` | `lastdv()` | `dt > sysdate-365` | |
| `tc` | `lab_bld_cholesterol_total` | `last()` | `dt > sysdate-365` | |
| `smoke0` | `status_smoking_h2_v1` | `last()` | — | Raw smoking status code |
| `rx_cessation` | `rxnc_n07ba` | `dt.last().where(val=1)` | — | Smoking cessation drug (varenicline, bupropion, NRT). ATC N07BA. **Not captured by any existing rule — new direct EADV lookup.** |
| `alcohol_ref` | `ref_drug_alcohol` | `dt.last()` | — | Drug/alcohol referral (if available) |

## 6. Outputs (Attributes)

### 6.1 Reconciliation outputs

| Output variable | Type | Description |
|----------------|------|-------------|
| `clin_high_risk` | 1001 (flag) | 1 = clinically determined high-risk (CKD>=3 or FHC) |
| `cvra_cat_r` | 2 (numeric) | Reconciled risk category (highest of clinical, Framingham, PREDICT-1) |
| `cvra_agree` | 2 (numeric) | 2 = clinical override, 1 = concordant, 0 = discordant, -1 = single-source |
| `cvra_src` | 3 (string) | Which source drove the reconciled value (CKD/FHC/FRAM/AUS/BOTH/NONE) |

### 6.2 Recommendation outputs

| Output variable | Type | Description |
|----------------|------|-------------|
| `recom_rx_bp` | 2 (numeric) | 0 = not indicated, 1 = initiate, 2 = consider, 3 = intensify, 4 = maintain |
| `recom_rx_lipid` | 2 (numeric) | 0 = not indicated, 1 = initiate, 2 = consider, 3 = intensify, 4 = maintain |
| `recom_rx_antiplatelet` | 2 (numeric) | 0 = not indicated (primary prev), 1 = initiate (secondary prev, no Rx), 4 = maintain (secondary prev, on Rx) |
| `recom_reassess_yr` | 2 (numeric) | Reassessment interval in years (0 = not required, 2, 5) |
| `rx_override_bp` | 1001 (flag) | 1 = Very high BP override triggered |
| `rx_override_tc` | 1001 (flag) | 1 = Very high TC override triggered |

### 6.3 Current treatment summary

| Output variable | Type | Description |
|----------------|------|-------------|
| `bp_rx_n` | 2 (numeric) | Count of distinct BP drug classes currently prescribed |
| `lipid_rx_n` | 2 (numeric) | Count of distinct lipid drug classes currently prescribed |

### 6.4 Smoking recommendation outputs

| Output variable | Type | Description |
|----------------|------|-------------|
| `is_smoker` | 1001 (flag) | 1 = current smoker (status >= 29) |
| `is_exsmoker` | 1001 (flag) | 1 = ex-smoker (status = 20) |
| `rx_cessation_f` | 1001 (flag) | 1 = currently on cessation pharmacotherapy (N07BA) |
| `recom_smoking` | 2 (numeric) | 0 = non-smoker, 1 = initiate cessation Rx, 2 = cessation Rx already prescribed (maintain), 3 = ex-smoker (monitor) |
| `gap_smoking_rx` | 1001 (flag) | 1 = current smoker but NOT on cessation pharmacotherapy |

### 6.5 Lifestyle flag outputs

| Output variable | Type | Description |
|----------------|------|-------------|
| `recom_lifestyle` | 1001 (flag) | Always 1 — universal lifestyle modification |
| `recom_weight` | 1001 (flag) | 1 = BMI >= 25 — weight management recommended |

### 6.6 Care gap detection

| Output variable | Type | Description |
|----------------|------|-------------|
| `gap_bp_rx` | 1001 (flag) | 1 = BP Rx recommended but none prescribed |
| `gap_bp_intensify` | 1001 (flag) | 1 = On BP meds but SBP still above target |
| `gap_lipid_rx` | 1001 (flag) | 1 = Lipid Rx recommended but no statin prescribed |
| `gap_lipid_intensify` | 1001 (flag) | 1 = On statin but LDL still above target — consider intensification |
| `gap_smoking_rx` | 1001 (flag) | 1 = Current smoker, no cessation pharmacotherapy |
| `gap_antiplatelet` | 1001 (flag) | 1 = Established CVD but NOT on antiplatelet or anticoagulant |
| `cd_cvra_recom` | 1001 (flag) | 1 = Any active recommendation or care gap exists |

### 6.7 Guideline concordance

| Output variable | Type | Description |
|----------------|------|-------------|
| `n_applicable` | 2 (numeric) | Number of guideline domains applicable to this patient (0-4) |
| `n_met` | 2 (numeric) | Number of applicable domains where recommendation is met (0-4) |
| `concordance_pct` | 2 (numeric) | Guideline concordance score: `round((n_met/n_applicable)*100)`. 100 = fully concordant, 0 = no recommendations met. Patients with no applicable domains default to 100. |

## 7. Conditional Logic (Pseudocode)

```
// ============================================================
// STAGE 1: Risk Reconciliation (3 sources: clinical, Framingham, PREDICT-1)
// ============================================================

// Clinically-determined high-risk overrides (guideline: bypass calculator)
clin_high_risk : { nvl(ckd,0) >= 3 => 1 },         // moderate-to-severe CKD (eGFR <45)
                 { nvl(fhc_prob,0) >= 2 => 1 },     // probable/definitive FHC
                 { => 0 };

// Reconciled category: clinical override > highest of calculators
cvra_cat_r : { clin_high_risk = 1 => 3 },
             { greatest(nvl(cvra_cat_fram,0), nvl(cvra_cat_aus,0)) > 0 
               => greatest(nvl(cvra_cat_fram,0), nvl(cvra_cat_aus,0)) },
             { => 0 };

// Track concordance (2=clinical override, 1=concordant, 0=discordant, -1=single-source)
cvra_agree : { clin_high_risk = 1 => 2 },
             { cvra_cat_fram = cvra_cat_aus => 1 },
             { cvra_cat_fram !? and cvra_cat_aus !? => 0 },
             { => -1 };

// Track which source drove the reconciled value
cvra_src :  { clin_high_risk = 1 and nvl(ckd,0) >= 3 => `CKD` },
            { clin_high_risk = 1 and nvl(fhc_prob,0) >= 2 => `FHC` },
            { nvl(cvra_cat_fram,0) > nvl(cvra_cat_aus,0) => `FRAM` },
            { nvl(cvra_cat_aus,0) > nvl(cvra_cat_fram,0) => `AUS` },
            { cvra_cat_fram = cvra_cat_aus and cvra_cat_fram !? => `BOTH` },
            { => `NONE` };

// ============================================================
// STAGE 2: Current Treatment Inventory
// ============================================================

// --- BP drug class count ---
// Each binding is 0 or 1; sum gives the number of distinct classes
bp_rx_n : { . => nvl(rx_bp_raas,0) + nvl(rx_bp_ccb,0) + nvl(rx_bp_bb,0) 
                + nvl(rx_bp_thiaz,0) + nvl(rx_bp_loop,0) };

// --- Lipid drug class count ---
lipid_rx_n : { . => nvl(rx_statin,0) + nvl(rx_ezet,0) + nvl(rx_evolocumab,0) };

// --- BP target and control ---
// SBP target: 120 for high-risk <65, 140 otherwise (from cd_htn_bp_control)
sbp_target : { cvra_cat_r = 3 and age < 65 => 120 },
             { => 140 };

sbp_above_target : { sbp_val !? and sbp_val > sbp_target => 1 }, { => 0 };

// --- LDL target based on CVD history ---
// Secondary prevention (prior CVD): LDL < 1.8 mmol/L
// Primary prevention: LDL < 2.0 mmol/L (high risk) or no specific target
ldl_target : { cvd_prev = 1 => 1.8 },
             { cvra_cat_r = 3 => 2.0 },
             { => 4.9 };

ldl_above_target : { ldl_val !? and ldl_val > ldl_target => 1 }, { => 0 };

// ============================================================
// STAGE 3: Override Triggers
// ============================================================

rx_override_bp  : { sbp_val >= 160 or dbp_val >= 100 => 1 }, { => 0 };
rx_override_tc  : { tc >= 7.5 => 1 }, { => 0 };

// ============================================================
// STAGE 4: Recommendations (based on reconciled risk + current Rx)
// ============================================================

// --- BP pharmacotherapy ---
// If already on BP meds, check if BP is at target to distinguish maintain vs intensify
recom_rx_bp :   { rx_override_bp = 1 and rx_bp = 0 => 1 },                    // override + not treated: initiate
                { rx_override_bp = 1 and rx_bp > 0 => 3 },                    // override + treated: intensify
                { cvra_cat_r = 3 and rx_bp = 0 => 1 },                        // high + not treated: initiate
                { cvra_cat_r = 3 and rx_bp > 0 and sbp_above_target = 1 => 3 },  // high + treated + above target: intensify
                { cvra_cat_r = 3 and rx_bp > 0 and sbp_above_target = 0 => 4 },  // high + treated + at target: maintain
                { cvra_cat_r = 2 and rx_bp = 0 => 2 },                        // intermediate + not treated: consider
                { cvra_cat_r = 2 and rx_bp > 0 and sbp_above_target = 1 => 3 },  // intermediate + treated + above target: intensify
                { cvra_cat_r = 2 and rx_bp > 0 and sbp_above_target = 0 => 4 },  // intermediate + treated + at target: maintain
                { => 0 };                                                       // low + not treated: not routine

// --- Lipid pharmacotherapy ---
recom_rx_lipid: { rx_override_tc = 1 and rx_statin = 0 => 1 },     // override + no statin: initiate
                { rx_override_tc = 1 and rx_statin > 0 => 3 },     // override + on statin: intensify
                { cvra_cat_r = 3 and lipid_rx_n = 0 => 1 },        // high + no lipid Rx: initiate statin
                { cvra_cat_r = 3 and ldl_above_target = 1 => 3 },  // high + on Rx but LDL above target: intensify
                { cvra_cat_r = 3 and ldl_above_target = 0 => 4 },  // high + on Rx and at target: maintain
                { cvra_cat_r = 2 and lipid_rx_n = 0 => 2 },        // intermediate + no Rx: consider
                { cvra_cat_r = 2 and lipid_rx_n > 0 => 4 },        // intermediate + on Rx: maintain
                { => 0 };                                            // low: not routine

// Recommendation codes:
//   0 = not indicated
//   1 = initiate (prescribe — not currently on treatment)
//   2 = consider (intermediate risk — shared decision-making)
//   3 = intensify/optimise (on treatment but override or target not met)
//   4 = maintain (on treatment and at target)

// ============================================================
// STAGE 4b: Antiplatelet — Secondary Prevention
// ============================================================

// Antiplatelet is indicated for SECONDARY prevention (established CVD) only
// NOT recommended for primary prevention (no prior CVD events)
// Anticoagulant (e.g. for AF) may substitute — don't flag gap if on anticoag

recom_rx_antiplatelet :  
    { cvd_prev = 1 and nvl(rx_antiplatelet,0) = 0 and nvl(rx_anticoag,0) = 0 => 1 },  // secondary prev, no antithrombotic: initiate
    { cvd_prev = 1 and (rx_antiplatelet !? or rx_anticoag !?) => 4 },                   // secondary prev, on therapy: maintain
    { => 0 };                                                                             // primary prev: not indicated

// Care gap: established CVD without any antithrombotic cover
gap_antiplatelet : { cvd_prev = 1 and nvl(rx_antiplatelet,0) = 0 
                     and nvl(rx_anticoag,0) = 0 => 1 }, { => 0 };

// ============================================================
// STAGE 4d: Smoking Cessation Recommendation
// ============================================================

// Smoking status classification
// status_smoking_h2_v1: 30=current, 29=recently quit, 20=ex-smoker, <20=never
is_smoker : { smoke0 >= 29 => 1 }, { => 0 };
is_exsmoker : { smoke0 = 20 => 1 }, { => 0 };

// Cessation pharmacotherapy flag (N07BA: varenicline, bupropion, NRT)
rx_cessation_f : { rx_cessation !? => 1 }, { => 0 };

// Recommendation: contextual to smoking status + current cessation Rx
recom_smoking : { is_smoker = 1 and rx_cessation_f = 0 => 1 },     // smoker, no Rx: initiate cessation
                { is_smoker = 1 and rx_cessation_f = 1 => 2 },     // smoker, on Rx: maintain/support
                { is_exsmoker = 1 => 3 },                           // ex-smoker: monitor/relapse prevention
                { => 0 };                                            // non-smoker: no action

// Care gap: smoker without cessation pharmacotherapy
gap_smoking_rx : { is_smoker = 1 and rx_cessation_f = 0 => 1 }, { => 0 };

// ============================================================
// STAGE 4e: Lifestyle Recommendations
// ============================================================

// Universal lifestyle (all patients regardless of risk)
recom_lifestyle : { . => 1 };

// Weight management
recom_weight : { nvl(bmi,0) >= 25 => 1 }, { => 0 };

// --- Reassessment interval (years) ---
// First Nations: annual or at least every 2 years (guideline-specific)
recom_reassess_yr : { eth_aboriginal = 1 => 1 },       // First Nations: annual
                    { cvra_cat_r = 3 => 0 },            // high: not routinely required
                    { cvra_cat_r = 2 and rx_bp = 0 and lipid_rx_n = 0 => 2 },  // untreated intermediate: 2yr
                    { cvra_cat_r = 2 => 1 },            // treated intermediate: annual review
                    { cvra_cat_r = 1 => 5 },            // low: every 5 years
                    { => 0 };

// ============================================================
// STAGE 5: Care Gap Detection
// ============================================================

// BP: recommended to initiate but nothing prescribed
gap_bp_rx : { recom_rx_bp = 1 and nvl(rx_bp,0) = 0 => 1 }, { => 0 };

// Lipid: recommended to initiate but no statin
gap_lipid_rx : { recom_rx_lipid = 1 and nvl(rx_statin,0) = 0 => 1 }, { => 0 };

// BP intensification: on BP meds but SBP still above target
gap_bp_intensify : { rx_bp > 0 and sbp_above_target = 1 => 1 }, { => 0 };

// Lipid intensification: on statin but LDL still above target — consider adding ezetimibe/PCSK9i
gap_lipid_intensify : { rx_statin > 0 and ldl_above_target = 1 
                        and nvl(rx_ezet,0) = 0 => 1 }, { => 0 };

// Summary flag
cd_cvra_recom : { greatest(recom_rx_bp, recom_rx_lipid, recom_rx_antiplatelet,
                           recom_smoking, gap_bp_rx, gap_bp_intensify,
                           gap_lipid_rx, gap_lipid_intensify, 
                           gap_smoking_rx, gap_antiplatelet) > 0 => 1 }, { => 0 };

// ============================================================
// STAGE 6: Guideline Concordance Score
// ============================================================

// Count applicable pharmacotherapy domains for this patient
// A domain is "applicable" when the guideline makes a recommendation (code > 0)
// Weight excluded — not resolvable via pharmacotherapy alone
n_recom_bp :        { recom_rx_bp > 0 => 1 },      { => 0 };
n_recom_lipid :     { recom_rx_lipid > 0 => 1 },    { => 0 };
n_recom_antipl :    { cvd_prev = 1 => 1 },           { => 0 };
n_recom_smoking :   { is_smoker = 1 => 1 },          { => 0 };

n_applicable : { . => n_recom_bp + n_recom_lipid + n_recom_antipl + n_recom_smoking };

// Count met domains — recommendation is satisfied when:
//   - BP/Lipid: code = 4 (on treatment, at target)
//   - Antiplatelet: code = 4 (on antithrombotic therapy)
//   - Smoking: code = 2 (on cessation Rx) — best achievable via pharmacotherapy
n_met_bp :       { recom_rx_bp = 4 => 1 },           { => 0 };
n_met_lipid :    { recom_rx_lipid = 4 => 1 },        { => 0 };
n_met_antipl :   { recom_rx_antiplatelet = 4 => 1 },  { => 0 };
n_met_smoking :  { recom_smoking = 2 => 1 },          { => 0 };

n_met : { . => n_met_bp + n_met_lipid + n_met_antipl + n_met_smoking };

// Concordance percentage (0-100)
// 100 = all applicable recommendations met; 0 = none met
// Patients with no applicable recommendations score 100 (fully concordant by default)
concordance_pct : { n_applicable > 0 => round((n_met / n_applicable) * 100, 0) },
                  { => 100 };
```

### 7.1 Recommendation Code Semantics

The `recom_rx_bp` and `recom_rx_lipid` outputs use a **four-valued code** that reflects both the guideline recommendation *and* the patient's current treatment state:

| Code | Meaning | Clinical action |
|------|---------|-----------------|
| 0 | Not indicated | No pharmacotherapy needed at this risk level |
| 1 | Initiate | Patient is NOT on treatment but SHOULD be — start Rx |
| 2 | Consider | Intermediate risk, not on treatment — shared decision-making |
| 3 | Intensify/optimise | Already on treatment but override triggered or target not met |
| 4 | Maintain | On treatment and at target — continue current regimen |

This avoids the blind spot of recommending "prescribe a statin" to a patient who is already on one. Instead, the system distinguishes between starting treatment, stepping it up, and maintaining it.

## 8. Design Decisions

### 8.1 Higher-of-two reconciliation
When two validated risk models disagree, the clinically safer default is to treat at the higher risk level. Under-treating a truly high-risk patient carries more harm than over-treating an intermediate-risk patient with a "consider" recommendation. The `greatest()` approach is simple, auditable, and defensible.

### 8.2 Concordance tracking (`cvra_agree`, `cvra_src`)
Discordant assessments are clinically interesting — they may indicate patients whose risk profile is edge-case or model-sensitive. Exposing `cvra_agree` and `cvra_src` as reportable attributes enables:
- Population-level audit: what proportion of patients get discordant assessments?
- Clinical review: flag discordant patients for manual reassessment
- Model evaluation: systematic comparison of Framingham vs PREDICT-1 in this population

### 8.3 Four-valued Rx recommendation (0/1/2/3/4)
The previous design used a three-valued code (prescribe/consider/not indicated). This ignored what the patient is already taking. The four-valued code (initiate/consider/intensify/maintain/not indicated) means the recommendation is always contextual to the patient's current regimen:
- A high-risk patient **not** on a statin gets `1` (initiate) — a clear care gap
- A high-risk patient **on** a statin with LDL at target gets `4` (maintain) — no action needed
- A high-risk patient **on** a statin with LDL still high gets `3` (intensify) — consider add-on therapy

### 8.4 Treatment inventory from existing rules
Rather than re-querying EADV for medications, this rule binds to outputs already computed by `cd_htn`, `cd_dyslip`, and `cd_cardiac_rx`. This avoids duplication and ensures consistency — if those rules' medication logic changes, this rule automatically inherits the update. The granular class-level bindings (ACEi, ARB, CCB, BB, thiazide, statin, ezetimibe, PCSK9i) enable both the drug-class count (`bp_rx_n`, `lipid_rx_n`) and future per-class recommendations.

### 8.5 LDL target by CVD context
LDL targets differ for secondary prevention (prior CVD: <1.8) vs primary high-risk (<2.0) vs general population (<4.9). The `ldl_target` conditional draws on `cvd_prev` from the upstream `cvra` rule. `gap_lipid_intensify` then compares actual LDL to this target, flagging patients on a statin who would benefit from ezetimibe or PCSK9i add-on.

### 8.6 Override thresholds aligned to current guidelines
The existing `cvra.prb` uses SBP >= 180 and TC >= 7. The 2023 Australian guideline (cvdcheck.org.au) specifies SBP >= 160, DBP >= 100, and TC >= 7.5. This rule uses the updated thresholds. The original `cvra.prb` overrides remain untouched — this rule layers on top.

### 8.7 Clinically-determined high-risk overrides
The guideline specifies two conditions that bypass the risk calculator entirely: moderate-to-severe CKD (eGFR <45, mapped to `ckd>=3` from the existing CKD staging rule) and familial hypercholesterolaemia (`fhc_prob>=2` from the Dutch Lipid Score in `cd_dyslip`). These override the reconciled calculator output to category 3 (High). The existing `cvra.prb` has some overlapping overrides (ckd3, tc7, sbp180) but they use older thresholds and don't include FHC. This rule captures both under `clin_high_risk` and records `cvra_src` as `CKD` or `FHC` for audit.

### 8.8 BP target gap (parity with lipid)
The lipid domain already had `ldl_above_target` and `gap_lipid_intensify`. The same logic now applies to BP: `sbp_target` is set based on risk and age (120 for high-risk <65, 140 otherwise), and `gap_bp_intensify` flags patients on BP meds whose SBP is still above target. This makes the BP and lipid recommendation pathways structurally parallel — both distinguish initiate/intensify/maintain.

### 8.9 First Nations reassessment
The guideline specifies annual reassessment for Aboriginal and Torres Strait Islander patients regardless of risk category (vs 2yr/5yr for general population). `eth_aboriginal` from `dmg.prb` is already available as a binding. This takes precedence over all other reassessment intervals.

### 8.10 Guideline concordance score
The `concordance_pct` output provides a single patient-level metric for how well current care aligns with guideline recommendations. Design choices:
- **Denominator is patient-specific** — only counts domains where a recommendation applies. A low-risk non-smoker without prior CVD has 0 applicable domains and scores 100% (no action needed). A high-risk patient with prior CVD and active smoking has 4 applicable domains.
- **"Met" means the best achievable pharmacotherapy outcome** — code 4 (on treatment, at target) for BP/lipid/antiplatelet, code 2 (on cessation Rx) for smoking. Code 3 (intensify) is NOT met — the patient is on treatment but not at target.
- **Weight excluded from denominator** — BMI is not resolvable via a single prescribing decision, so including it would penalise the concordance score unfairly. It remains a separate recommendation flag.
- **Population-level utility** — averaging `concordance_pct` across a cohort gives a single quality-of-care metric comparable across time, clinics, or regions.

### 8.11 Dependency chain
This rule sits downstream of CVRA ruleblocks, CKD staging, FHC scoring, demographics, and all medication/disease rules. It consumes their outputs but does not feed back. No circular binding risk.

## 9. Dependency Graph

```
rout_cvra ───────────────────────┐
  .cvra_cat (Framingham)         │
  .cvd_prev                      │
  .age                           │
                                 │
rout_cvra_predict1_aus ──────────┤
  .cvra_cat (PREDICT-1)          │
                                 │
rout_cd_htn ─────────────────────┤    cd_cvra_recom
  .cd_htn                        │    ┌──────────────────────────────┐
  .htn_rxn (any BP med)          ├───>│ S1: Reconcile risk           │
  .htn_rxn_raas                  │    │ S2: Inventory current Rx     │
  .htn_rxn_acei / _arb           │    │ S3: Override triggers        │
  .htn_rxn_ccb / _bb             │    │ S4: Recommendations          │
  .htn_rxn_diuretic_thiaz/_loop  │    │ S5: Care gap detection       │
                                 │    └──────────────────────────────┘
rout_cd_dyslip ──────────────────┤
  .rx_statin / .rx_ezet          │
  .rx_evolocumab / .ldl_val      │
                                 │
rout_cd_cardiac_rx ──────────────┤
  .rxn_ap (antiplatelet)         │
  .rxn_anticoag                  │
                                 │
rout_at_risk ────────────────────┤
  .smoker                        │
                                 │
rout_cd_obesity ─────────────────┤
  .bmi / .cd_obesity             │
                                 │
rout_ckd ────────────────────────┤
  .ckd (stage)                   │
                                 │
rout_dmg ────────────────────────┤
  .eth_aboriginal                │
                                 │
rout_cd_htn_bp_control ──────────┤
  .sbp_mu_1 / .sbp_tir_1y       │
                                 │
eadv (direct) ───────────────────┘
  obs_bp_systolic
  obs_bp_diastolic
  lab_bld_cholesterol_total
  status_smoking_h2_v1
  rxnc_n07ba (cessation Rx)
```

## 10. Testing Scenarios

### 10.1 Reconciliation scenarios

| # | Scenario | FRAM | AUS | CKD | FHC | Reconciled | agree | src |
|---|----------|------|-----|-----|-----|------------|-------|-----|
| 1 | Concordant High | 3 | 3 | 0 | 0 | 3 | 1 | BOTH |
| 2 | Concordant Low | 1 | 1 | 0 | 0 | 1 | 1 | BOTH |
| 3 | Discordant: FRAM > AUS | 3 | 2 | 0 | 0 | 3 | 0 | FRAM |
| 4 | Discordant: AUS > FRAM | 1 | 2 | 0 | 0 | 2 | 0 | AUS |
| 5 | CKD override (calculators say Low) | 1 | 1 | 3 | 0 | 3 | 2 | CKD |
| 6 | FHC override (calculators say Intermediate) | 2 | 2 | 0 | 3 | 3 | 2 | FHC |
| 7 | FRAM only | 2 | null | 0 | 0 | 2 | -1 | FRAM |
| 8 | No data | null | null | 0 | 0 | 0 | -1 | NONE |

### 10.2 Medication-aware recommendation scenarios

| # | Scenario | Risk | BP Rx classes | Statin | Ezet | LDL | SBP | TC | recom_rx_bp | recom_rx_lipid | Gaps |
|---|----------|------|---------------|--------|------|-----|-----|----|-------------|----------------|------|
| 9 | High, untreated | 3 | 0 | 0 | 0 | 3.5 | 145 | 6.0 | 1 (initiate) | 1 (initiate) | gap_bp=1, gap_lipid=1 |
| 10 | High, on RAAS+statin, BP+LDL at target | 3 | 1 | 1 | 0 | 1.6 | 118 | 4.5 | 4 (maintain) | 4 (maintain) | none |
| 11 | High, on RAAS+statin, SBP above target | 3 | 1 | 1 | 0 | 1.6 | 148 | 4.5 | 3 (intensify) | 4 (maintain) | gap_bp_intensify=1 |
| 12 | High, on statin, LDL above target | 3 | 0 | 1 | 0 | 2.8 | 120 | 5.0 | 1 (initiate BP) | 3 (intensify) | gap_bp=1, gap_lipid_intensify=1 |
| 13 | High, on statin+ezet, LDL above target | 3 | 1 | 1 | 1 | 2.5 | 130 | 5.0 | 4 (maintain) | 3 (intensify) | gap_lipid_intensify=0 (ezet on) |
| 14 | Intermediate, untreated | 2 | 0 | 0 | 0 | 3.0 | 138 | 5.5 | 2 (consider) | 2 (consider) | none |
| 15 | Intermediate, on Rx, at target | 2 | 2 | 1 | 0 | 2.0 | 132 | 4.8 | 4 (maintain) | 4 (maintain) | none |
| 16 | Low, normal values | 1 | 0 | 0 | 0 | 2.5 | 120 | 4.0 | 0 | 0 | none, reassess=5 |

### 10.3 Override scenarios

| # | Scenario | Risk | SBP | TC | On BP Rx | On Statin | recom_rx_bp | recom_rx_lipid |
|---|----------|------|-----|----|----------|-----------|-------------|----------------|
| 17 | BP override, untreated | 1 | 165 | 4.0 | 0 | 0 | 1 (initiate) | 0 |
| 18 | BP override, already on 2 classes | 1 | 168 | 4.0 | 1 | 0 | 3 (intensify) | 0 |
| 19 | TC override, no statin | 1 | 120 | 8.0 | 0 | 0 | 0 | 1 (initiate) |
| 20 | TC override, on statin | 1 | 120 | 8.0 | 0 | 1 | 0 | 3 (intensify) |

### 10.4 Antiplatelet — secondary prevention scenarios

| # | Scenario | cvd_prev | On antiplatelet | On anticoag | recom_rx_antiplatelet | gap_antiplatelet |
|---|----------|----------|-----------------|-------------|----------------------|------------------|
| 21 | Prior MI, no antithrombotic | 1 | 0 | 0 | 1 (initiate) | 1 |
| 22 | Prior MI, on aspirin | 1 | 1 | 0 | 4 (maintain) | 0 |
| 23 | Prior CVA, on anticoagulant (AF) | 1 | 0 | 1 | 4 (maintain) | 0 |
| 24 | No prior CVD (primary prev) | 0 | 0 | 0 | 0 (not indicated) | 0 |

### 10.5 Smoking and lifestyle scenarios

| # | Scenario | Smoke status | Cessation Rx | BMI | recom_smoking | gap_smoking_rx | recom_weight |
|---|----------|-------------|--------------|-----|---------------|----------------|--------------|
| 25 | Current smoker, no cessation Rx | 30 | null | 28 | 1 (initiate) | 1 | 1 |
| 26 | Current smoker, on varenicline | 30 | yes | 24 | 2 (maintain) | 0 | 0 |
| 27 | Recently quit, no Rx | 29 | null | 32 | 1 (initiate) | 1 | 1 |
| 28 | Ex-smoker | 20 | null | 22 | 3 (monitor) | 0 | 0 |
| 29 | Never smoker | 10 | null | 26 | 0 | 0 | 1 |

### 10.6 First Nations reassessment

| # | Scenario | eth_aboriginal | cvra_cat_r | recom_reassess_yr |
|---|----------|----------------|------------|-------------------|
| 30 | First Nations, Low risk | 1 | 1 | 1 (annual, overrides 5yr default) |
| 31 | First Nations, High risk | 1 | 3 | 1 (annual) |
| 32 | Non-Indigenous, Low risk | 0 | 1 | 5 |

### 10.7 Guideline concordance scenarios

| # | Scenario | Applicable | Met | concordance_pct |
|---|----------|-----------|-----|-----------------|
| 33 | High risk, fully treated + at target, non-smoker, no CVD | 2 (BP, lipid) | 2 | 100% |
| 34 | High risk + prior CVD, all Rx, at target, non-smoker | 3 (BP, lipid, antiplatelet) | 3 | 100% |
| 35 | High risk, on statin at target, no BP Rx, non-smoker | 2 (BP, lipid) | 1 (lipid) | 50% |
| 36 | High risk + prior CVD + smoker, completely untreated | 4 (BP, lipid, antiplatelet, smoking) | 0 | 0% |
| 37 | High risk + prior CVD, on aspirin+statin, no BP Rx, smoker on varenicline | 4 (BP, lipid, antiplatelet, smoking) | 3 (lipid@target, antiplatelet, smoking) | 75% |
| 38 | Low risk, non-smoker, no CVD | 0 | 0 | 100% (no recommendations applicable) |

### 10.8 Composite worst-case

| # | Scenario | Expected |
|---|----------|----------|
| 39 | High risk + prior CVD + CKD 4 + smoker + BMI 30 + no treatment | cvra_cat_r=3 (CKD override), recom_rx_bp=1, recom_rx_lipid=1, recom_rx_antiplatelet=1, recom_smoking=1, recom_weight=1, all gaps=1, concordance_pct=0% |

## 11. Guideline Coverage Matrix

Maps each recommendation domain from the [Australian CVD guidelines](https://www.cvdcheck.org.au/overview) to what this rule covers:

| Guideline domain | Covered | How | Notes |
|-----------------|---------|-----|-------|
| BP-lowering pharmacotherapy | Yes | `recom_rx_bp` (0-4) | Class-level awareness via cd_htn bindings |
| Lipid-modifying pharmacotherapy | Yes | `recom_rx_lipid` (0-4) | Statin/ezetimibe/PCSK9i awareness via cd_dyslip |
| Antiplatelet — secondary prevention | Yes | `recom_rx_antiplatelet` (0/1/4) + `gap_antiplatelet` | B01AC from cd_cardiac_rx; anticoag-aware (no gap if on warfarin/NOAC for AF) |
| Smoking cessation + pharmacotherapy | Yes | `recom_smoking` (0-3) + `gap_smoking_rx` | N07BA (varenicline/bupropion/NRT) from EADV |
| Healthy eating / nutrition | Partial | `recom_lifestyle` (universal flag) | Not individually computable — no structured diet data in EADV |
| Physical activity | Partial | `recom_lifestyle` (universal flag) | Not individually computable — no structured activity data |
| Weight management | Yes | `recom_weight` (BMI >= 25) | BMI from cd_obesity binding |
| Alcohol reduction | No | — | `ref_drug_alcohol` exists in EADV but coverage unclear; candidate for future extension |
| Risk communication / decision aids | Out of scope | — | Presentation-layer concern, not rule logic |
| Reassessment interval | Yes | `recom_reassess_yr` | Risk-dependent: 0/1/2/5 years |
| Clinically high-risk: CKD | Yes | `clin_high_risk` override in reconciliation | CKD stage >=3 bypasses calculator, auto-classified high-risk |
| Clinically high-risk: FHC | Yes | `clin_high_risk` override in reconciliation | FHC prob >=2 (probable/definitive) bypasses calculator |
| First Nations reassessment | Yes | `eth_aboriginal` modifies `recom_reassess_yr` | Annual reassessment per guideline |
| Reclassification: ethnicity risk adjustment | Partial | — | PREDICT-1 has SEIFA; Maori/Pacific/South Asian adjustment not yet computable |
| BP target assessment | Yes | `sbp_target`, `sbp_above_target`, `gap_bp_intensify` | Mirrors the LDL target gap logic for BP |
| Coronary artery calcium scoring | Out of scope | — | Guideline says "not recommended for general screening" |

## 12. Next Steps

1. **Activate `cvra_predict1_aus`** — set `is_active:2` so it runs alongside `cvra` and produces a bindable `cvra_cat`
2. **Author** the `.prb` file as `cd_cvra_recom.prb` following the pseudocode in section 7
3. **Compile** against T-SQL dialect to validate syntax
4. **Test** with EADV mocker — prioritise:
   - Scenarios 8-11 (medication-aware recommendations)
   - Scenarios 15-18 (overrides with existing treatment)
   - Scenarios 19-24 (smoking cessation + composite cases)
5. **Future extensions** (not in scope for v1):
   - Alcohol reduction recommendation (pending `ref_drug_alcohol` data quality assessment)
   - SGLT2i/GLP1a for cardiorenal benefit in diabetic high-risk patients (cross-reference with `cd_dm_rx_rcm`)
