# HFrEF by Medication Signature — Implementation Plan

## Clinical Background

Heart Failure with reduced Ejection Fraction (HFrEF) has a distinctive pharmacotherapy profile defined by guideline-directed medical therapy (GDMT). The 2022 AHA/ACC/HFSA guidelines and 2021 ESC guidelines establish four foundational pillars of HFrEF treatment:

1. **ARNI** (sacubitril/valsartan) or **ACEi/ARB** — RAAS inhibition
2. **Evidence-based beta-blockers** — carvedilol, bisoprolol, or metoprolol succinate (not atenolol)
3. **MRA** — spironolactone or eplerenone
4. **SGLT2 inhibitor** — dapagliflozin or empagliflozin

Additional HFrEF-associated medications:
- **Loop diuretics** — frusemide (symptom control, not disease-modifying)
- **Ivabradine** — heart rate control when beta-blockers insufficient
- **Digoxin** — rate control or symptom relief in refractory HF
- **Hydralazine + nitrate** — alternative vasodilator in patients intolerant of RAAS blockade

## Approach: Medication Signature Scoring

Rather than relying solely on ICD coding (which may be absent or inaccurate), this ruleblock infers probable HFrEF from the combination of prescribed medications. The logic is:

- Certain drugs are **highly specific** for HFrEF (ARNI, ivabradine) — their presence alone is strong evidence
- Other drugs are **common but non-specific** (beta-blockers, ACEi/ARB, SGLT2i, MRAs) — used for hypertension, CKD, diabetes
- The **combination** of 3+ GDMT pillars is highly specific for HFrEF even when individual drugs are not
- **Loop diuretics** combined with GDMT drugs increase specificity (loop diuretics alone are non-specific)

### Scoring Model

| Signal | Score | Rationale |
|--------|-------|-----------|
| ARNI prescribed | 3 | Virtually pathognomonic for HFrEF |
| Ivabradine prescribed | 3 | Only indicated in HFrEF |
| Evidence-based BB (carvedilol/bisoprolol/metoprolol succinate) | 1 | GDMT pillar, but also used in HTN/AF |
| ACEi or ARB | 1 | GDMT pillar, but also used in HTN/CKD/DM |
| MRA (spironolactone/eplerenone) | 1 | GDMT pillar, but also used in HTN/hyperaldosteronism |
| SGLT2 inhibitor | 1 | GDMT pillar, but also used in DM/CKD |
| Loop diuretic (frusemide) | 1 | Symptomatic HF, but also used in CKD/oedema |
| Digoxin | 1 | HF or AF rate control |
| Hydralazine + nitrate combination | 2 | Strongly suggests HFrEF (RAAS-intolerant pathway) |

### Classification Thresholds

| Score | Classification | Interpretation |
|-------|---------------|----------------|
| >= 5 | **Probable HFrEF** | High confidence — ARNI/ivabradine present, or >= 4 GDMT classes |
| 3-4 | **Possible HFrEF** | Moderate confidence — needs clinical correlation |
| 1-2 | **Unlikely HFrEF** | Non-specific cardiac medications |
| 0 | **No signal** | No relevant medications detected |

## EADV Attributes Used

### ATC class level (rxnc_)
| Attribute | Drug Class |
|-----------|-----------|
| `rxnc_c09dx04` | ARNI (sacubitril/valsartan) |
| `rxnc_c09aa` | ACE inhibitors |
| `rxnc_c09ca` | ARBs |
| `rxnc_c07ab` | Beta-blockers, selective (bisoprolol, metoprolol, atenolol) |
| `rxnc_c07ag` | Beta-blockers, alpha+beta (carvedilol) |
| `rxnc_c03da` | Aldosterone antagonists / steroidal MRA (spironolactone, eplerenone) |
| `rxnc_a10bk` | SGLT2 inhibitors |
| `rxnc_c03ca` | Loop diuretics (frusemide) |
| `rxnc_c01aa` | Cardiac glycosides (digoxin) |
| `rxnc_c01eb` | Other cardiac preparations (ivabradine) |

### RxNorm CUI level (rxn_cui_) for dose-specific identification
Used where ATC class is too broad. Leverages existing patterns from `rx_cv_common.prb`:
- Carvedilol: `rxn_cui_315577`, `rxn_cui_315575`, `rxn_cui_315576`
- Bisoprolol: `rxn_cui_854915`, `rxn_cui_854904`, `rxn_cui_854900`
- Metoprolol succinate (XR): `rxn_cui_1370489`, `rxn_cui_1370474`, `rxn_cui_1370483`, `rxn_cui_1370500`

## Cross-Ruleblock Dependencies

| Ruleblock | Binding | Purpose |
|-----------|---------|---------|
| `rout_cd_cardiac_chf` | `chf` | Existing CHF diagnosis (ICD/ICPC coded) |
| `rx_cv_common` | Could bind but we re-derive for independence | Medication data |

**Design decision**: This ruleblock derives medications independently rather than binding to `rx_cv_common`, because:
1. We need `val=1` (currently prescribed) filtering which `rx_cv_common` doesn't consistently apply
2. We need the evidence-based BB subset (carvedilol, bisoprolol, metoprolol succinate) which `rx_cv_common` lumps with all beta-blockers
3. We need ARNI, ivabradine, and digoxin which aren't all available as bindings

We do bind to `cd_cardiac_chf` to cross-reference coded CHF diagnosis against the medication signal.

## Outputs

| Variable | Type | Description |
|----------|------|-------------|
| `rx_hf_score` | integer | Composite medication signature score (0-12) |
| `rx_hf_pillars` | integer | Count of GDMT pillars present (0-4) |
| `rx_hfref_probable` | boolean | 1 if score >= 5 (probable HFrEF) |
| `rx_hfref_possible` | boolean | 1 if score 3-4 (possible HFrEF) |
| `rx_hfref_uncoded` | boolean | 1 if probable/possible HFrEF but no CHF ICD code |
| `[[rb_id]]` | boolean | 1 if probable or possible HFrEF by medication signature |

## References

- 2022 AHA/ACC/HFSA Guideline for Management of Heart Failure (Heidenreich et al., Circulation 2022)
- 2021 ESC Guidelines for Diagnosis and Treatment of Acute and Chronic Heart Failure (McDonagh et al., European Heart Journal 2021)
- 2023 ACC Expert Consensus Decision Pathway on HFrEF (Writing Committee, JACC 2023)
