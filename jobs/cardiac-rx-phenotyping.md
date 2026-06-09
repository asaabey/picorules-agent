# Cardiac Phenotyping from Medication Signals — New & Upgraded Rules

**Created:** 2026-04-07
**Context:** Existing cardiac rules rely heavily on ICD/ICPC diagnosis codes. Many cardiac phenotypes can be inferred or strengthened from medication patterns, even when diagnostic coding is absent or incomplete.

---

## Current State

### Rules that already use medication data
| Rule | Medications tracked | Gap |
|------|-------------------|-----|
| cd_cardiac_cad | Antiplatelet, anticoag, BB, ACEi/ARB, statin | Good coverage — but no inference from Rx alone |
| cd_cardiac_chf | ARNI only | Misses loop diuretics, BB, MRA, SGLT2i, digoxin, ivabradine |
| cd_cardiac_af | Anticoag (cross-bind only) | No rate/rhythm control agents |
| cd_cardiac_rx | Antiplatelet, anticoag, antiarrhythmics, diuretics, statins | Catalogues meds but doesn't infer phenotypes |
| cd_htn | ACEi, ARB, BB, CCB, C02, thiazide, loop | Diagnoses HTN but doesn't detect uncoded treatment |
| cd_dyslip | Statin, ezetimibe, PCSK9i | Detects treatment but no Rx-based phenotype inference |
| cd_cardiac_vte | Anticoag only | No duration or appropriateness assessment |
| rx_cv_common | Dose-level CUIs for most cardiac drugs | Utility rule — no phenotype logic |

### Available but unused EADV medication attributes
| ATC prefix | Class | Available in EADV | Currently used |
|------------|-------|-------------------|----------------|
| rxnc_c01aa | Cardiac glycosides (digoxin) | Yes | Only via c01% wildcard in cd_cardiac_rx |
| rxnc_c01bd | Antiarrhythmics class III (amiodarone, dronedarone) | Yes | Only via c01% wildcard |
| rxnc_c01da | Organic nitrates (ISMN, GTN) | Yes | Only in rx_cv_common |
| rxnc_c01ea | Prostaglandins | Yes | No |
| rxnc_c03ca | Aldosterone antagonists (spironolactone) | Yes | No |
| rxnc_c03da | K-sparing diuretics | Yes | Only in cd_cardiac_rx |
| rxnc_c09dx04 | Sacubitril/valsartan (ARNI) | Yes | Only in cd_cardiac_chf |
| rxnc_a10bk | SGLT2 inhibitors | Yes | Only in diabetes rules |
| rxnc_c10ax09 | Ezetimibe | Yes | Only in cd_dyslip |
| rxnc_c10ax13 | PCSK9 inhibitors | Yes | Only in cd_dyslip |

---

## Proposed New Rules

### 1. NEW: `cd_cardiac_chf_rx` — Heart Failure Medication Phenotyping

**Rationale:** CHF is often treated before formal coding. The combination of loop diuretic + ACEi/ARB + BB is strongly suggestive of CHF management. GDMT (guideline-directed medical therapy) assessment is clinically valuable.

**Medication signals for CHF phenotype inference:**
- Loop diuretic (`rxnc_c03c%`) — fluid management
- MRA / spironolactone (`rxnc_c03ca`, `rxnc_c03da`) — neurohormonal blockade
- Beta-blocker (`rxnc_c07ab`, `rxnc_c07ag`) — rate control / remodelling
- ACEi/ARB (`rxnc_c09aa`, `rxnc_c09ca`) — neurohormonal blockade
- ARNI (`rxnc_c09dx04`) — highly specific to HFrEF
- SGLT2i (`rxnc_a10bk`) — emerging HF indication (check if DM absent → strong HF signal)
- Digoxin (`rxnc_c01aa` or `rxnc_c01bb`) — rate control / inotropy
- Ivabradine (`rxnc_c01eb`) — if available in EADV, otherwise via CUI

**Proposed logic:**
- `chf_rx_signal`: ARNI present → definite HF treatment (score 3)
- `chf_rx_signal`: Loop diuretic + (ACEi/ARB or BB) → probable HF treatment (score 2)
- `chf_rx_signal`: SGLT2i without DM diagnosis → probable HF indication (score 2)
- `chf_rx_signal`: Loop diuretic alone → possible HF (score 1)
- `chf_gdmt_count`: count of 4 pillars (RAAS blocker, BB, MRA, SGLT2i) — 0 to 4
- `chf_gdmt_gap`: which pillars are missing

**Outputs:**
- `chf_rx_signal` (type 2) — Rx-inferred CHF likelihood (0-3)
- `chf_gdmt_count` (type 2) — GDMT pillars prescribed (0-4)
- `chf_gdmt_gap` (type 1001) — Missing GDMT components

---

### 2. NEW: `cd_cardiac_af_rx` — AF Rate vs Rhythm Control Phenotyping

**Rationale:** Current `cd_cardiac_af` computes CHA2DS2-VASc but doesn't assess the treatment strategy (rate vs rhythm control). Medication patterns distinguish these clearly.

**Medication signals:**
- Rate control: BB (`rxnc_c07%`), CCB non-DHP — verapamil/diltiazem (`rxnc_c08da`, `rxnc_c08db`), digoxin (`rxnc_c01aa`/`rxnc_c01bb`)
- Rhythm control: Amiodarone (`rxnc_c01bd`), flecainide (`rxnc_c01bc`), sotalol (β-blocker with class III — `rxnc_c07aa`)
- Anticoagulation: Already tracked in cd_cardiac_rx

**Proposed logic:**
- `af_rhythm_control`: amiodarone or flecainide present → 1
- `af_rate_control`: (BB or non-DHP CCB or digoxin) and no rhythm agent → 1
- `af_anticoag_status`: bind from cd_cardiac_rx.rxn_anticoag
- `af_rx_gap`: AF diagnosed + CHA2DS2-VASc ≥ 2 + no anticoag → flag

**Outputs:**
- `af_strategy` (type 1001) — Rate vs rhythm control
- `af_anticoag_gap` (type 1001) — Anticoagulation gap flag

---

### 3. NEW: `cd_cardiac_cad_rx_gap` — Secondary Prevention Gap Detection

**Rationale:** Post-ACS and stable CAD patients should be on dual/single antiplatelet + statin + ACEi/ARB + BB. Current `cd_cardiac_cad` tracks whether these meds are present but doesn't flag treatment gaps.

**Proposed logic (requires CAD diagnosis from cd_cardiac_cad):**
- Bind: `cad`, `ami`, `cabg_flag` from cd_cardiac_cad
- Expected therapy post-AMI: antiplatelet + statin + BB + ACEi/ARB (4 agents)
- Expected therapy stable CAD: antiplatelet + statin (2 agents minimum)
- `cad_rx_count`: count of expected agents present
- `cad_rx_gap`: which agents are missing
- `cad_statin_intensity`: dose-level check using rx_cv_lmd CUIs (atorva 40-80mg or rosuva 20-40mg = high intensity)

**Outputs:**
- `cad_rx_gap` (type 1001) — Missing secondary prevention agents
- `cad_statin_intensity` (type 1001) — High vs moderate vs low intensity

---

### 4. NEW: `cd_cardiac_rx_uncoded` — Rx-Inferred Uncoded Cardiac Conditions

**Rationale:** Some patients are treated but never coded. Medication patterns can flag probable uncoded diagnoses for clinical review.

**Inference rules:**
| Medication pattern | Inferred condition | Confidence |
|---|---|---|
| Anticoagulant (DOAC/warfarin) + no AF/VTE/VHD coded | Possible uncoded AF or VTE | Medium |
| ARNI (sacubitril/valsartan) + no CHF coded | Probable uncoded CHF | High |
| Nitrate (ISMN) + no CAD coded | Possible uncoded angina/CAD | Medium |
| Amiodarone/flecainide + no AF coded | Probable uncoded arrhythmia | High |
| Loop diuretic + MRA + BB + ACEi + no CHF coded | Probable uncoded CHF | High |
| SGLT2i + no DM + no CHF coded | Possible uncoded CHF | Medium |
| High-intensity statin + ezetimibe + no CAD/dyslip coded | Possible uncoded FH or high-risk CVD | Low |

**Proposed logic:**
- Cross-bind all existing cardiac diagnoses (AF, CHF, CAD, VTE, VHD)
- Cross-bind all medication flags
- Flag where treatment present but diagnosis absent

**Outputs:**
- `uncoded_af_flag` (type 1001) — Possible uncoded AF
- `uncoded_chf_flag` (type 1001) — Possible uncoded CHF
- `uncoded_cad_flag` (type 1001) — Possible uncoded CAD

---

## Proposed Upgrades to Existing Rules

### 5. UPGRADE: `cd_cardiac_chf` — Add Medication-Based Case Finding

**Current state:** Detects CHF only via ICD/ICPC codes + cardiomyopathy subtypes + ARNI.

**Proposed additions:**
- Add loop diuretic (`rxnc_c03c%`) as supporting evidence
- Add MRA (`rxnc_c03ca`, `rxnc_c03da`) as supporting evidence
- Add SGLT2i without DM as supporting evidence
- Add digoxin (`rxnc_c01aa`/`rxnc_c01bb`) as supporting evidence
- New conditional: `chf_rx_inferred`: high medication signal + no CHF code → flag for review

---

### 6. UPGRADE: `cd_cardiac_af` — Add Treatment Strategy Assessment

**Current state:** Detects AF, computes CHA2DS2-VASc, checks anticoagulation status.

**Proposed additions:**
- Bind rhythm control agents (amiodarone, flecainide) from cd_cardiac_rx or directly
- Bind rate control agents (digoxin, non-DHP CCB)
- New outputs: `af_rate_control`, `af_rhythm_control`, `af_anticoag_gap`

---

### 7. UPGRADE: `cd_cardiac_rx` — Expand Drug Class Coverage

**Current state:** Tracks antiplatelet, anticoag, antiarrhythmics (wildcard c01%), diuretics, statins.

**Proposed additions:**
- Break `rxnc_c01%` wildcard into specific subclasses:
  - `rxn_digoxin`: `rxnc_c01aa` or `rxnc_c01bb`
  - `rxn_amiodarone`: `rxnc_c01bd`
  - `rxn_flecainide`: `rxnc_c01bc`
  - `rxn_nitrate`: `rxnc_c01da`, `rxnc_c01ea`
- Add SGLT2i for cardiac indication: `rxnc_a10bk`
- Add ARNI: `rxnc_c09dx04`
- Add MRA: `rxnc_c03ca`
- Add PCSK9i: `rxnc_c10ax13`

---

### 8. UPGRADE: `cd_htn` — Detect Uncoded Treated Hypertension

**Current state:** Detects HTN via codes or ≥ 3 elevated SBP readings. Tracks medications individually.

**Proposed addition:**
- `htn_rx_uncoded`: Patient on ≥ 2 antihypertensive agents (ACEi/ARB + CCB/BB/thiazide) but no HTN ICD/ICPC code → flag as probable uncoded HTN
- This pattern already partially exists (`htn_obs` check) but doesn't use medication signals

---

## Priority Ranking

| # | Rule | Impact | Effort | Priority |
|---|------|--------|--------|----------|
| 1 | cd_cardiac_chf_rx (GDMT assessment) | High — actionable clinical gaps | Medium | **P1** |
| 4 | cd_cardiac_rx_uncoded (uncoded conditions) | High — case finding | Medium | **P1** |
| 7 | cd_cardiac_rx upgrade (expand drug classes) | High — enables all other rules | Low | **P1** |
| 3 | cd_cardiac_cad_rx_gap (secondary prevention) | High — actionable gaps | Medium | **P2** |
| 2 | cd_cardiac_af_rx (rate/rhythm strategy) | Medium — clinical insight | Low | **P2** |
| 6 | cd_cardiac_af upgrade | Medium — extends existing rule | Low | **P2** |
| 5 | cd_cardiac_chf upgrade | Medium — extends existing rule | Low | **P3** |
| 8 | cd_htn upgrade | Low — partially exists already | Low | **P3** |

---

## Dependencies

```
cd_cardiac_rx (upgrade first — P1)
  ├── cd_cardiac_chf_rx (new)
  ├── cd_cardiac_af_rx (new)
  ├── cd_cardiac_cad_rx_gap (new)
  └── cd_cardiac_rx_uncoded (new)
        ├── binds cd_cardiac_af
        ├── binds cd_cardiac_chf
        ├── binds cd_cardiac_cad
        └── binds cd_cardiac_vte
```

## Notes

- All thresholds and lab values must use **Australian metric units** (mmol/L, not mg/dL)
- ATC codes confirmed present in EADV dictionary: c01aa, c01bb, c01bc, c01bd, c01ca, c01da, c01dx, c01ea, c01eb, c03aa, c03ba, c03ca, c03da, c03db, c07aa, c07ab, c07ag, c08ca, c08da, c08db, c09aa, c09ca, c09dx04, c10aa, c10ab, c10ac, c10ax, c10ax09, c10ax13, a10bk
- SGLT2i (`rxnc_a10bk`) dual indication (DM + HF) needs careful handling — check for DM diagnosis context
