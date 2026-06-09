# Multi-Morbidity Recom Ruleblocks — Overlap Audit

**Date:** 2026-04-22
**Scope:** `new_rules/ckd_recom.prb`, `new_rules/cd_cardiac_chf_recom.prb`, `new_rules/cd_dm_recom.prb`, `new_rules/cd_cardiac_cad_recom.prb`, `new_rules/cd_htn_recom.prb`, `new_rules/cd_multimorbid_recom.prb`.

The federation design recommended by the planning doc is working, but audit of the actual files shows three layers of redundancy worth addressing before Phase 3 validation or production deployment.

---

## 1. Drug-Recommendation Overlap (the big one)

Each per-disease block independently computes a drug-recommendation state (`recom_<dx>_<drug> ∈ {0,1,2,3,4}`) for its drug set. Multi-indication drugs therefore end up computed 3–4 times with near-identical gating logic.

| Drug | Computed in | Cells | Redundant logic |
|---|---|---|---|
| **SGLT2i** | `ckd_recom`, `cd_cardiac_chf_recom`, `cd_dm_recom`, `cd_cardiac_cad_recom` | 4 | Same eGFR<20 block; same `rx_sglt2` bind; overlapping "is prescribed → maintain" branch |
| **GLP-1 RA** | `ckd_recom`, `cd_cardiac_chf_recom`, `cd_dm_recom`, `cd_cardiac_cad_recom` | 4 | Same `rx_glp1` bind; overlapping "maintain if on Rx" branch |
| **ACEi/ARB** | `ckd_recom`, `cd_cardiac_chf_recom`, `cd_cardiac_cad_recom`, `cd_htn_recom` | 4 | Same `ci_block_acei_arb` check; `rx_raas` composite re-derived in 3 blocks |
| **Statin** | `ckd_recom`, `cd_dm_recom`, `cd_cardiac_cad_recom` | 3 | LDL-above-target check re-derived with different thresholds (1.8 vs 2.6) |
| **Beta-blocker** | `cd_cardiac_chf_recom`, `cd_cardiac_cad_recom`, `cd_htn_recom` | 3 | `rx_bb` bound 3 times |
| **MRA** | `cd_cardiac_chf_recom`, `cd_htn_recom` | 2 | `rx_mra_dt` derived twice via direct EADV |

**SQL cost:** each `recom_<dx>_<drug>` becomes a CTE in the generated SQL. At 15 redundant cells this is ~15 extra CTEs per execution. On a 1M-patient warehouse that is 15M redundant row evaluations per nightly run.

**Orchestrator cost:** `cd_multimorbid_recom` then wraps each of those cells in an `rsf_<dx>_<drug>` state-factor conditional (28 such conditionals). The orchestrator is ~250 lines of mostly-mechanical mapping.

---

## 2. Binding Overlap

The same upstream attribute is bound from multiple recom ruleblocks. Each bind is a fresh JOIN in SQL and a fresh lookup in the JS runtime.

| Upstream | Bound by |
|---|---|
| `rout_cd_htn.htn_rxn_acei` | ckd, chf, cad, htn (4×) |
| `rout_cd_htn.htn_rxn_arb` | ckd, chf, cad, htn (4×) |
| `rout_cd_htn.htn_rxn_bb` | chf, cad, htn (3×) |
| `rout_cd_dyslip.rx_statin` | ckd, dm, cad (3×) |
| `rout_cd_dm_rx_rcm.sglt2_f` | ckd, chf, dm, cad (4×) |
| `rout_cd_dm_rx_rcm.glp1_f` | ckd, chf, dm, cad (4×) |
| `rout_ckd_recom.ci_block_acei_arb` | chf, cad, dm, htn (4×) |
| `rout_cd_dm_dx.cd_dm_dx` | cad, htn (2×) |
| `rout_cd_cardiac_chf.chf` | dm, htn (2×) |

---

## 3. Logic Overlap

Identical or near-identical small computations re-derived:

- **`rx_raas` composite** = `greatest(rx_acei, rx_arb) > 0` — derived in `cd_cardiac_chf_recom`, `cd_cardiac_cad_recom`, `cd_htn_recom`. CHF additionally folds ARNI into the same concept.
- **`ldl_above_target`** — derived in `ckd_recom` (threshold 1.8) and `cd_cardiac_cad_recom` (threshold 1.8 *and* 2.6). Different thresholds are intentional, but the presence check `ldl_val !?` is duplicated.
- **`high_cv_risk`** flag in `cd_dm_recom` replicates a concept that partially overlaps with `cvra_cat_r` (already computed in `cd_cvra_recom`).

---

## 4. Orchestrator Combinatorial Expansion

`cd_multimorbid_recom` contains:
- 28 `rsf_*_*` conditionals, each with identical structural shape `{state=1→10, 3→7, 2→5, 4→3, 0→0}`. Any change to the state-factor mapping requires editing 28 places.
- 13 `u_<drug>` sum expressions. Each adds a new CTE.
- A 13-way `top_drug` ladder.

The orchestrator is long, mechanical, and brittle to guideline changes because adding a new indication to any drug means editing both the per-disease block AND the orchestrator's `u_<drug>` summation.

---

## Consolidation Options

### Option A — Drug-centric recommendation layer (biggest win)

Invert the architecture. Per-disease blocks stop emitting `recom_<dx>_<drug>`. Instead, they emit **clinical context variables** the drug layer consumes:

- `ckd_recom` → `ckd_present`, `proteinuric`, `proteinuric_high`, `ci_block_*`, `sev_ckd_acr`
- `cd_cardiac_chf_recom` → `chf_present`, `hfref_likely`, `obesity_hfpef_candidate`
- `cd_dm_recom` → `dm_present`, `hba1c_above_target`, `high_cv_risk`
- `cd_cardiac_cad_recom` → `cad_present`, `post_mi`, `ldl_above_target`
- `cd_htn_recom` → `htn_present`, `sbp_above_target`, `resistant_htn`

Then a new single block `cd_drug_recom.prb` computes every drug once, gating on the full multi-morbid context:

```
recom_sglt2i : { ci_block_sglt2i = 1 => 0 },
               { ckd_present = 1 and proteinuric = 1 and rx_sglt2 = 0 => 1 },
               { chf_present = 1 and rx_sglt2 = 0 => 1 },
               { dm_present = 1 and high_cv_risk = 1 and rx_sglt2 = 0 => 1 },
               { rx_sglt2 = 1 => 4 },
               { => 0 };
```

This single conditional replaces four `recom_<dx>_sglt2i` conditionals plus the orchestrator's `rsf_*_sglt2i` + `u_sglt2i` machinery.

**Pros:** Eliminates ~70% of the orchestrator. One place to change SGLT2i logic. Utility score reduces to counting which `recom_*` branches fired, via a simpler mapping.
**Cons:** Loses per-disease concordance scoring (which tracks "is CKD being managed?" vs "is DM being managed?"). Concordance would need to be reconstructed from the drug layer + context flags — doable but more indirect.

### Option B — Shared med-inventory block

Introduce `cd_med_inventory.prb` that binds every `rx_*` flag once and re-exports them. All recom blocks then bind from `rout_cd_med_inventory` instead of the original sources.

**Pros:** Trivial to build; removes binding redundancy (Section 2 of this audit).
**Cons:** Doesn't touch the main overlap problem (per-drug recommendation duplication).

### Option C — Keep federation, add drug-level view

Leave the per-disease blocks untouched. Add a new thin block `cd_drug_view.prb` that only computes, per drug, the *maximum* `recom_<dx>_<drug>` across diseases. The orchestrator then consumes this instead of re-aggregating.

```
recom_sglt2i_max : { . => greatest(r_ckd_sglt2i, r_chf_sglt2i, r_dm_sglt2i, r_cad_sglt2i) };
```

**Pros:** Low-risk, additive. Per-disease concordance preserved. Orchestrator shrinks dramatically.
**Cons:** Redundant per-disease computation still happens upstream. Masks rather than solves.

### Option D — Hybrid (recommended)

Do **A + B** together. Move drug decisions into a single `cd_drug_recom.prb`. Move shared med-inventory into `cd_med_inventory.prb`. Per-disease blocks shrink to phenotype+target+severity. Concordance lives in a separate `cd_concordance.prb` that consumes both the drug layer and per-disease context.

Final DAG:
```
upstream phenotyping (cd_htn, cd_dyslip, cd_dm_*, ckd, cd_cardiac_*, cd_obesity)
    │
    ▼
cd_med_inventory                 (Section 2 consolidation)
    │
    ▼
per-disease context blocks       (shrunken: no drug decisions)
    │                            ckd_context, chf_context, dm_context, cad_context, htn_context
    ▼
cd_drug_recom                    (Section 1 consolidation: single-pass drug decisions)
    │
    ▼
cd_concordance                   (rolls up per-domain concordance)
    │
    ▼
cd_multimorbid_recom             (shrunken: just utility ranking + gap surface)
```

---

## Open Questions Before Refactor

1. **Do we lose anything clinically** by collapsing per-disease `recom_<dx>_<drug>`? My read: no — the multi-morbid view is the clinically useful one; per-disease recom was a convenience for the orchestrator, not a deliverable.
2. **Concordance granularity.** Option A/D requires reconstructing per-disease concordance from the drug-level output. Is per-disease concordance a required reporting surface, or is `concordance_pct_overall` sufficient?
3. **Compilation cost vs readability.** Keeping federation is more verbose but more clinician-readable (each disease block is a self-contained document). The drug-centric block trades readability for efficiency. Which is the priority?
4. **Migration path.** Can be staged: build `cd_drug_recom` alongside existing blocks, compare outputs on fixtures, then retire per-disease `recom_*` once equivalence is verified.

---

## Recommendation

Adopt **Option D** with a staged migration. Biggest immediate wins:

1. Build `cd_med_inventory` first — trivial, risk-free, removes 20+ redundant binds.
2. Build `cd_drug_recom` alongside existing blocks; validate parity on fixtures.
3. Strip per-disease `recom_*` once parity is confirmed; collapse orchestrator to utility ranking only.
4. Move concordance to `cd_concordance` — whether per-disease scoring stays depends on Q2 above.

Estimated line-count reduction: orchestrator from ~255 lines to ~60; combined per-disease blocks from ~750 to ~400; net new code ~150 (med_inventory + drug_recom + concordance). Total library shrinks ~40% with semantically equivalent output.
