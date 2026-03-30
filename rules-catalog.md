# Rules Catalog

First-pass catalog for `reference/rules/picodomain_rule_pack/rule_blocks/*.prb`.

This index is based on static analysis plus light context inference from rule descriptions, `#doc(...)` blocks, citations, bindings, filenames, and queried attributes. It is meant for triage and review, not as a substitute for compile-time validation or clinician sign-off.

- **Indexed rules:** 168
- **Entry format:** one section per rule with purpose, key inputs/dependencies, likely issues or review targets, suggested fixes, and possible improvements
- **Confidence note:** when the rule text is ambiguous, entries say “inferred” or “review target” rather than claiming a confirmed defect

## `acr_graph`

- **Primary purpose:** plot acr graph.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`; attributes: `lab_ua_acr`; families: urine labs
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `acr_metrics`

- **Primary purpose:** Summarize albumin-creatinine ratio measurements and severity bands.
- **Key inputs / dependencies:** attributes: `lab_ua_acr`; families: urine labs
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination. Review target: the ruleblock is marked inactive (`is_active:0`), so it may be incomplete, deprecated, or not ready for production use.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed. Confirm whether the rule should remain inactive; if not, complete validation and activate it intentionally.
- **Potential improvements:** Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ad_aki`

- **Primary purpose:** identify AKI in last 12 months.
- **Key inputs / dependencies:** binds: `rout_tg4100.cr_base_max_1y_qt`, `rout_tg4100.akin_stage`, `rout_tg4100.aki_outcome`; attributes: `icd_n17%`; families: ICD coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `at_risk`

- **Primary purpose:** assess at_risk.
- **Key inputs / dependencies:** binds: `rout_ckd.ckd`, `rout_rrt.rrt`, `rout_cd_dm_dx.dm`, `rout_cd_htn.cd_htn`, `rout_cd_cardiac_cad.cad`; attributes: `icd_%`, `icpc_%`, `lab_%`, `rxnc_%`, `obs_%`; families: ICD coding, ICPC coding, RxNorm/ATC medication codes, observations; citations: `at_risk_ckd_ref1`, `at_risk_ckd_ref2`, `at_risk_ckd_ref3`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library.

## `at_risk_dense`

- **Primary purpose:** This is the at_risk_dense algorithm.
- **Key inputs / dependencies:** binds: `rout_ckd_dense.ckd`, `rout_ckd_dense.rrt`, `rout_ckd_dense.alive`; attributes: `icpc_u99035`, `icpc_u99036`, `icpc_u99037`, `icpc_u99043`, `icpc_u99044`; families: ICPC coding, ICD coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Review target: the ruleblock is marked inactive (`is_active:0`), so it may be incomplete, deprecated, or not ready for production use. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Confirm whether the rule should remain inactive; if not, complete validation and activate it intentionally. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `bi_vm`

- **Primary purpose:** Defined stable view of data for BI.
- **Key inputs / dependencies:** binds: `rout_dmg_hrn.hrn_last`, `rout_dmg_loc.loc_mode_24`, `rout_dmg_loc.loc_mode`, `rout_dmg_loc.loc_def`, `rout_dmg_loc.dmg_loc`
- **Logical errors / review targets:** Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `bp_graph`

- **Primary purpose:** Prepare blood pressure trend outputs for graphing or display.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`, `rout_cd_htn.cd_htn`, `rout_cd_htn_bp_control.sbp_max`, `rout_cd_htn_bp_control.sbp_min`, `rout_cd_htn_bp_control.sbp_target_max`; attributes: `obs_bp_systolic`; families: observations
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ca_breast`

- **Primary purpose:** This is a algorithm to identify breast carcinoma.
- **Key inputs / dependencies:** attributes: `icd_c50%`, `icpc_x76001`, `icpc_x76002`, `rxnc_l02bg`, `rxnc_l02ba`; families: ICD coding, ICPC coding, RxNorm/ATC medication codes
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ca_careplan`

- **Primary purpose:** This is a algorithm to identify cancer careplan.
- **Key inputs / dependencies:** attributes: `enc_op_onc_%`; families: encounters
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ca_crc`

- **Primary purpose:** This is a algorithm to identify colorectal.
- **Key inputs / dependencies:** attributes: `icd_c18%`, `icd_c19%`, `icd_c20%`, `icpc_d75%`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ca_endometrial`

- **Primary purpose:** This is a algorithm to identify endometrial carcinoma.
- **Key inputs / dependencies:** attributes: `icd_c54_1`; families: ICD coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ca_lung`

- **Primary purpose:** This is a algorithm to identify lung carcinoma.
- **Key inputs / dependencies:** attributes: `icd_c34%`, `icpc_r84%`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ca_mets`

- **Primary purpose:** This is a algorithm to identify metastatic carcinoma.
- **Key inputs / dependencies:** attributes: `icd_c79_5`, `icd_c79_3`, `icd_c79_7`, `icd_c78_7`, `icd_c78_0`; families: ICD coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ca_misc`

- **Primary purpose:** identify misc carcinoma.
- **Key inputs / dependencies:** attributes: `icd_c%`; families: ICD coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ca_ovarian`

- **Primary purpose:** identify ovarian carcinoma.
- **Key inputs / dependencies:** attributes: `icd_c56%`, `icpc_x77006`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ca_prostate`

- **Primary purpose:** This is a algorithm to identify prostate carcinoma.
- **Key inputs / dependencies:** attributes: `icd_c61%`, `icpc_y77%`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ca_rcc`

- **Primary purpose:** This is a algorithm to identify renal cell carcinoma.
- **Key inputs / dependencies:** attributes: `icd_c64%`, `icpc_u75003`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ca_skin_melanoma`

- **Primary purpose:** identify melanoma.
- **Key inputs / dependencies:** attributes: `icd_c43%`, `icpc_s77003`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ca_solid`

- **Primary purpose:** identify solid organ carcinoma.
- **Key inputs / dependencies:** binds: `rout_ca_mets.ca_mets`, `rout_ca_breast.code_fd`, `rout_ca_prostate.code_fd`, `rout_ca_rcc.code_fd`, `rout_ca_crc.code_fd`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ca_thyroid`

- **Primary purpose:** This is a algorithm to identify thyroid carcinoma.
- **Key inputs / dependencies:** attributes: `icd_c37%`, `icpc_t71%`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cardiac_cad_card`

- **Primary purpose:** View model for coronary artery disease info card.
- **Key inputs / dependencies:** binds: `rout_dmg.dob`, `rout_dmg.gender`, `rout_cd_cardiac_cad.cabg`, `rout_cd_cardiac_cad.cabg_flag`, `rout_cd_cardiac_cad.nstemi_fd_icd`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_cardiac_af`

- **Primary purpose:** This is a assess chadvas score in AF.
- **Key inputs / dependencies:** binds: `rout_cd_cardiac_vhd.cd_cardiac_vhd`, `rout_cd_cardiac_cad.cad`, `rout_cd_cardiac_chf.chf`, `rout_cd_cardiac_cad.pvd`, `rout_cd_cardiac_cad.cva`; attributes: `dmg_dob`, `dmg_gender`, `icd_i48%`, `icpc_k78%`; families: demographics, ICD coding, ICPC coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_cardiac_cad`

- **Primary purpose:** assess cardiac disease (coronary artery disease).
- **Key inputs / dependencies:** binds: `rout_cd_cardiac_ix.echo_ld`, `rout_cd_cardiac_ix.cardang_ld`; attributes: `icd_z95_1`, `icpc_k54007`, `icd_i21_a1`, `icd_i21_4`, `icd_i22_2`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_cardiac_chf`

- **Primary purpose:** This is a assess CHF.
- **Key inputs / dependencies:** binds: `rout_cd_cardiac_ix.echo_ld`; attributes: `icd_i50%`, `icpc_k77%`, `icd_i42_0`, `icd_i42_1`, `icd_i42_2`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_cardiac_device`

- **Primary purpose:** assess cardiac device.
- **Key inputs / dependencies:** attributes: `icpc_k54001`, `caresys_38253%`, `caresys_3839002`; families: ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_cardiac_enc`

- **Primary purpose:** assess cardiac encounters.
- **Key inputs / dependencies:** attributes: `enc_op_car_%`; families: encounters
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_cardiac_ix`

- **Primary purpose:** assess cardiac investigations.
- **Key inputs / dependencies:** attributes: `enc_ris_echo%`, `ntc_rep_tte`, `enc_ris_cardang%`; families: encounters
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_cardiac_rhd`

- **Primary purpose:** assess rheumatic heart disease.
- **Key inputs / dependencies:** binds: `rout_cd_cardiac_ix.echo_ld`; attributes: `icd_i05%`, `icd_i06%`, `icd_i07%`, `icd_i08%`, `icd_i09%`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_cardiac_rx`

- **Primary purpose:** assess cardiac medication.
- **Key inputs / dependencies:** attributes: `rxnc_b01ac`, `rxnc_b01aa`, `rxnc_b01af`, `rxnc_b01ae`, `rxnc_b01ab`; families: RxNorm/ATC medication codes; citations: `cvd_tg_2019`, `cvd_heart_foundation_2012`
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Consider adding tighter documentation, shared helper bindings, and small compile-based regression checks around the core outputs.

## `cd_cardiac_vhd`

- **Primary purpose:** assess cardiac disease.
- **Key inputs / dependencies:** binds: `rout_cd_cardiac_rx.rxn_anticoag`, `rout_cd_cardiac_ix.echo_ld`; attributes: `icd_i05%`, `icd_i06%`, `icd_i07%`, `icd_i08%`, `icd_i09%`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_cardiac_vte`

- **Primary purpose:** assess VTE.
- **Key inputs / dependencies:** attributes: `icd_i26%`, `icpc_k93002`, `icd_i82_2`, `icd_i82_3`, `icd_i82_9`; families: ICD coding, ICPC coding, RxNorm/ATC medication codes
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_careplan`

- **Primary purpose:** determine existing careplans.
- **Key inputs / dependencies:** binds: `rout_dmg_source.phc_1`; attributes: `careplan_h9_v1`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_cirrhosis`

- **Primary purpose:** identify cirrhosis e-phenotype.
- **Key inputs / dependencies:** attributes: `icpc_d97011`, `icd_k74_3`, `icpc_d97005`, `icd_k74_6`, `lab_bld_albumin`; families: ICPC coding, ICD coding, blood labs
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_cns`

- **Primary purpose:** This is a algorithm to identify CNS disorders.
- **Key inputs / dependencies:** attributes: `icd_f3%`, `icpc_p76%`, `rxnc_n06%`, `icd_f01%`, `icd_f02%`; families: ICD coding, ICPC coding, RxNorm/ATC medication codes
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_cns_ch`

- **Primary purpose:** identify cerebral haemorrhage.
- **Key inputs / dependencies:** attributes: `icpc_n80001`, `icpc_n80004`, `icd_i62_0`, `icpc_n80008`, `icpc_n80015`; families: ICPC coding, ICD coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_cva`

- **Primary purpose:** assess for cva.
- **Key inputs / dependencies:** attributes: `icd_i63%`, `icd_i65%`, `icd_i66%`, `icd_i67%`, `icd_i60%`; families: ICD coding
- **Logical errors / review targets:** Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_dm_comp`

- **Primary purpose:** assess diabetes.
- **Key inputs / dependencies:** binds: `rout_cd_dm_dx.cd_dm_dx`; attributes: `icd_e10_31`, `icd_e11_31`, `icd_e13_31`, `icd_e10_32`, `icd_e11_32`; families: ICD coding; citations: `dm_dmcare_2014`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library.

## `cd_dm_dx`

- **Primary purpose:** assess diabetic diagnosis.
- **Key inputs / dependencies:** attributes: `icd_e10%`, `icpc_t89002`, `icd_e08%`, `icd_e11%`, `icd_e14%`; families: ICD coding, ICPC coding; citations: `dm_bmc_ehr_2019`, `dm_mja_2012`, `dm_nhmrc_2009`, `dm_rxn`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Likely issue: the rule contains development markers, placeholders, or commented-out unfinished logic. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Replace placeholder constants and commented stubs with implemented logic, or clearly retire inactive branches. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Consider adding tighter documentation, shared helper bindings, and small compile-based regression checks around the core outputs.

## `cd_dm_glyc_cntrl`

- **Primary purpose:** assess diabetic glycaemic control.
- **Key inputs / dependencies:** binds: `rout_cd_dm_dx.cd_dm_dx`; attributes: `lab_bld_hba1c_ngsp`; families: blood labs; citations: `dm_pcd_2019`, `dm_ada_2018`, `dm_bmj_2011`, `dm_nejm_2008`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `cd_dm_mx`

- **Primary purpose:** assess diabetic management.
- **Key inputs / dependencies:** binds: `rout_cd_dm_dx.cd_dm_dx`; attributes: `careplan_h9_v1`, `mbs_10962`, `mbs_10951`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_dm_rx_rcm`

- **Primary purpose:** recommend diabetic pharmacotherapy.
- **Key inputs / dependencies:** binds: `rout_cd_dm_dx.cd_dm_dx`, `rout_cd_obesity.bmi`; attributes: `rxnc_a10ae`, `rxnc_a10ac`, `rxnc_a10ad`, `rxnc_a10ab`, `rxnc_a10ba`; families: RxNorm/ATC medication codes
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_dyslip`

- **Primary purpose:** assess for cd_dyslipidaemia.
- **Key inputs / dependencies:** binds: `rout_cvra.cvd_prev`, `rout_dmg.dob`, `rout_dmg.gender`, `rout_cd_cardiac_cad.cd_cardiac_cad`; attributes: `icd_e78%`, `icpc_t93%`, `lab_bld_cholesterol_total`, `lab_bld_cholesterol_hdl`, `lab_bld_cholesterol_tg`; families: ICD coding, ICPC coding, blood labs, RxNorm/ATC medication codes
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_endo_hypothyroid`

- **Primary purpose:** This is a algorithm to identify hypothyroidism.
- **Key inputs / dependencies:** attributes: `icd_e03_1`, `icpc_t86004`, `icd_e03_2`, `icpc_t86008`, `icd_e89%`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_haem`

- **Primary purpose:** This is a algorithm to identify haematological disease.
- **Key inputs / dependencies:** attributes: `lab_bld_hb`, `lab_bld_rbc_mcv`, `lab_bld_wcc_neutrophils`, `lab_bld_platelets`, `lab_bld_ferritin`; families: blood labs
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_hep_b_sero`

- **Primary purpose:** detect Chronic hepatitis B from serology.
- **Key inputs / dependencies:** binds: `rout_dmg.gender`; attributes: `lab_bld_hbs_ab_level`, `lab_bld_hbs_ag`, `lab_bld_hbc_ab`, `lab_bld_hbe_ab_level`, `lab_bld_hbe_ag_level`; families: blood labs
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_hepb`

- **Primary purpose:** detect Chronic hepatitis B from coding - deprecated.
- **Key inputs / dependencies:** attributes: `icpc_d72j97`, `icpc_d72j96`, `icpc_d72j99`, `icpc_d72j93`, `icpc_d72j92`; families: ICPC coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Review target: the ruleblock is marked inactive (`is_active:0`), so it may be incomplete, deprecated, or not ready for production use.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Confirm whether the rule should remain inactive; if not, complete validation and activate it intentionally.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_hepb_coded`

- **Primary purpose:** detect Chronic hepatitis B from coding.
- **Key inputs / dependencies:** attributes: `icpc_d72j92`, `icd_b17_0`, `rxnc_j05af`; families: ICPC coding, ICD coding, RxNorm/ATC medication codes
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_hepb_master`

- **Primary purpose:** detect Chronic hepatitis B.
- **Key inputs / dependencies:** binds: `rout_cd_hep_b_sero.hbv_status`, `rout_cd_hep_b_sero.hbv_phase`, `rout_cd_hep_b_sero.vl_val`, `rout_cd_hep_b_sero.vl_dt`, `rout_cd_hep_b_sero.alt_dt`; attributes: `enc_ris_usabkid`; families: encounters
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_htn`

- **Primary purpose:** assess hypertension.
- **Key inputs / dependencies:** attributes: `obs_bp_systolic`, `icd_i10%`, `icd_i15%`, `icpc_k85%`, `icpc_k86%`; families: observations, ICD coding, ICPC coding, blood labs; citations: `htn_nhf_2016`, `htn_aha_2018`, `htn_mja_2016`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `cd_htn_bp_control`

- **Primary purpose:** assess blood pressure control.
- **Key inputs / dependencies:** binds: `rout_cvra.age`, `rout_cvra.cvra_cat`, `rout_cd_htn.cd_htn`, `rout_rrt.rrt`; attributes: `obs_bp_systolic`, `obs_bp_diastolic`; families: observations; citations: `htn_plos_2018`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library.

## `cd_htn_card`

- **Primary purpose:** View model for hypertension info card.
- **Key inputs / dependencies:** binds: `rout_cd_htn.htn`, `rout_cd_htn_bp_control.sbp_mu_1`, `rout_cd_htn_bp_control.dbp_mu_1`, `rout_cd_htn_bp_control.sbp_dt`, `rout_cd_htn_bp_control.sbp_min`
- **Logical errors / review targets:** Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_htn_rcm`

- **Primary purpose:** assess hypertension pharmacology recommendations.
- **Key inputs / dependencies:** binds: `rout_ckd.ckd`, `rout_cd_htn.cd_htn`, `rout_cd_htn.bp_control`, `rout_cd_cardiac_cad.cad`; attributes: `rxnc_c09aa`, `rxnc_c09ca`, `rxnc_c07%`, `rxnc_c08%`, `rxnc_c02%`; families: RxNorm/ATC medication codes; citations: `htn_tga_2019`, `htn_jnc_2014`, `htn_rcm_compmethods_2000`, `htn_rcm_amia_2017`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Review target: the ruleblock is marked inactive (`is_active:0`), so it may be incomplete, deprecated, or not ready for production use. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Confirm whether the rule should remain inactive; if not, complete validation and activate it intentionally. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library.

## `cd_imm_vasculitis`

- **Primary purpose:** This is a algorithm to identify vasculitic phenotypes.
- **Key inputs / dependencies:** attributes: `icd_m31_3`, `icd_m31_5`, `icd_m31_6`, `icd_m31_7`, `icd_m31_4`; families: ICD coding, RxNorm/ATC medication codes
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_multi_m1`

- **Primary purpose:** define multi disease m1 level viewmodel.
- **Key inputs / dependencies:** binds: `rout_ckd.ckd`, `rout_rrt.rrt`, `rout_cd_dm_dx.dm_type`, `rout_cd_dm_dx.dm_fd_year`, `rout_cd_dm_dx.dm1_mm`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Review target: the ruleblock is marked inactive (`is_active:0`), so it may be incomplete, deprecated, or not ready for production use.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Confirm whether the rule should remain inactive; if not, complete validation and activate it intentionally.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_nutr_low`

- **Primary purpose:** assess loss of weight.
- **Key inputs / dependencies:** attributes: `obs_height`, `obs_weight`; families: observations
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_obesity`

- **Primary purpose:** assess obesity.
- **Key inputs / dependencies:** attributes: `obs_height`, `obs_weight`, `icd_e66%`, `icpc_t82%`; families: observations, ICD coding, ICPC coding; citations: `cd_obesity_ref2`, `cd_obesity_ref1`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed.
- **Potential improvements:** Consider adding tighter documentation, shared helper bindings, and small compile-based regression checks around the core outputs.

## `cd_pulm`

- **Primary purpose:** This is a algorithm to identify pulmonary disease.
- **Key inputs / dependencies:** attributes: `icpc_r95%`, `icd_j44%`, `rxnc_r03%`; families: ICPC coding, ICD coding, RxNorm/ATC medication codes
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_pulm_bt`

- **Primary purpose:** identify bronchiectasis.
- **Key inputs / dependencies:** attributes: `icd_j47%`; families: ICD coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_pulm_copd`

- **Primary purpose:** identify pulmonary disease.
- **Key inputs / dependencies:** attributes: `icpc_r95%`, `icd_j44%`, `rxnc_r03%`; families: ICPC coding, ICD coding, RxNorm/ATC medication codes
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_rheum_aps`

- **Primary purpose:** identify Antiphosphlipid syndrome.
- **Key inputs / dependencies:** binds: `rout_cd_cardiac_rx.rxn_anticoag`; attributes: `icd_d68_61%`, `icpc_b83021`, `enc_op_med_rhe`; families: ICD coding, ICPC coding, encounters
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_rheum_gout`

- **Primary purpose:** identify Gout.
- **Key inputs / dependencies:** attributes: `icd_m10%`, `icpc_t92001`, `rxnc_m04aa`, `enc_op_med_rhe`; families: ICD coding, ICPC coding, RxNorm/ATC medication codes, encounters
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_rheum_ra`

- **Primary purpose:** identify Rheumatoid Arthritis.
- **Key inputs / dependencies:** attributes: `icd_m05%`, `icpc_l88004`, `rxnc_l04ax`, `rxnc_p01ba`, `rxnc_a07ec`; families: ICD coding, ICPC coding, RxNorm/ATC medication codes, encounters
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cd_rheum_sle`

- **Primary purpose:** identify SLE e-phenotype.
- **Key inputs / dependencies:** attributes: `icd_m32%`, `icpc_l99056`, `icpc_l99065`, `rxnc_l04ax`, `rxnc_p01ba`; families: ICD coding, ICPC coding, RxNorm/ATC medication codes, blood labs
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd`

- **Primary purpose:** stage CKD.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`, `rout_rrt.hd_131_n`, `rout_ckd_egfr_metrics.egfr_l_val`, `rout_ckd_egfr_metrics.egfr_l_dt`, `rout_ckd_egfr_metrics.egfr_outdated`; citations: `ckd_ref1`, `ckd_ref2`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library.

## `ckd_access`

- **Primary purpose:** stage CKD.
- **Key inputs / dependencies:** attributes: `caresys_3450901`, `caresys_3451200`, `caresys_3451800`, `icpc_k99049`, `icd_z49_0`; families: ICPC coding, ICD coding
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain.
- **Potential improvements:** Consider binding more shared CKD helper outputs if equivalent staging or metrics already exist elsewhere in the pack. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd_anaemia`

- **Primary purpose:** determine CKD complications.
- **Key inputs / dependencies:** binds: `rout_ckd.ckd`, `rout_rrt.rrt`; attributes: `lab_bld_hb`, `lab_bld_platelets`, `lab_bld_wcc_neutrophils`, `lab_bld_wcc_eosinophils`, `lab_bld_rbc_mcv`; families: blood labs, RxNorm/ATC medication codes; citations: `ckd_complications_ref1`, `ckd_complications_ref2`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `ckd_c_gn`

- **Primary purpose:** determine CKD by cause.
- **Key inputs / dependencies:** attributes: `icd_n00%`, `icpc_u88007`, `icd_n01%`, `icd_n02%`, `icd_n03%`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Consider binding more shared CKD helper outputs if equivalent staging or metrics already exist elsewhere in the pack. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd_c_rnm`

- **Primary purpose:** determine coded conditions leading to reduced nephron mass.
- **Key inputs / dependencies:** attributes: `icd_q60%`, `icd_n26%`, `icd_n27%`, `icd_q61%`, `icpc_u85008`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Consider binding more shared CKD helper outputs if equivalent staging or metrics already exist elsewhere in the pack. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd_c_tid`

- **Primary purpose:** determine coded tubulointerstitial disease.
- **Key inputs / dependencies:** attributes: `icd_n11%`, `icd_n12%`, `icd_n13%`, `icd_n14%`, `icd_n15%`; families: ICD coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Consider binding more shared CKD helper outputs if equivalent staging or metrics already exist elsewhere in the pack. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd_card`

- **Primary purpose:** View model for ckd info card.
- **Key inputs / dependencies:** binds: `rout_ckd.ckd`, `rout_rrt.rrt`, `rout_ckd.cga_g`, `rout_ckd.cga_a`, `rout_ckd_egfr_metrics.egfr_l_val`
- **Logical errors / review targets:** Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd_careplan`

- **Primary purpose:** assess careplan.
- **Key inputs / dependencies:** binds: `rout_dmg_source.phc_1`; attributes: `careplan_h9_v1`, `icpc_u59011`; families: ICPC coding
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd_cause`

- **Primary purpose:** determine causality for CKD.
- **Key inputs / dependencies:** binds: `rout_cd_dm_dx.dm`, `rout_cd_htn.htn`, `rout_ckd.ckd`, `rout_rrt.rrt`, `rout_cd_rheum_sle.cd_rheum_sle`; attributes: `icd_m32_14`, `icd_n0%`, `icpc_u88%`, `icd_n17%`, `icd_n20%`; families: ICD coding, ICPC coding; citations: `ckd_cause_ref1`, `ckd_cause_ref2`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library.

## `ckd_coded_dx`

- **Primary purpose:** Evaluate existing coded ckd diagnoses.
- **Key inputs / dependencies:** attributes: `icpc_u88j91`, `icpc_u88j92`, `icpc_u88j93`, `icpc_u88j94`, `icpc_u88j95`; families: ICPC coding
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain.
- **Potential improvements:** Consider binding more shared CKD helper outputs if equivalent staging or metrics already exist elsewhere in the pack. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd_complications`

- **Primary purpose:** determine CKD complications.
- **Key inputs / dependencies:** binds: `rout_ckd.ckd`; attributes: `lab_bld_hb`, `lab_bld_pth`, `lab_bld_wcc_neutrophils`, `lab_bld_wcc_eosinophils`, `lab_bld_rbc_mcv`; families: blood labs, RxNorm/ATC medication codes; citations: `ckd_complications_ref1`, `ckd_complications_ref2`
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `ckd_dense`

- **Primary purpose:** Optimized Rule block for cube generation in CKD.
- **Key inputs / dependencies:** attributes: `dmg_dob`, `dmg_dod`, `dmg_gender`, `dmg_location`, `dmg_source`; families: demographics, ICD coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination. Review target: the ruleblock is marked inactive (`is_active:0`), so it may be incomplete, deprecated, or not ready for production use.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed. Confirm whether the rule should remain inactive; if not, complete validation and activate it intentionally.
- **Potential improvements:** Consider binding more shared CKD helper outputs if equivalent staging or metrics already exist elsewhere in the pack. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd_diagnostics`

- **Primary purpose:** determine diagnostics.
- **Key inputs / dependencies:** binds: `rout_ckd.ckd`; attributes: `lab_ua_acr`, `lab_ua_rbc`, `lab_ua_poc_rbc`, `lab_ua_leucocytes`, `lab_ua_poc_leucocytes`; families: urine labs, blood labs
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd_egfr_metrics`

- **Primary purpose:** Summarize eGFR recency, extrema, and trend metrics for CKD logic.
- **Key inputs / dependencies:** attributes: `lab_bld_egfr_c`; families: blood labs; citations: `ckd_ref1`, `ckd_ref2`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Consider binding more shared CKD helper outputs if equivalent staging or metrics already exist elsewhere in the pack. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `ckd_journey`

- **Primary purpose:** determine journey of CKD.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`, `rout_ckd.ckd`; attributes: `enc_op_ren_%`, `enc_op_rdu_%`, `enc_op_renal_edu`, `caresys_3450901`, `careplan_h9_v1`; families: encounters
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd_labs`

- **Primary purpose:** gather lab tests.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`, `rout_ckd.ckd`; attributes: `lab_bld_egfr_c`, `lab_bld_creatinine`, `lab_ua_acr`, `lab_bld_sodium`, `lab_bld_potassium`; families: blood labs, urine labs
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd_prog_vm`

- **Primary purpose:** Assemble CKD progress view model.
- **Key inputs / dependencies:** binds: `rout_dmg.age`, `rout_dmg.gender`, `rout_dmg_source.tkc_provider`, `rout_ckd.ckd`, `rout_rrt.rrt`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd_shpt`

- **Primary purpose:** assess for secondary hyperparathyroidism.
- **Key inputs / dependencies:** binds: `rout_ckd.ckd_stage_val`, `rout_rrt.rrt`; attributes: `lab_bld_calcium_corrected`, `lab_bld_magnesium`, `lab_bld_phosphate`, `lab_bld_pth`, `rxnc_h05bx`; families: blood labs, RxNorm/ATC medication codes
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd_ttem`

- **Primary purpose:** CKD time to event modelling.
- **Key inputs / dependencies:** attributes: `icpc_u59001`, `icpc_u59008`, `caresys_1310000`, `icd_z49_1`, `mbs_13105`; families: ICPC coding, ICD coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Consider binding more shared CKD helper outputs if equivalent staging or metrics already exist elsewhere in the pack. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ckd_uacr_metrics`

- **Primary purpose:** Summarize urine ACR recency and albuminuria severity metrics.
- **Key inputs / dependencies:** attributes: `lab_ua_acr`, `lab_ua_poc_leucocytes`, `lab_ua_leucocytes`; families: urine labs; citations: `ckd_ref1`, `ckd_ref2`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain.
- **Potential improvements:** Consider binding more shared CKD helper outputs if equivalent staging or metrics already exist elsewhere in the pack. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `cm_vm`

- **Primary purpose:** comorbidity view model.
- **Key inputs / dependencies:** binds: `rout_vacc_covid.vax_pf_dt`, `rout_vacc_covid.vax_az_dt`, `rout_vacc_covid.vax_md_dt`, `rout_vacc_covid.vax_dt`, `rout_vacc_covid.vax_val`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cmidx_charlson`

- **Primary purpose:** Calculate a Charlson-style comorbidity index from coded history.
- **Key inputs / dependencies:** attributes: `icd_i21%`, `icd_i09_9`, `icd_i70%`, `icd_g45%`, `icd_f00%`; families: ICD coding
- **Logical errors / review targets:** Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Preserve model provenance clearly: keep coefficients, cohorts, and recalibration assumptions documented next to the coded equations. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `core_info_entropy`

- **Primary purpose:** assess core information entropy.
- **Key inputs / dependencies:** attributes: `dmg_dod`, `icpc_%`, `icd_%`, `lab_%`, `obs_%`; families: demographics, ICPC coding, ICD coding, observations
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Review target: the ruleblock is marked inactive (`is_active:0`), so it may be incomplete, deprecated, or not ready for production use. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Confirm whether the rule should remain inactive; if not, complete validation and activate it intentionally. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `cvra`

- **Primary purpose:** Assess overall cardiovascular risk and related override states.
- **Key inputs / dependencies:** binds: `rout_ckd.ckd`, `rout_ckd.esrd_risk`, `rout_cd_dm_dx.dm`, `rout_cd_careplan.cp_hicvr`, `rout_dmg_source.dmg_source`; attributes: `asm_cvra`, `dmg_dob`, `dmg_gender`, `icd_z95_1%`, `icpc_k54007`; families: assessment attributes, demographics, ICD coding, ICPC coding; citations: `cvra_hlc_2019`, `cvra_circ_2018`, `cvra_nsf_2019`, `cvra_ahj_1991`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Preserve model provenance clearly: keep coefficients, cohorts, and recalibration assumptions documented next to the coded equations.

## `cvra_predict1_aus`

- **Primary purpose:** Estimate Australian Predict1-style cardiovascular risk and map it to a risk category.
- **Key inputs / dependencies:** binds: `rout_ckd.ckd`, `rout_ckd.esrd_risk`, `rout_cd_dm_dx.dm`, `rout_cd_careplan.cp_hicvr`, `rout_dmg_source.dmg_source`; attributes: `asm_cvra`, `lab_bld_egfr_c`, `lab_ua_acr`, `lab_bld_cholesterol_hdl`, `lab_bld_cholesterol_total`; families: assessment attributes, blood labs, urine labs, observations; citations: `cvra_hlc_2019`, `cvra_circ_2018`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination. Likely issue: the rule contains development markers, placeholders, or commented-out unfinished logic.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed. Replace placeholder constants and commented stubs with implemented logic, or clearly retire inactive branches.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Preserve model provenance clearly: keep coefficients, cohorts, and recalibration assumptions documented next to the coded equations. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `dm_card`

- **Primary purpose:** View model for diabetes info card.
- **Key inputs / dependencies:** binds: `rout_cd_dm_dx.dm`, `rout_cd_dm_dx.dm_vintage_yr`, `rout_cd_dm_dx.dm_rxn_su`, `rout_cd_dm_dx.dm_rxn_ins`, `rout_cd_dm_dx.dm_rxn_bg`
- **Logical errors / review targets:** Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `dmg`

- **Primary purpose:** assess demographics.
- **Key inputs / dependencies:** attributes: `dmg_dob`, `dmg_dod`, `dmg_gender`, `dmg_indigenous_status`; families: demographics
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `dmg_eid_alt`

- **Primary purpose:** assess alternative eid.
- **Key inputs / dependencies:** attributes: `dmg_eid_alt`; families: demographics
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `dmg_hrn`

- **Primary purpose:** assess HRN.
- **Key inputs / dependencies:** attributes: `dmg_hrn`; families: demographics
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `dmg_loc`

- **Primary purpose:** assess demographics.
- **Key inputs / dependencies:** attributes: `mbs_%`, `mbs_715`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `dmg_loc2`

- **Primary purpose:** assess possible location of origin for all TKC clients.
- **Key inputs / dependencies:** attributes: `mbs_715`, `mbs_%`, `enc_%`, `icd_%`; families: encounters, ICD coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `dmg_loc_origin`

- **Primary purpose:** assess demographics origin.
- **Key inputs / dependencies:** attributes: `mbs_715`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `dmg_residency`

- **Primary purpose:** assess residential status.
- **Key inputs / dependencies:** attributes: `mbs_731`
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `dmg_source`

- **Primary purpose:** assess demographic source.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`, `rout_dmg_loc.loc_def`, `rout_dmg_loc.loc_def_alt`, `rout_dmg_loc.loc_null`, `rout_dmg_loc.loc_mode_n`; attributes: `mbs_%`, `icd_%`, `lab_%`; families: ICD coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `dmg_tkcuser_interact`

- **Primary purpose:** assess TKC user interaction.
- **Key inputs / dependencies:** attributes: `tkc_corresp`, `sys_record_partial`
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `dmg_vm`

- **Primary purpose:** assess demographic view model.
- **Key inputs / dependencies:** binds: `rout_dmg_loc.loc_def`, `rout_dmg_loc.loc_mode_n`, `rout_dmg_loc.loc_n`, `rout_dmg_loc.mode_pct`, `rout_dmg_hrn.hrn_last`
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `egfr_graph2`

- **Primary purpose:** plot egfr graph 2.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`; attributes: `lab_bld_egfr_c`; families: blood labs
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `egfr_metrics`

- **Primary purpose:** derive egfr metrics.
- **Key inputs / dependencies:** attributes: `lab_bld_egfr_c`; families: blood labs
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination. Review target: the ruleblock is marked inactive (`is_active:0`), so it may be incomplete, deprecated, or not ready for production use.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed. Confirm whether the rule should remain inactive; if not, complete validation and activate it intentionally.
- **Potential improvements:** Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `engmnt_renal`

- **Primary purpose:** assess encounters with renal.
- **Key inputs / dependencies:** attributes: `ref_nephrologist`, `icpc_u67004`, `enc_op_ren_%`; families: ICPC coding, encounters
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `frm_func_assm`

- **Primary purpose:** mobility functional state.
- **Key inputs / dependencies:** binds: `rout_at_risk.is_active`, `rout_ckd.ckd`, `rout_rrt.rrt`, `rout_cd_dm_dx.dm`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `global`

- **Primary purpose:** Global TKC interface.
- **Key inputs / dependencies:** binds: `rout_at_risk.tkc_cat`, `rout_dmg_loc.loc_mode_24`, `rout_dmg_loc.loc_last_val`; attributes: `dmg_opted_out`; families: demographics
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `hb_graph`

- **Primary purpose:** Prepare haemoglobin trend outputs for graphing or display.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`; attributes: `lab_bld_hb`; families: blood labs
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `hba1c_graph`

- **Primary purpose:** Prepare HbA1c trend outputs for graphing or display.
- **Key inputs / dependencies:** binds: `rout_cd_dm_dx.cd_dm_dx`; attributes: `lab_bld_hba1c_ngsp`; families: blood labs
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `id_cap`

- **Primary purpose:** This is a algorithm to identify respiratory infections.
- **Key inputs / dependencies:** attributes: `icd_j09%`, `icd_j13%`, `icd_j14%`, `icd_j18%`, `icpc_a78054`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `id_covid19`

- **Primary purpose:** This is a algorithm to identify covid19.
- **Key inputs / dependencies:** attributes: `icpc_r83015`; families: ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `id_hcv`

- **Primary purpose:** identify Chronic Hepatitis C.
- **Key inputs / dependencies:** attributes: `icpc_d72008`, `icd_b18_2%`; families: ICPC coding, ICD coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `id_htlv`

- **Primary purpose:** identify HTLV1-2.
- **Key inputs / dependencies:** attributes: `lab_bld_htlv`, `icd_b97_33`; families: blood labs, ICD coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `id_sti`

- **Primary purpose:** This is a algorithm to identify soft tissue infection.
- **Key inputs / dependencies:** attributes: `icd_l0%`, `icpc_s10%`, `icpc_s76%`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `id_tb`

- **Primary purpose:** This is a algorithm to identify Tuberculosis.
- **Key inputs / dependencies:** attributes: `icpc_a700%`, `icpc_a70j99`; families: ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `id_uti`

- **Primary purpose:** This is a algorithm to identify uti.
- **Key inputs / dependencies:** attributes: `icd_n39%`, `icpc_u71015`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ipa_icu`

- **Primary purpose:** Inpatient activity for ICU admissions.
- **Key inputs / dependencies:** attributes: `adm_icu_vent_los`, `caresys_1387900`, `adm_icu`, `caresys_1310004`
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ipa_sep`

- **Primary purpose:** Inpatient activity with exclusions.
- **Key inputs / dependencies:** attributes: `icd_%`; families: ICD coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `kfre`

- **Primary purpose:** Estimate kidney failure risk using Kidney Failure Risk Equation style variables.
- **Key inputs / dependencies:** binds: `rout_ckd.ckd`, `rout_dmg.dob`, `rout_dmg.gender`; attributes: `lab_bld_egfr_c`, `lab_ua_acr`; families: blood labs, urine labs; citations: `kfre_ref1`, `kfre_ref2`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Preserve model provenance clearly: keep coefficients, cohorts, and recalibration assumptions documented next to the coded equations. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `kpi_uncategorised`

- **Primary purpose:** these are the rules for KPIs which do not fit into other categories.
- **Key inputs / dependencies:** attributes: `mbs_715`, `mbs_721`, `mbs_723`, `mbs_732`, `icd_%`; families: ICD coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Review target: the ruleblock is marked inactive (`is_active:0`), so it may be incomplete, deprecated, or not ready for production use.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Confirm whether the rule should remain inactive; if not, complete validation and activate it intentionally.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `mbs715`

- **Primary purpose:** Annual health check mbs 715.
- **Key inputs / dependencies:** binds: `rout_dmg.dob`, `rout_dmg.age`, `rout_dmg.gender`, `rout_rrt.rrt`, `rout_ckd.ckd`; attributes: `mbs_715`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Review target: the ruleblock is marked inactive (`is_active:0`), so it may be incomplete, deprecated, or not ready for production use. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Confirm whether the rule should remain inactive; if not, complete validation and activate it intentionally. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `mbs_billing_history`

- **Primary purpose:** MBS billing last dates.
- **Key inputs / dependencies:** attributes: `mbs_715`, `mbs_721`, `mbs_732`, `mbs_723`, `mbs_705`
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `obs_vm`

- **Primary purpose:** Observation view model.
- **Key inputs / dependencies:** binds: `rout_cd_obesity.ht_dt`, `rout_cd_obesity.ht_val`, `rout_cd_obesity.ht_err`, `rout_cd_obesity.wt_dt`, `rout_cd_obesity.wt_val`
- **Logical errors / review targets:** Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `opa_sep`

- **Primary purpose:** Outpatient activity with exclusions.
- **Key inputs / dependencies:** attributes: `enc_op_%`; families: encounters
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ortho_amputation`

- **Primary purpose:** Identify amputation phenotypes.
- **Key inputs / dependencies:** attributes: `enc_op_po_kpt`, `icd_y83_5`, `icpc_a87010`, `caresys_443%`, `caresys_4433800`; families: encounters, ICD coding, ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `ortho_fractures`

- **Primary purpose:** Identify fracture phenotypes.
- **Key inputs / dependencies:** attributes: `icd_s32_1`; families: ICD coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `pcd`

- **Primary purpose:** assess PCD Traffic light report.
- **Key inputs / dependencies:** binds: `rout_ckd.ckd`, `rout_cd_dm_dx.dm`, `rout_cvra.cvra`; attributes: `dmg_dob`, `dmg_gender`, `mbs_721`, `asm_cvra`, `lab_bld_cholesterol_tot`; families: demographics, assessment attributes, blood labs, observations
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination. Review target: the ruleblock is marked inactive (`is_active:0`), so it may be incomplete, deprecated, or not ready for production use.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed. Confirm whether the rule should remain inactive; if not, complete validation and activate it intentionally.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `periop_nsqip`

- **Primary purpose:** Estimate perioperative risk using an NSQIP-style feature set.
- **Key inputs / dependencies:** binds: `rout_cd_cardiac_cad.cd_cardiac_cad`, `rout_cd_cardiac_vhd.cd_cardiac_vhd`, `rout_cd_htn.cd_htn`, `rout_cd_htn.htn_rxn`, `rout_cd_pulm.cd_pulm`; attributes: `dmg_dob`, `icd_c%`, `icpc_a79%`, `rxnc_h02ab`, `icd_d68%`; families: demographics, ICD coding, ICPC coding, RxNorm/ATC medication codes
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Review target: the ruleblock is marked inactive (`is_active:0`), so it may be incomplete, deprecated, or not ready for production use.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Confirm whether the rule should remain inactive; if not, complete validation and activate it intentionally.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Preserve model provenance clearly: keep coefficients, cohorts, and recalibration assumptions documented next to the coded equations. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `phos_graph`

- **Primary purpose:** Prepare phosphate trend outputs for graphing or display.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`; attributes: `lab_bld_phosphate`; families: blood labs
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `pregnancy`

- **Primary purpose:** Identify pregnancy-related state from coded, lab, or care signals.
- **Key inputs / dependencies:** attributes: `enc_ris_uspreg%`, `icpc_w05%`, `icpc_w17%`, `icpc_w18%`, `icpc_w29%`; families: encounters, ICPC coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt`

- **Primary purpose:** determine RRT status.
- **Key inputs / dependencies:** attributes: `icd_z49_1`, `caresys_1310000`, `mbs_13105`, `icpc_u59001`, `icpc_u59008`; families: ICD coding, ICPC coding; citations: `rrt_hd_icd`, `rrt_pd_icd`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Likely issue: the rule contains development markers, placeholders, or commented-out unfinished logic.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Replace placeholder constants and commented stubs with implemented logic, or clearly retire inactive branches.
- **Potential improvements:** Consider adding tighter documentation, shared helper bindings, and small compile-based regression checks around the core outputs.

## `rrt_1_card`

- **Primary purpose:** View model for haemodialysis info card.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`, `rout_rrt_hd_adequacy.spktv`, `rout_rrt_1_metrics.tspan_y`, `rout_rrt_1_metrics.hd_oe`, `rout_rrt.hd_dt_min`
- **Logical errors / review targets:** Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_1_metrics`

- **Primary purpose:** determine RRT 1 metrics.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`; attributes: `icd_z49_1`, `mbs_13105`; families: ICD coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_assert`

- **Primary purpose:** assess RRT level assertion criteria.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`, `rout_rrt.tx_dt`, `rout_rrt.pd_dt`, `rout_rrt.homedx_dt`, `rout_rrt.hd_dt`
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_hd_acc_card`

- **Primary purpose:** View model for haemodialysis vascular access info card.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`, `rout_rrt_hd_acc_iv.acc_side_val`, `rout_rrt_hd_acc_iv.acc_type_val`, `rout_rrt_hd_acc_iv.acc_detail`, `rout_rrt_hd_acc_iv.avf_dt`
- **Logical errors / review targets:** Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_hd_acc_iv`

- **Primary purpose:** determine Fistula intervention.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`, `rout_ckd_access.avf_dt`; attributes: `hd_access_side`, `hd_access_type`, `enc_ris_usavfist`, `enc_ris_dshfist`, `enc_ris_dshplas%`; families: encounters
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Review target: broad wildcard code matching is used heavily; confirm that the included code families are specific enough for the intended phenotype.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Re-check wildcard families against the coding spec and narrow them where false positives are likely.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_hd_adequacy`

- **Primary purpose:** determine Haemodialysis adequacy.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`; attributes: `lab_bld_urea_post_hd`, `lab_bld_urea_pre_hd`; families: blood labs
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_hd_loc`

- **Primary purpose:** count RRT HD presentations.
- **Key inputs / dependencies:** attributes: `caresys_1310000`, `caresys_1310004`, `icpc_u59001`, `icpc_u59008`, `icd_z49_1`; families: ICPC coding, ICD coding
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Review target: the ruleblock is marked inactive (`is_active:0`), so it may be incomplete, deprecated, or not ready for production use.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Confirm whether the rule should remain inactive; if not, complete validation and activate it intentionally.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_hd_location`

- **Primary purpose:** determine Haemodialysis location or facility 2023 update.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`; attributes: `dmg_dod`, `caresys_1310000`, `mbs_13105`; families: demographics
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_hd_param`

- **Primary purpose:** determine Haemodialysis parameters.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`; attributes: `psi_hd_param_mode`, `hd_param_hours`, `obs_dry_weight`, `obs_weight`, `psi_hd_param_dx`; families: observations
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_hd_prog_vm`

- **Primary purpose:** Assemble hd progress view model.
- **Key inputs / dependencies:** binds: `rout_dmg.age`, `rout_dmg.gender`, `rout_dmg_source.tkc_provider`, `rout_rrt.rrt`, `rout_engmnt_renal.enc_ld`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_journey`

- **Primary purpose:** determine RRT 1 metrics.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`; attributes: `icd_z49_1`; families: ICD coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_labs_euc`

- **Primary purpose:** gather lab tests.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`; attributes: `lab_bld_sodium`, `lab_bld_potassium`, `lab_bld_bicarbonate`; families: blood labs
- **Logical errors / review targets:** Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_new3_wip`

- **Primary purpose:** assign tx.
- **Key inputs / dependencies:** attributes: `caresys_1310000`, `icd_z49_1`, `mbs_13105`, `enc_op_ren_hpd`, `icpc_u28001`; families: ICD coding, encounters, ICPC coding
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Likely issue: the rule contains development markers, placeholders, or commented-out unfinished logic. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Replace placeholder constants and commented stubs with implemented logic, or clearly retire inactive branches. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_panel_vm`

- **Primary purpose:** generate rrt panel view model.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`, `rout_rrt.hd_dt_min`, `rout_rrt_hd_location.loc_mode_1m_txt`, `rout_rrt_hd_location.hd_131000_pri_loc`, `rout_rrt_hd_location.hd_13105_loc`
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Expose display-oriented outputs consistently with labels and consider parameterizing lookback windows if this supports UI trends. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_pd`

- **Primary purpose:** identify presence of PD catheter.
- **Key inputs / dependencies:** attributes: `caresys_1310900`
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_pd_card`

- **Primary purpose:** View model for PD info card.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`, `rout_rrt.pd_dt`, `rout_rrt.pd_dt_min`; attributes: `pd_regimen_apd_cycles`, `pd_pet_transporter_stat`, `pd_adequacy_ktv_dialysis`, `pd_adequacy_ktv_renal`, `pd_adequacy_ktv_total`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_tx`

- **Primary purpose:** determine Tx metrics.
- **Key inputs / dependencies:** binds: `rout_rrt.tx_dt`; attributes: `lab_bld_creatinine`, `enc_op_ren_rnt`, `rxnc_l04ad`, `lab_bld_tdm_tacrolimus`, `rxnc_l04aa`; families: blood labs, encounters, RxNorm/ATC medication codes
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rrt_tx_card`

- **Primary purpose:** View model for renal transplant info card.
- **Key inputs / dependencies:** binds: `rout_rrt.rrt`, `rout_rrt.tx_dt`, `rout_rrt_tx.enc_op_ld`, `rout_rrt_tx.rx_l04ad`, `rout_rrt_tx.tdm_tac_val`; attributes: `lab_bld_creatinine`; families: blood labs
- **Logical errors / review targets:** Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rx_av_nrti`

- **Primary purpose:** Rx: Nucleoside and nucleotide reverse transcriptase inhibitors.
- **Key inputs / dependencies:** attributes: `rxn_cui_485432`, `rxn_cui_485435`, `rxn_cui_393334`, `rxn_cui_1741729`, `rxn_cui_317397`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rx_cv_common`

- **Primary purpose:** Rx: Common cardiac drugs.
- **Key inputs / dependencies:** attributes: `rxn_cui_316100`, `rxn_cui_316098`, `rxn_cui_316099`, `rxnc_c09ca`, `rxn_cui_1600723`; families: RxNorm/ATC medication codes
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rx_cv_lmd`

- **Primary purpose:** Rx: Lipid Modifying drugs.
- **Key inputs / dependencies:** attributes: `rxn_cui_1422086`, `rxn_cui_597971`, `rxn_cui_597977`, `rxn_cui_597987`, `rxn_cui_617312`
- **Logical errors / review targets:** Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rx_desc_ptr`

- **Primary purpose:** serialize active medications.
- **Key inputs / dependencies:** attributes: `rx_desc_ptr`; families: medication attributes
- **Logical errors / review targets:** Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rx_is_sot`

- **Primary purpose:** Rx: Immunosuppresion for Solid organ Transplant.
- **Key inputs / dependencies:** attributes: `rxn_cui_330404`, `rxn_cui_42316`, `rxn_cui_998188`, `rxn_cui_977437`, `rxn_cui_977433`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `rx_rrt_common`

- **Primary purpose:** Rx: Common renal drugs.
- **Key inputs / dependencies:** attributes: `rxn_cui_315513`, `rxn_cui_328936`, `rxn_cui_857223`, `rxn_cui_749204`, `rxn_cui_336764`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Likely issue: no `#define_attribute(...)` metadata was found, which makes outputs harder to interpret and report consistently.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Add `#define_attribute(...)` declarations for reportable outputs and any key intermediate outputs worth surfacing.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `sx_abdo`

- **Primary purpose:** assess abdominal colorectal surgical procedures.
- **Key inputs / dependencies:** attributes: `caresys_3037300`, `caresys_32000%`, `caresys_32003%`, `caresys_32004%`, `caresys_32005%`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `tg2610`

- **Primary purpose:** detect untreated chronic disease.
- **Key inputs / dependencies:** binds: `rout_dmg.dod`, `rout_dmg_source.dmg_source`, `rout_cd_dm_dx.dm`, `rout_cd_dm_dx.dm_rxn`, `rout_cd_dm_glyc_cntrl.hba1c_n0_val`; attributes: `csu_action_tg2610`, `rxnc_c09aa`, `rxnc_c09ca`, `rxnc_c09%`, `obs_bp_systolic`; families: RxNorm/ATC medication codes, observations, blood labs; citations: `tg2610_ref1`, `tg2610_ref2`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `tg4100`

- **Primary purpose:** generate AKI trigger from labs.
- **Key inputs / dependencies:** binds: `rout_dmg.dod`, `rout_rrt.rrt`, `rout_ckd.ckd`, `rout_dmg_source.dmg_source`; attributes: `csu_action_tg4100`, `lab_bld_creatinine`, `lab_bld_egfr_c`; families: blood labs; citations: `tg4100_ref1`, `tg4100_ref2`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `tg4110`

- **Primary purpose:** generate AKI from hospital coded diagnosis.
- **Key inputs / dependencies:** binds: `rout_dmg.dod`, `rout_dmg_source.dmg_source`; attributes: `icd_n17%`, `csu_action_tg4110`; families: ICD coding
- **Logical errors / review targets:** Review target: the ruleblock is marked inactive (`is_active:0`), so it may be incomplete, deprecated, or not ready for production use.
- **Suggested fixes:** Confirm whether the rule should remain inactive; if not, complete validation and activate it intentionally.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `tg4122`

- **Primary purpose:** CKD stage 4 has not been seen in 12 months.
- **Key inputs / dependencies:** binds: `rout_dmg.age`, `rout_dmg.dod`, `rout_ckd.ckd`, `rout_engmnt_renal.enc_renal`, `rout_dmg_source.dmg_source`; attributes: `lab_bld_egfr_c`, `csu_action_tg4122`, `mbs_%`; families: blood labs
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `tg4123`

- **Primary purpose:** CKD 5 has not been seen in 6 months.
- **Key inputs / dependencies:** binds: `rout_dmg.age`, `rout_dmg.dod`, `rout_ckd.ckd`, `rout_engmnt_renal.enc_renal`, `rout_dmg_source.dmg_source`; attributes: `csu_action_tg4123`, `mbs_%`
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `tg4410`

- **Primary purpose:** detect nephrotic syndrome.
- **Key inputs / dependencies:** binds: `rout_dmg.dod`, `rout_dmg_source.dmg_source`, `rout_rrt.rrt`, `rout_cd_dm_dx.dm`, `rout_ckd.ckd`; attributes: `lab_ua_acr`, `lab_bld_egfr`, `lab_bld_albumin`, `lab_bld_cholesterol_total`, `obs_bp_systolic`; families: urine labs, blood labs, observations, ICD coding; citations: `tg4410_ref1`, `tg4410_ref2`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `tg4420`

- **Primary purpose:** detect nephritic syndrome.
- **Key inputs / dependencies:** binds: `rout_dmg.dod`, `rout_dmg_source.dmg_source`, `rout_rrt.rrt`, `rout_engmnt_renal.ref_renal`, `rout_engmnt_renal.enc_renal`; attributes: `csu_action_tg4420`, `lab_ua_acr`, `lab_bld_egfr`, `lab_ua_rbc`, `lab_ua_leucocytes`; families: urine labs, blood labs, observations; citations: `tg4420_ref1`, `tg4420_ref2`, `tg4420_ref3`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `tg4610`

- **Primary purpose:** generate CKD2 or 3 rapid progression 20% decline per annum.
- **Key inputs / dependencies:** binds: `rout_dmg.age`, `rout_dmg.dod`, `rout_ckd.ckd`, `rout_dmg_source.dmg_source`, `rout_ckd.ckd_stage`; attributes: `csu_action_tg4610`, `lab_bld_egfr_c`; families: blood labs; citations: `tg4610_ref1`
- **Logical errors / review targets:** Definite issue: at least one conditional statement appears to lack an explicit default branch.
- **Suggested fixes:** Add a trailing `{ => ... }` branch to every non-constant conditional chain.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `tg4620`

- **Primary purpose:** generate CKD4 or 5 rapid progression 5% decline per annum no AVF.
- **Key inputs / dependencies:** binds: `rout_dmg.dod`, `rout_dmg.age`, `rout_ckd.ckd`, `rout_ckd_egfr_metrics.egfr_slope2`, `rout_ckd.assert_level`; attributes: `csu_action_tg4620`; citations: `tg4620_ref1`, `tg4620_ref2`
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename.

## `tg4630`

- **Primary purpose:** detect albuminuria pharmacotherapy.
- **Key inputs / dependencies:** binds: `rout_dmg.dod`, `rout_rrt.rrt`, `rout_dmg_source.dmg_source`, `rout_cd_dm_dx.dm`, `rout_ckd.cga_a_val`; attributes: `csu_action_tg4630`, `rxnc_c09aa`, `rxnc_c09ca`, `rxnc_a10bk`, `rxnc_c03da`; families: RxNorm/ATC medication codes, observations; citations: `tg2610_ref1`, `tg2610_ref2`
- **Logical errors / review targets:** Definite issue: one or more functional statements appear after conditional statements, which violates Picorules ordering rules. Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination.
- **Suggested fixes:** Move all `=>` data-retrieval statements above every `:` conditional statement. Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename.

## `tg4660`

- **Primary purpose:** Algorithm medication safety concern in CKD.
- **Key inputs / dependencies:** binds: `rout_ckd.ckd`, `rout_dmg.dod`, `rout_dmg_source.dmg_source`, `rout_cd_dm_dx.dm_rxn_bg`, `rout_cd_dm_dx.dm_rxn_sglt2`; attributes: `csu_action_tg4660`, `rxnc_m01a%`; families: RxNorm/ATC medication codes; citations: `tg4660_ref1`, `tg4660_ref2`, `tg4660_ref3`
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename.

## `tg4720`

- **Primary purpose:** detect new RRT.
- **Key inputs / dependencies:** binds: `rout_dmg.dod`, `rout_dmg_source.dmg_source`; attributes: `csu_action_tg4720`, `icd_z49_1`, `caresys_1310006`, `caresys_1310007`, `caresys_1310008`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `tg4722`

- **Primary purpose:** detect new RRT.
- **Key inputs / dependencies:** binds: `rout_dmg.dod`, `rout_dmg_source.dmg_source`; attributes: `csu_action_tg4722`, `icd_z49_1`, `caresys_1310006`, `caresys_1310007`, `caresys_1310008`; families: ICD coding, ICPC coding
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename. Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.

## `tg4810`

- **Primary purpose:** detect high haemoglobin while on ESA.
- **Key inputs / dependencies:** binds: `rout_dmg.dod`, `rout_dmg_source.dmg_source`; attributes: `csu_action_tg4810`, `rxnc_b03xa`, `lab_bld_hb`; families: RxNorm/ATC medication codes, blood labs; citations: `tg4810_ref1`, `tg4810_ref2`
- **Logical errors / review targets:** Definite issue: a DV function appears to be called after `.val` or `.dt`, which is likely an invalid column specifier combination.
- **Suggested fixes:** Use `._` before DV functions, or switch to a non-DV aggregation if only value or date is needed.
- **Potential improvements:** Where duplicated derivations exist, prefer reusing upstream rule outputs via `.bind()` to keep phenotype logic aligned across the library. Document the external billing or trigger specification more explicitly so the coded criteria are auditable outside the filename. Make recency windows and unit assumptions explicit where thresholds drive decisions, especially for guideline-based lab cutoffs.

## `vacc_covid`

- **Primary purpose:** assess covid 19 vaccination.
- **Key inputs / dependencies:** attributes: `vacc_covid_comirnaty`, `vacc_covid_astrazeneca`, `vacc_covid_moderna`
- **Logical errors / review targets:** No obvious logic defect on a quick static read; treat this entry as a baseline review summary rather than a clean bill of health.
- **Suggested fixes:** No urgent code-level fix from static review; the main next step is targeted compile-time and clinical validation.
- **Potential improvements:** Add or strengthen `#doc(..., { cite: ... })` metadata where thresholds or phenotype definitions come from clinical literature or policy.
