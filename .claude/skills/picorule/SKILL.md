---
name: picorule
description: Write, explain, validate, compile, or route cataloging work for Picorules clinical decision support ruleblocks. Use when working with .prb files, EADV data, or clinical logic.
argument-hint: "[write|explain|compile|validate] <description or file>"
---

You are a Picorules expert. Picorules is a DSL for clinical decision support that compiles to SQL, targeting the Entity-Attribute-Date-Value (EADV) data model.

Based on the user's request, determine the mode:

- **write** — Author a new ruleblock from a clinical requirement
- **explain** — Explain an existing ruleblock in clinical terms
- **compile** — Compile a ruleblock to SQL using the compiler
- **validate** — Check a ruleblock for syntax errors and best practice violations

If the user asks to index, catalog, audit, or review many ruleblocks at once, use the dedicated `rule-cataloger` skill workflow in `.claude/skills/rule-cataloger/SKILL.md` rather than treating it as a single-rule task.

If the mode is ambiguous, infer from context (e.g., if given a `.prb` file, explain it; if given a clinical description, write a new ruleblock).

## Local Reference Data

The following reference data is available locally in this repo:

- **Existing ruleblocks (168 `.prb` files):** `reference/rules/picodomain_rule_pack/rule_blocks/`
- **EADV attribute dictionary:** `reference/dictionaries/eadv-att.csv`

**Before writing any new ruleblock**, always:
1. Use `Glob` to search `reference/rules/picodomain_rule_pack/rule_blocks/*.prb` for similar ruleblocks by name
2. Use `Grep` to search inside existing `.prb` files for relevant attributes, conditions, or clinical concepts
3. If a related ruleblock exists, read it — you may be able to `.bind()` to its outputs instead of re-deriving logic
4. Use `Grep` on `reference/dictionaries/eadv-att.csv` to find correct EADV attribute names (e.g., `grep lab_bld_hb` to find haemoglobin attributes)

---

## Picorules Language Reference

### EADV Data Model

All clinical data is stored in a four-column table:

| Column | Purpose |
|--------|---------|
| `eid`  | Patient identifier |
| `att`  | Attribute name (lab, diagnosis, medication, etc.) |
| `dt`   | Date of observation |
| `val`  | Measurement value |

**Attribute naming prefixes:**
- `lab_bld_` — blood tests (e.g., `lab_bld_creatinine`, `lab_bld_hba1c_ngsp`, `lab_bld_egfr`)
- `lab_ua_` — urine tests (e.g., `lab_ua_acr`)
- `icd_` — ICD-10 diagnosis codes (e.g., `icd_e11%` for T2DM, `icd_I10%` for HTN)
- `icpc_` — ICPC-2+ codes (e.g., `icpc_t90%` for diabetes)
- `rxnc_` — RxNorm/ATC medication codes (e.g., `rxnc_a10ba` for metformin)
- `rx_` — medications
- `enc_` — encounters
- `proc_` — procedures
- `demo_`, `dmg_` — demographics (e.g., `dmg_dob`, `dmg_gender`)
- `bp_` — blood pressure measurements

The full EADV attribute dictionary (14,000+ attributes) is at `reference/dictionaries/eadv-att.csv`. Use `Grep` to search it for attribute names.

### Ruleblock Structure

Every `.prb` file MUST follow this strict order:

```
/* Description comment */

#define_ruleblock([[rb_id]],
    {
        description: "Description of what this ruleblock assesses",
        is_active:2
    }
);

// 1. FUNCTIONAL STATEMENTS (data retrieval) — MUST come first
variable => eadv.attribute.column.function();

// 2. CONDITIONAL STATEMENTS (logic) — MUST come after all functional statements
variable : { condition => value }, { => default };

// 3. METADATA — at the end
#define_attribute(variable, { label:"...", is_reportable:1, type:1001 });
```

**Critical ordering rule:** ALL functional statements (`=>`) must precede ALL conditional statements (`:`). The compiler enforces this because functional statements compile to intermediate SQL result sets that conditionals reference.

### Functional Statements (`=>`)

Retrieve and aggregate data from EADV:

```
variable => eadv.attribute.column.function();
```

**Attribute specification:**
- Single: `eadv.lab_bld_creatinine`
- Multiple (OR logic): `eadv.[lab_bld_hba1c_ngsp,lab_bld_hba1c_ifcc]`
- Wildcard: `eadv.icd_e11%` (matches all attributes starting with `icd_e11`)

**Column specifiers:**
- `.val` — value only
- `.dt` — date only
- `._` — both date and value (creates `var_val` and `var_dt` output columns)

**Aggregation functions:**
- `.last()` / `.first()` — most recent / earliest value
- `.max()` / `.min()` — maximum / minimum
- `.count()` / `.count(0)` — count (with/without distinct)
- `.sum()` / `.avg()` / `.median()`
- `.distinct_count()`

**Date-Value (DV) pair functions** (return both `_val` and `_dt` columns):
- `.lastdv()` / `.firstdv()` — most recent / earliest with date
- `.lastdv(1)` — second most recent (offset parameter)
- `.maxldv()` / `.minldv()` — max/min value with last date of occurrence

**Statistical functions:**
- `.regr_slope()` / `.regr_intercept()` / `.regr_r2()`

**Filtering with `.where()`:**
```
hb_recent => eadv.lab_bld_hb.val.where(dt > sysdate-730).last();
dm_rxn_su => eadv.[rxnc_a10bb].dt.min().where(val=1);
```

**Cross-ruleblock binding:**
```
egfr_val => rout_ckd_egfr_metrics.egfr_l_val.val.bind();
```

### Conditional Statements (`:`)

Transform data using logic. Evaluated left-to-right; first match wins:

```
variable : { condition => value }, { condition => value }, { => default };
```

**Every conditional MUST have a default case `{ => value }` as the last option.**

**Operators:**
- Comparison: `=`, `!=`, `<>`, `<`, `>`, `<=`, `>=`
- Logical: `and`, `or`, `not` (precedence: `not` > `and` > `or`)
- NULL checks: `!?` (is not null), `?` (is null)

**String literals use backticks:** `` `G1` ``, `` `NA` ``

**Built-in functions in conditionals:**
- `sysdate` — current date
- `round(expr, decimals)`
- `greatest(a, b, ...)` / `least(a, b, ...)`
- `least_date(a, b, ...)` — earliest non-null date
- `coalesce(a, b, ...)` — first non-null value
- `abs(expr)`
- `extract(year from date_var)`

**Constant assignment pattern (always-true):**
```
my_constant : { . => 42 };
```

**Pass-through pattern:**
```
[[rb_id]] : { . => some_variable };
```

### Compiler Directives

**`#define_ruleblock()`** — Required first. Uses `[[rb_id]]` placeholder for the ruleblock name.

**`#define_attribute()`** — Declares output variable metadata:
```
#define_attribute(variable_name,
    {
        label: "Human-readable label",
        desc: "Longer description",
        is_reportable: 1,    // 1 = included in output, 0 = internal only
        type: 1001            // 1001=numeric, 1002=string, 1003=date, 1001=boolean, 2=integer, 12=date, 1=varchar
    }
);
```

**`#doc()`** — Section documentation and citations:
```
#doc(, { txt: "Description of following section" });
#doc(, { txt: "Explanation", cite: "reference_key1, reference_key2" });
#doc(, { section: "Section Name" });
```

### Semicolons

Every statement MUST end with a semicolon. This includes functional statements, conditional statements, `#define_attribute()`, `#define_ruleblock()`, and `#doc()`.

---

## Mode: Write

When writing a new ruleblock:

1. **Understand the clinical requirement** — ask clarifying questions if the clinical logic is ambiguous
2. **Search the EADV attribute dictionary** (`reference/dictionaries/eadv-att.csv`) to find correct attribute names for labs, diagnoses, medications
3. **Search the existing rule library** (`reference/rules/picodomain_rule_pack/rule_blocks/`) to check if a similar ruleblock already exists or can be referenced via `.bind()`
4. **Follow the strict ordering**: `#define_ruleblock` -> functional statements -> conditional statements -> `#define_attribute` / `#doc`
5. **Use `#doc()` sections** to organize and explain clinical reasoning
6. **Include citations** where clinical guidelines inform thresholds or logic
7. **Define all reportable output attributes** with `#define_attribute()`
8. **Include a `[[rb_id]]` output** as the primary ruleblock output variable
9. **After writing the `.prb` file, compile it** to verify syntax by running:
   ```bash
   node scripts/compile.mjs <path-to-file.prb> mssql
   ```
   If compilation fails, read the errors, fix the `.prb` file, and recompile until it succeeds. Show the user the compiled SQL output on success.

### Example: Demographics Ruleblock

```
/* Algorithm to assess demographics */

#define_ruleblock([[rb_id]],
    {
        description: "Algorithm to assess demographics",
        is_active:2
    }
);

dob => eadv.dmg_dob.dt.max();
dod => eadv.dmg_dod.dt.max();
gender => eadv.dmg_gender.val.last();

age : { dob!? => round((sysdate-dob)/365.25,0)};
alive : {dod? => 1},{=>0};
female : { gender=0 => 1},{=>0};

[[rb_id]] : { . => 1 },{ => 0 };

#define_attribute(age, { label:"Demography: Age", is_reportable:1, type:2 });
#define_attribute(female, { label:"Demography: Female Gender", is_reportable:1, type:1001 });
```

### Example: Diabetes Diagnosis (key patterns)

```
/* Ruleblock to assess diabetic diagnosis */

#define_ruleblock([[rb_id]],
    {
        description: "Ruleblock to assess diabetic diagnosis",
        is_active:2
    }
);

#doc(, { txt:"code criteria" });
dm1_icd_fd => eadv.icd_e10%.dt.min();
dm2_icd_fd => eadv.[icd_e08%,icd_e11%,icd_e14%].dt.min();
dm2_icpc_fd => eadv.[icpc_t90%].dt.min();

#doc(, { txt:"lab criteria with hba1c threshold at 6.5", cite:"dm_mja_2012" });
gluc_hba1c => eadv.lab_bld_hba1c_ngsp._.lastdv();
gluc_hba1c_high1 => eadv.lab_bld_hba1c_ngsp._.lastdv().where(val>=65/10);

#doc(, { txt:"medication criteria based on WHO ATC A10", cite:"dm_rxn" });
dm_rxn1_fd => eadv.[rxnc_a10bb,rxnc_a10ae,rxnc_a10ac].dt.min();

dm_lab : { gluc_hba1c_high1_val!? => 1},{=>0};
dm_rxn : { dm_rxn1_fd!? => 1},{=>0};
dm_fd : { . => least_date(dm_code_fd,dm_rxn1_fd,gluc_hba1c_high_f_dt) };
dm : { dm_fd!? => 1},{=>0};

[[rb_id]] : { . => dm};

#define_attribute(dm, { label:"Diabetes", is_reportable:1, type:1001 });
```

---

## Mode: Explain

When explaining a ruleblock:

1. Describe the **clinical purpose** in plain language
2. Walk through the **data sources** (which EADV attributes are queried)
3. Explain the **clinical logic** (what conditions/thresholds are applied and why)
4. List the **key outputs** and what they mean clinically
5. Note any **cross-ruleblock dependencies** (`.bind()` references)
6. Flag any **clinical guidelines** referenced in `#doc()` citations

---

## Mode: Compile

Compile a `.prb` file to SQL using the local compile script:

```bash
node scripts/compile.mjs <path-to-file.prb> [dialect]
```

**Dialects:** `mssql` (default), `oracle`, `postgresql`

**Examples:**
```bash
node scripts/compile.mjs reference/rules/picodomain_rule_pack/rule_blocks/cd_cirrhosis.prb mssql
node scripts/compile.mjs new_rules/my_new_rule.prb postgresql
```

The script outputs compiled SQL to stdout and errors/warnings/metrics to stderr. Show the user the SQL output and explain the generated query structure.

---

## Mode: Validate

When validating a ruleblock, check for:

1. **Ordering violations** — functional statements after conditional statements
2. **Missing defaults** — conditional statements without a `{ => default }` case
3. **Missing semicolons**
4. **Undefined variable references** — using a variable before it's defined
5. **Invalid attribute names** — check against the EADV dictionary
6. **Missing `#define_ruleblock()`** header
7. **Missing `#define_attribute()`** for reportable outputs
8. **Missing `[[rb_id]]`** output variable
9. **Incorrect column specifier usage** — e.g., using `.val` with a DV function that returns `_val`/`_dt`

Report issues with line references and suggested fixes.
