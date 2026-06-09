# cd_cvra_recom_v2 — flow diagrams

Companion to [`cd_cvra_recom_v2.prb`](./cd_cvra_recom_v2.prb). Decision flows for each recommendation domain, sliced for readability. Diagrams reflect rule logic as of 2026-05-19; re-verify against the `.prb` if it has changed since.

For rationale, guideline citations (AU 2023, ESC/EAS 2025, AHA/ACC 2025 BP, KDIGO 2024) and v1→v2 changes, see the header comment of the `.prb`.

---

## 1. Overview — how bindings feed the recommendation engines

```mermaid
flowchart LR
    subgraph Inputs[Upstream ruleblocks]
        ENS[rout_cvra_ensemble]
        CVRA[rout_cvra]
        CKD[rout_ckd]
        DM[rout_cd_dm_dx + dm_comp]
        DYS[rout_cd_dyslip]
        HTN[rout_cd_htn]
        DMG[rout_dmg]
        DMRX[rout_cd_dm_rx_rcm]
        OBS[rout_cd_obesity]
        RISK[rout_at_risk]
    end

    subgraph Stage1[Risk reconciliation]
        CHR[clin_high_risk]
        FNP[fnp_uplift]
        CAT[cvra_cat_r 0..3]
    end

    subgraph Stage2[Targets and inventory]
        SBPT[sbp_target]
        LDLT[ldl_target]
        BPRX[rx_bp / bp_rx_n]
        LRX[lipid_rx_n]
    end

    subgraph Stage3[Override triggers]
        OVB[rx_override_bp]
        OVT[rx_override_tc]
    end

    subgraph Engines[Recommendation engines]
        R_BP[recom_rx_bp]
        R_LIP[recom_rx_lipid]
        R_AP[recom_rx_antiplatelet]
        R_CM[recom_cardiometab_rx]
        R_SMK[recom_smoking]
    end

    Inputs --> Stage1 --> Stage2 --> Stage3 --> Engines
    CAT --> Engines
    SBPT --> R_BP
    LDLT --> R_LIP
    Engines --> CONC[concordance_pct]
    Engines --> GAPS[gap_* flags]
```

---

## 2. Risk reconciliation → `cvra_cat_r`

Clinical overrides short-circuit the ensemble category. First match wins.

```mermaid
flowchart TD
    START([patient])
    Q1{cvd_prev = 1?}
    Q2{ckd >= 3?}
    Q3{fhc_prob >= 2?}
    Q5{dm = 1 AND dm_eod = 1?}
    Q6{albuminuria_persistent_au = 1?}
    Q7{fnp = 1 AND age 30..79 AND ensemble_cat in 1,2?}
    Q8{ensemble_cat > 0?}

    H3[/cvra_cat_r = 3<br/>clin_high_src/]
    UP[/cvra_cat_r = ensemble_cat + 1<br/>FNP/]
    EN[/cvra_cat_r = ensemble_cat<br/>FRAM or AUS or BOTH/]
    Z[/cvra_cat_r = 0<br/>NONE/]

    START --> Q1
    Q1 -- yes --> H3
    Q1 -- no  --> Q2
    Q2 -- yes --> H3
    Q2 -- no  --> Q3
    Q3 -- yes --> H3
    Q3 -- no  --> Q5
    Q5 -- yes --> H3
    Q5 -- no  --> Q6
    Q6 -- yes --> H3
    Q6 -- no  --> Q7
    Q7 -- yes --> UP
    Q7 -- no  --> Q8
    Q8 -- yes --> EN
    Q8 -- no  --> Z

    note["dm_eod = retinopathy OR neuropathy OR foot ulcer OR cga_a_val >= 2.<br/>albuminuria_persistent_au = >=2 uACR above sex-banded threshold spanning >=90 days."]
```

---

## 3. BP pharmacotherapy → `recom_rx_bp`

Codes: `1` initiate, `2` consider, `3` intensify, `4` maintain, `0` not indicated.

```mermaid
flowchart TD
    START([cvra_cat_r, rx_bp,<br/>sbp_above_target, rx_override_bp])
    OVR{rx_override_bp = 1?<br/>SBP>=160 or DBP>=100}
    OVR_RX{rx_bp = 0?}
    OVR_I[/recom_rx_bp = 1<br/>initiate/]
    OVR_X[/recom_rx_bp = 3<br/>intensify/]

    H{cvra_cat_r = 3?<br/>high}
    HRX{rx_bp = 0?}
    H_I[/= 1 initiate/]
    HABT{sbp_above_target?}
    H_X[/= 3 intensify/]
    H_M[/= 4 maintain/]

    M{cvra_cat_r = 2?<br/>intermediate}
    MRX{rx_bp = 0?}
    M_C[/= 2 consider/]
    MABT{sbp_above_target?}
    M_X[/= 3 intensify/]
    M_M[/= 4 maintain/]

    Z[/= 0 not indicated/]

    START --> OVR
    OVR -- yes --> OVR_RX
    OVR_RX -- yes --> OVR_I
    OVR_RX -- no  --> OVR_X
    OVR -- no --> H
    H -- yes --> HRX
    HRX -- yes --> H_I
    HRX -- no  --> HABT
    HABT -- yes --> H_X
    HABT -- no  --> H_M
    H -- no --> M
    M -- yes --> MRX
    MRX -- yes --> M_C
    MRX -- no  --> MABT
    MABT -- yes --> M_X
    MABT -- no  --> M_M
    M -- no --> Z

    target["sbp_target (AU 2023): 140 if age&gt;=80 (frailty proxy); else 130/80"]
```

---

## 4. Lipid pharmacotherapy → `recom_rx_lipid` (extended ladder)

Codes: `1` initiate statin, `2` consider statin, `3` intensify (add ezetimibe), `4` maintain, `5` add non-statin intensifier (bempedoic acid / PCSK9i / inclisiran), `0` not indicated.

```mermaid
flowchart TD
    START([cvra_cat_r, rx_statin, rx_ezet,<br/>ldl_above_target, rx_override_tc])

    OVR{rx_override_tc = 1?<br/>TC >= 7.5}
    OVR_S{rx_statin = 0?}
    OVR_I[/= 1 initiate statin/]
    OVR_X[/= 3 intensify add ezetimibe/]

    H{cvra_cat_r = 3?}
    H_NONE{lipid_rx_n = 0?}
    H_INIT[/= 1 initiate/]
    H_EZ{rx_statin>0 AND rx_ezet>0<br/>AND LDL above target?}
    H_NS[/= 5 add non-statin/]
    H_NOEZ{rx_statin>0 AND rx_ezet=0<br/>AND LDL above target?}
    H_INT[/= 3 add ezetimibe/]
    H_ATG{LDL at or below target?}
    H_M[/= 4 maintain/]

    M{cvra_cat_r = 2?}
    M_NONE{lipid_rx_n = 0?}
    M_CON[/= 2 consider/]
    M_M[/= 4 maintain/]

    Z[/= 0 not indicated/]

    START --> OVR
    OVR -- yes --> OVR_S
    OVR_S -- yes --> OVR_I
    OVR_S -- no  --> OVR_X
    OVR -- no --> H
    H -- yes --> H_NONE
    H_NONE -- yes --> H_INIT
    H_NONE -- no  --> H_EZ
    H_EZ  -- yes --> H_NS
    H_EZ  -- no  --> H_NOEZ
    H_NOEZ -- yes --> H_INT
    H_NOEZ -- no --> H_ATG
    H_ATG -- yes --> H_M
    H_ATG -- no  --> Z
    H -- no --> M
    M -- yes --> M_NONE
    M_NONE -- yes --> M_CON
    M_NONE -- no  --> M_M
    M -- no --> Z

    target["ldl_target: 1.8 if cvd_prev; 2.0 if cvra_cat_r=3; else 4.9 mmol/L"]
```

---

## 5. SGLT2i / GLP-1 cardio-renal → `recom_cardiometab_rx` (new in v2)

Codes: `1` initiate, `4` maintain, `0` not indicated.

```mermaid
flowchart TD
    START([dm, cvd_prev, ckd,<br/>rx_sglt2, rx_glp1])
    ELIG{dm = 1<br/>AND cvd_prev = 1 OR ckd &gt;= 3?}
    ON{rx_sglt2 = 0 AND rx_glp1 = 0?}
    INIT[/= 1 initiate<br/>SGLT2i or GLP-1 RA/]
    MAINT[/= 4 maintain/]
    Z[/= 0 not indicated/]

    START --> ELIG
    ELIG -- no  --> Z
    ELIG -- yes --> ON
    ON   -- yes --> INIT
    ON   -- no  --> MAINT

    GAP["gap_cardiometab_rx = 1 when result = 1<br/>n_met_cardiometab_v = 1 when result = 4"]
```

---

## 6. Antiplatelet, smoking, and concordance roll-up

Smaller branches grouped — each is shallow on its own.

```mermaid
flowchart TD
    subgraph AP[Antiplatelet — secondary prevention]
        AP_Q{cvd_prev = 1?}
        AP_NONE{antipl = 0 AND anticoag = 0?}
        AP_I[/recom_rx_antiplatelet = 1<br/>+ gap_antiplatelet/]
        AP_M[/recom_rx_antiplatelet = 4/]
        AP_Z[/= 0/]
        AP_Q -- yes --> AP_NONE
        AP_Q -- no  --> AP_Z
        AP_NONE -- yes --> AP_I
        AP_NONE -- no  --> AP_M
    end

    subgraph SMK[Smoking]
        SMK_Q{smoke0 >= 29?<br/>current}
        SMK_RX{rx_cessation present?}
        SMK_I[/= 1 offer cessation Rx<br/>+ gap_smoking_rx/]
        SMK_M[/= 2 maintain Rx/]
        SMK_EX{smoke0 = 20?<br/>ex-smoker}
        SMK_S[/= 3 sustain/]
        SMK_Z[/= 0/]
        SMK_Q -- yes --> SMK_RX
        SMK_RX -- no  --> SMK_I
        SMK_RX -- yes --> SMK_M
        SMK_Q -- no --> SMK_EX
        SMK_EX -- yes --> SMK_S
        SMK_EX -- no  --> SMK_Z
    end

    subgraph CONC[Concordance score]
        APP["n_applicable = sum of applicable domains<br/>(bp, lipid, antipl, smoking, cardiometab)"]
        MET["n_met = sum of domains at code 4 or smoking=2"]
        PCT[/concordance_pct =<br/>round(n_met / n_applicable * 100)/]
        APP --> PCT
        MET --> PCT
    end
```

---

## Maintenance

- Diagrams are hand-maintained. When a conditional in `.prb` changes, update the matching slice here.
- If drift becomes a problem across multiple ruleblocks, consider an auto-generator that walks the compiler AST and emits Mermaid per output variable.
