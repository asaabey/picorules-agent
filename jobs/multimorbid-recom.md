# Multi-Morbidity Recommendation Ruleblock — Planning Document

**Status:** Draft / Planning
**Created:** 2026-04-20
**Scope:** Federation of per-disease recommendation ruleblocks + orchestrator, producing specific regimen combinations ranked by multi-indication utility.

---

## 1. Scope & Design Decisions (confirmed)

| # | Decision | Implication |
|---|---|---|
| 1 | **Federation (B)** — one ruleblock per disease + thin orchestrator | Each disease tracks its own guideline; conflict-resolution lives in the orchestrator only |
| 2 | **Specific regimen combinations** | Need drug-level (not just class-level) logic, dose-adjustment hooks, interaction flags |
| 3 | **Rank by number of comorbid indications satisfied** | A "drug utility score" is computed across domains; tie-breaking by safety profile |
| 4 | **Latest consensus** (verified current as of 2026-04) | See §3 |
| 5 | **MASLD = modifier, not full domain** (for now) | Influences DM2/obesity/lipid choices; lifestyle + weight-loss-Rx flag only |
| 6 | **Parallel prognostic scoring** | HF risk, KFRE, MACE-in-established-disease live alongside existing CVD risk |
| 7 | **All 4 output attribute shapes** | `recom_<drug>`, `_indications`, `_priority`, `gap_<domain>` |

---

## 2. Diseases In Scope

| Disease | Dedicated Ruleblock | Prognostic Score | Upstream (verified present) |
|---|---|---|---|
| Type 2 Diabetes | `cd_dm_recom.prb` (new) | HbA1c trajectory, UACR trend | `cd_dm_dx`, `cd_dm_mx`, `cd_dm_glyc_cntrl`, `cd_dm_rx_rcm`, `cd_dm_comp` |
| Hypertension | `cd_htn_recom.prb` (new) | BP control metric, SPRINT-eligibility flag | `cd_htn`, `cd_htn_bp_control`, `cd_htn_rcm` |
| Ischaemic Heart Disease | `cd_cardiac_cad_recom.prb` (new) | SMART-2 / REACH MACE | `cd_cardiac_cad` (CAD/AMI/CABG/MACE) |
| Heart Failure | `cd_cardiac_chf_recom.prb` (new) | MAGGIC / WATCH-DM | `cd_cardiac_chf` (CHF/DCM/HOCM/ARNI), `cd_cardiac_ix` (LVEF via `echo_ld`) |
| CKD | `ckd_recom.prb` (new) | KFRE 2-yr/5-yr | `ckd`, `ckd_egfr_metrics`, `ckd_uacr_metrics`, `ckd_prog_vm` |
| MASLD (modifier) | `cd_masld.prb` (in dev) → extend with `masld_fib_stage`, `masld_rx_flag` outputs | FIB-4, ELF proxy | `cd_masld` |
| **Orchestrator** | `cd_multimorbid_recom.prb` (new) | — | Binds all six above + `cvra_ensemble` + `cd_cardiac_rx` + `cd_dyslip` |

**Gate for inclusion:** prevalence > 5% in target population AND ≥1 disease-modifying pharmacotherapy with hard-outcome evidence AND a defined stage/severity marker computable from EADV.

---

## 3. Evidence Anchors (verified 2026-04)

| Domain | Primary guideline | Key 2024–2026 updates relevant to multi-morbid logic |
|---|---|---|
| DM2 | ADA Standards of Care 2026, EASD | GLP-1 RA / SGLT2i first-line when ASCVD/HF/CKD present (regardless of HbA1c/metformin status) |
| HTN | NHF Australia 2016 (under review), ESC 2024, AHA/ACC 2025 | SPRINT-style target (SBP<120) when high-risk and tolerated; RAAS+CCB+thiazide before beta-blocker (unless IHD/HF) |
| IHD | ESC 2024 Chronic Coronary Syndromes | SGLT2i/GLP-1 added as cardiometabolic pillar alongside antiplatelet+statin+RAASi+BB |
| HF | ESC 2023 focused update, HFA 2024 | Quadruple therapy HFrEF (ARNI/ACEi + BB + MRA + SGLT2i); SGLT2i across EF spectrum; **semaglutide** for obese HFpEF (STEP-HFpEF); finerenone for HFmrEF/HFpEF (FINEARTS-HF) |
| CKD | **KDIGO 2024** | SGLT2i for proteinuric CKD ± DM; finerenone in T2D+CKD; GLP-1 RA kidney-protective; cystatin C for eGFR when drug-dosing-critical |
| MASLD | **AASLD Nov 2025 update** + EASL-EASD-EASO 2024 + Younossi 2025 global consensus | Resmetirom for non-cirrhotic MASH F2–F3; **semaglutide FDA-approved Aug 2025** for MASH F2–F3; GLP-1/SGLT2i preferred in DM+MASLD |

**Action item before build:** lock a citation table (`reference/citations/multimorbid_refs.md`) mapping each recommendation clause → guideline section/page/DOI. Required for audit trail on `#doc(cite:...)` tags.

---

## 4. Drug Universe & Indication Matrix

This is the **heart** of the design — a matrix the orchestrator consults to compute utility.

| Drug class / agent | DM2 | HTN | IHD | HFrEF | HFpEF | CKD (prot) | MASLD | Indications count |
|---|---|---|---|---|---|---|---|---|
| **SGLT2i** (empa/dapa) | ✔ | (✔) | ✔ | ✔ | ✔ | ✔ | (✔) | **6–7** |
| **GLP-1 RA** (sema/tirze) | ✔ | — | ✔ | (✔ HFpEF obese) | ✔ | ✔ | ✔ (sema F2-3) | **5–6** |
| **ACEi / ARB** | (✔ DKD) | ✔ | ✔ | ✔ | (✔) | ✔ | — | 5 |
| **ARNI** (sac/val) | — | ✔ | — | ✔ | (✔) | — | — | 2–3 |
| **MRA** (spiro/epler) | — | ✔ (resistant) | (✔ post-MI) | ✔ | ✔ | — | — | 3–4 |
| **Finerenone** | ✔ (T2D+CKD) | — | — | (✔ HFmrEF/HFpEF) | (✔) | ✔ | — | 3 |
| **Beta-blocker** | — | (✔) | ✔ | ✔ | — | — | — | 2–3 |
| **CCB** (amlo) | — | ✔ | ✔ (angina) | — (avoid non-DHP in HFrEF) | — | — | — | 2 |
| **Thiazide** | — | ✔ | — | — | — | — | — | 1 |
| **Statin** | ✔ | — | ✔ | — | — | ✔ | (✔) | 3–4 |
| **Ezetimibe** | — | — | ✔ (add-on) | — | — | — | — | 1 |
| **PCSK9i** | — | — | ✔ (very high risk) | — | — | — | — | 1 |
| **Antiplatelet** | — | — | ✔ | — | — | — | — | 1 |
| **Resmetirom** | — | — | — | — | — | — | ✔ (F2–F3) | 1 |

**Matrix encoding plan:** express as a `#doc`-annotated conditional table inside the orchestrator, OR (preferred) externalise as `reference/data/drug_indication_matrix.csv` and generate Picorules snippets programmatically. The externalised approach wins because:
- The matrix is reviewed by clinicians outside the Picorules toolchain.
- Updates (e.g. finerenone HFpEF label expansion) become a CSV diff, not a ruleblock rewrite.
- Weight columns (next section) can be tuned without touching Picorules source.

---

## 4b. Indication Weighting Scheme

Not all indications are equal. Unweighted counting treats "SGLT2i for HFrEF (Class I, Level A, mortality benefit, NNT~22)" identically to "SGLT2i for MASLD (subgroup signal, surrogate endpoint)" — which distorts ranking. Three weight dimensions:

### Dim 1 — Evidence strength (guideline class × level)
| Class × Level | Weight |
|---|---|
| I / A | 1.0 |
| I / B  or  IIa / A | 0.7 |
| IIa / B | 0.5 |
| IIb (any level) | 0.3 |
| Off-label / emerging | 0.2 |

### Dim 2 — Outcome magnitude
| Outcome type | Weight |
|---|---|
| Hard (all-cause mortality, CV death, MACE, KRT, HF hospitalisation, liver-related mortality) | 1.0 |
| Composite with surrogate | 0.6 |
| Surrogate only (HbA1c, LDL, liver fat, MASH resolution without fibrosis) | 0.3 |

### Dim 3 — Patient-specific severity modifier (runtime)
Scales the cell weight up/down based on EADV-observable severity. Encoded as a Picorules expression in the CSV `severity_expr` column. Examples:

| Drug × disease | severity_expr |
|---|---|
| SGLT2i × HFrEF | `lvef < 30 => 1.2 ; => 1.0` |
| SGLT2i × CKD | `uacr > 300 => 1.3 ; uacr > 30 => 1.0 ; => 0.7` |
| GLP-1 × DM2 | `hba1c > 75 => 1.2 ; => 1.0` |
| MRA × HFrEF | `lvef < 35 => 1.2 ; => 1.0` |
| Statin × IHD | `ldl > 2.6 => 1.2 ; => 1.0` |

### Composite weight
```
cell_weight[d,dx]          = evidence_w × outcome_w                 (static, in CSV)
effective_weight[d,dx]     = cell_weight[d,dx] × severity_mod[d,dx] (runtime)
```

### Starter weights — five pivotal drug classes × six diseases

Format: **`cell_weight (evidence_w × outcome_w)`** — dash `—` = no indication.

| Drug | DM2 | HTN | IHD | HFrEF | HFpEF | CKD (prot) | MASLD |
|---|---|---|---|---|---|---|---|
| **SGLT2i** | 0.7 (1.0×0.7)† | — | 0.5 (0.7×0.7) | **1.0** (1.0×1.0) | 0.7 (1.0×0.7) | **1.0** (1.0×1.0) | 0.14 (0.2×0.7) |
| **GLP-1 RA** | 0.7 (1.0×0.7)† | — | 0.7 (1.0×0.7) | 0.3 (0.5×0.6) | 0.5 (1.0×0.5)‡ | 0.5 (0.7×0.7) | **1.0** (1.0×1.0)§ |
| **ACEi / ARB** | 0.5 (1.0×0.5)¶ | **1.0** (1.0×1.0) | 0.7 (1.0×0.7) | **1.0** (1.0×1.0) | 0.3 (0.5×0.6) | **1.0** (1.0×1.0) | — |
| **MRA** (steroidal) | — | 0.3 (0.5×0.6) | 0.5 (0.7×0.7) | **1.0** (1.0×1.0) | 0.5 (0.7×0.7)§§ | — | — |
| **Finerenone** | 0.7 (1.0×0.7) | — | — | 0.5 (0.7×0.7) | 0.5 (0.7×0.7) | **1.0** (1.0×1.0) | — |

† DM2 baseline: evidence I/A for ASCVD/HF/CKD benefit, but primary DM2 endpoint is HbA1c (surrogate) → 0.7.
‡ STEP-HFpEF / STEP-HFpEF-DM: symptomatic/QoL benefit, not yet Class I for mortality → 0.5.
§ Semaglutide FDA-approved Aug 2025 for MASH F2–F3 with histological endpoints → 1.0.
¶ ACEi/ARB in DM2 gated on albuminuria, not all DM2 → 0.5.
§§ MRA in HFpEF: TOPCAT subgroup signal, not Class I → 0.5.

### Revised utility formula
```
recom_state_factor(s) : s=1 (initiate)  => 10
                        s=3 (intensify) => 7
                        s=2 (consider)  => 5
                        s=4 (maintain)  => 3
                        s=0 (none)      => 0

utility[d] = Σ_dx ( cell_weight[d,dx] × severity_mod[d,dx] × recom_state_factor(recom_<dx>_<d>) )
           + safety_bonus[d]
           + simplicity_bonus[d]
           - cost_penalty[d]

ranked_drug[d] = utility[d]  if  ci_block_<d> = 0  else  -∞
```

### Worked example — 65M, DM2 + HFrEF (LVEF 28) + CKD3b (UACR 450) + MASLD F2
All four diseases would emit `recom_<dx>_<drug> = 1` (initiate) for SGLT2i and GLP-1 RA.

| Drug | Contribution breakdown | Utility |
|---|---|---|
| SGLT2i | DM2: 0.7×1.0×10 + HFrEF: 1.0×**1.2**×10 + CKD: 1.0×**1.3**×10 + MASLD: 0.14×1.0×10 | **33.4** |
| GLP-1 RA | DM2: 0.7×1.0×10 + HFrEF: 0.3×**1.2**×10 + CKD: 0.5×**1.3**×10 + MASLD: 1.0×1.0×10 | **27.1** |
| ACEi / ARB | DM2: 0.5×1.0×10 + HFrEF: 1.0×1.2×10 + CKD: 1.0×1.3×10 | **30.0** |
| Finerenone | DM2: 0.7×1.0×10 + HFrEF: 0.5×1.2×10 + CKD: 1.0×1.3×10 | **26.0** |

Unweighted, SGLT2i and GLP-1 RA tie at 4 indications each. Weighted, SGLT2i wins clearly, ACEi/ARB is a strong second — matching clinical intuition for a HFrEF-dominant phenotype.

---

## 5. Calculation System — Arriving at Drug Combinations

### Stage 1 — Per-disease recommendation
Each `cd_<dx>_recom.prb` independently emits, for every relevant drug class:
```
recom_<dx>_<drug> : 0=none, 1=initiate, 2=consider, 3=intensify, 4=maintain
```
Matching the convention already established in `cd_cvra_recom.prb`.

### Stage 2 — Cross-disease aggregation (orchestrator)
For each drug class `d`:
```
drug_indications_n[d]  = count of diseases where recom_<dx>_<d> ∈ {1,2,3}
drug_initiation_n[d]   = count where recom_<dx>_<d> = 1
drug_maintenance_n[d]  = count where recom_<dx>_<d> = 4
drug_indications_lst[d]= backtick-list of disease codes
```

### Stage 3 — Weighted utility score
See §4b for the full weighting scheme. Summary:
```
utility[d] = Σ_dx ( cell_weight[d,dx] × severity_mod[d,dx] × recom_state_factor(recom_<dx>_<d>) )
           + safety_bonus[d]        // +/-, based on per-patient tolerability signals
           + simplicity_bonus[d]    // +1 oral, +1 once-daily
           - cost_penalty[d]        // regional, config-driven (e.g. PBS authority barrier)
```
`cell_weight` comes from `drug_indication_matrix.csv`; `severity_mod` is evaluated at runtime from EADV observables via the CSV's `severity_expr` column.

### Stage 4 — Contraindication overlay
A second matrix: `drug × contraindication_condition`. Examples:
- non-DHP CCB × HFrEF → **hard block**
- TZD × HF → **hard block** (even though pioglitazone benefits MASLD)
- MRA × eGFR<30 or K>5.0 → **hard block**
- SGLT2i × eGFR<20 or active DKA risk → **hard block**
- GLP-1 RA × personal/family MTC → **hard block**
- ACEi/ARB × K>5.5 or bilateral RAS → **hard block**

Output: `ci_block_<drug>` flags. Feed into utility as -∞.

### Stage 5 — Regimen selection
Rank drugs by `utility[d]` descending, filtered by `ci_block_<drug>=0`.
Output:
- `recom_regimen_top3` — top 3 drug classes by utility (comma-separated string)
- `recom_priority_1`, `_2`, `_3` — drug code + primary indication
- `recom_regimen_rationale` — backtick-joined string of contributing domains

### Stage 6 — Gaps & concordance
Per disease, `gap_<dx>_<drug>` already emitted. Orchestrator rolls up:
- `gap_total_n`
- `gap_multimorb_priority_n` (gaps where drug would cover ≥2 domains — these are the "highest-leverage" gaps)
- `concordance_pct_overall` (weighted mean of per-disease concordance)

---

## 6. Binding Architecture

```
                     ┌──────────────────────────────┐
                     │  cd_multimorbid_recom.prb    │
                     │  (orchestrator)              │
                     └──────────────┬───────────────┘
                                    │ binds
      ┌──────────────┬──────────────┬──────┴──────────┬──────────────────┬──────────────┐
      │              │              │                 │                  │              │
  cd_dm_recom  cd_htn_recom  cd_cardiac_cad_recom  cd_cardiac_chf_recom  ckd_recom     │
      │              │              │                 │                  │              │
      └─bind──┬──────┴─bind─────────┴─bind────────────┴─bind─────────────┴─bind────────┤
             │                                                                          │
      cvra_ensemble / cd_cvra_recom  (existing — CVD risk)                              │
             │                                                                          │
      cd_dm_dx / cd_dm_mx / cd_dm_glyc_cntrl / cd_htn / cd_htn_bp_control /             │
      cd_cardiac_cad / cd_cardiac_chf / cd_cardiac_ix / cd_cardiac_rx /                 │
      ckd / ckd_egfr_metrics / ckd_uacr_metrics / cd_dyslip / cd_obesity / cd_masld     │
```

Each new `cd_<dx>_recom` ruleblock depends **only** on existing phenotyping ruleblocks, **with one deliberate exception**: all recom blocks bind the `ci_block_*` contraindication signals from `ckd_recom` to avoid re-deriving K+/eGFR thresholds. This creates a shallow two-layer DAG (ckd_recom first, then the other four) and keeps the renal-safety policy authoritative in one place. The orchestrator sits above all five.

---

## 7. Attribute Schema (output contract)

Per-disease ruleblock (example: DM2):
```
recom_dm2_sglt2i         type=2   0|1|2|3|4
recom_dm2_glp1           type=2   0|1|2|3|4
recom_dm2_metformin      type=2   0|1|2|3|4
recom_dm2_indications    type=1   backtick list
gap_dm2_sglt2i           type=1001 0|1
gap_dm2_hba1c_target     type=1001 0|1
concordance_dm2_pct      type=2    0-100
```

Orchestrator outputs:
```
drug_sglt2i_ind_n         type=2   0-6
drug_sglt2i_ind_lst       type=1   `DM2,HF,CKD`
drug_sglt2i_utility       type=2   signed int
ci_block_sglt2i           type=1001
recom_priority_1          type=1   `SGLT2i for DM2+HF+CKD`
recom_priority_2          type=1
recom_priority_3          type=1
gap_multimorb_priority_n  type=2
concordance_pct_overall   type=2   0-100
```

---

## 8. Open Questions — Need Your Input

1. **Drug granularity.** Go down to specific agent (empagliflozin vs dapagliflozin) or stop at class? Specific agent lets us encode e.g. "dapagliflozin has DAPA-HF/DAPA-CKD evidence, empa has EMPEROR — prefer X in Y". But it doubles the matrix size.
2. **Dose adjustment.** In scope, or out of scope for v1? (I'd recommend out of scope — delegate to prescribing software.)
3. **Cost / formulary.** Region-configurable weight (PBS in AU)? Or ignore and produce guideline-ideal regimen only?
4. **Stacking limits.** Max number of new initiations to recommend in one visit (e.g. "don't start 4 new drugs at once — pick top 2")? Clinically realistic but adds state.
5. **Timing / sequencing.** Do you want `recom_priority_sequence` encoding the *order* of initiation (e.g. "RAAS first, then SGLT2i at 2w, then MRA at 4w") or just the *set*?
6. **Confirmation of upstream availability.** I need to verify these ruleblocks exist — can you confirm, or should I grep `reference/rules/` first?
   - `rout_cd_ihd` / `cd_ihd`
   - `rout_cd_hf` / `cd_hf`
   - `rout_cd_dm2` / `cd_dm2`
   - presence of UACR, potassium, cystatin C, NT-proBNP, LVEF attributes in EADV dictionary
7. **First Nations adjustment.** `cd_cvra_recom` uses `fnp` to reclassify risk upward and shorten reassess interval. Apply same logic across all per-disease ruleblocks, or centralise in orchestrator?
8. **MASLD promotion path.** At what point does MASLD graduate from "modifier" to full recommendation domain? Trigger could be: local prevalence of resmetirom/semaglutide-F2F3 eligibility reaching a threshold, OR publication of an AU-specific guideline.

---

## 9. Phased Build Plan

**Phase 0 — Groundwork (1–2 days)**
- Confirm upstream ruleblock availability (Q6 above).
- Lock citation table.
- ✅ Starter `reference/data/drug_indication_matrix.csv` drafted (14 drugs × 7 diseases, 98 cells).
- ✅ Starter `reference/data/drug_contraindication_matrix.csv` drafted (39 rules across 14 drugs).
- Clinician review of starter weights (§4b) — especially the MASLD row and HFpEF column where evidence is evolving fastest.
- Write 3–5 canonical test patient fixtures (e.g. "65M, DM2+HFrEF+CKD3b+MASLD-F2", "70F, HTN+IHD+CKD2", "50M, DM2+MASLD only") with expected regimen *and expected utility scores* so weight-tuning regressions get caught.

**Phase 1 — Per-disease ruleblocks (3–5 days)**
- Build in this order: `ckd_recom` → `cd_cardiac_chf_recom` → `cd_dm_recom` → `cd_cardiac_cad_recom` → `cd_htn_recom`.
- Rationale: CKD first because it supplies most contraindication signals (eGFR, K, UACR); CHF second because drug universe is largest.
- Each ruleblock compiles standalone and produces its own `concordance_<dx>_pct` for unit-level validation.

**Phase 2 — Orchestrator (2–3 days)**
- Bind all per-disease outputs.
- Implement utility calculation and CI overlay.
- Emit priority list.

**Phase 3 — Validation (2 days)**
- Run fixtures; compare recommended regimen to clinician expectation.
- Edge cases: all-contraindicated patient, no-disease patient, MASLD-only patient.

**Phase 4 — MASLD extension (deferred)**
- Promote MASLD from modifier to full domain once AASLD-aligned Australian guidance lands.

---

## 10. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Guideline drift — anything we encode now will be out-of-date in 12 months | Externalised matrices (CSV), citation table with versions, quarterly review cadence |
| Combinatorial explosion of conditional clauses in orchestrator | Matrix-driven code-gen instead of hand-written conditionals |
| Conflicting recommendations between per-disease ruleblocks (e.g. HF wants beta-blocker, COPD discourages) | Explicit contraindication matrix is **authoritative**; per-disease ruleblocks recommend in isolation, orchestrator resolves |
| EADV attribute gaps (e.g. LVEF, NT-proBNP not consistently captured) | Phase 0 audit of attribute presence; degrade gracefully with `nvl()` and flag `data_completeness_<dx>` |
| Over-prescribing risk if rules recommend many initiations | Stacking limit (Q4) + `recom_priority_top3` surfaces only the highest-utility moves |
| Clinician distrust of "black box" utility score | Every recommendation carries `_indications` list + `_rationale` string showing *why* |

---

## References

[1] [2024 update in heart failure](https://consensus.app/papers/details/04740fb416dc578daf4c87be6c9b688b/?utm_source=claude_desktop) (Beghini et al., 2024, ESC Heart Failure)
[2] [KDIGO 2024 clinical practice guideline on evaluation and management of chronic kidney disease](https://consensus.app/papers/details/f620a7e429c459beb0daaaa069bee2b8/?utm_source=claude_desktop) (Awdishu et al., 2025, AJHP)
[3] [Semaglutide therapy for MASH: November 2025 updates to AASLD Practice Guidance](https://consensus.app/papers/details/9aacc4b83d2c5c9c942911c156f92ce3/?utm_source=claude_desktop) (Bansal et al., 2025, Hepatology)
[4] [Global Consensus Recommendations for MASLD and MASH](https://consensus.app/papers/details/1638ec19964058ad8b40b28d8ac83ec9/?utm_source=claude_desktop) (Younossi et al., 2025, Gastroenterology)
[5] [Key takeaways from the updated multidisciplinary European MASLD guidelines](https://consensus.app/papers/details/75a3a311de775d6f97c9f369c55c763f/?utm_source=claude_desktop) (Horn et al., 2025, eGastroenterology)
