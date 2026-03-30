# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**picorules-agent** is an agentic framework for understanding, writing, testing, optimizing, and compiling **Picorules** — a domain-specific language (DSL) for clinical decision support systems. Picorules bridges clinical reasoning and database queries, enabling clinicians to author complex medical logic that compiles to optimized SQL targeting the Entity-Attribute-Date-Value (EADV) data model.

## Key Resources

**Local (git submodules):**
- **Existing rule library** (~168 `.prb` files): `reference/rules/picodomain_rule_pack/rule_blocks/`
- **EADV attribute dictionary** (14,000+ attributes): `reference/dictionaries/eadv-att.csv`

**External:**
- **Language reference**: https://raw.githubusercontent.com/asaabey/picorules-docs/master/picorules-language-reference.md
- **Compiler** (`picorules-compiler-js-core` v1.0.7): Pure JS/TS compiler, multi-dialect (Oracle, SQL Server, PostgreSQL), available on npm
- **DB manager**: `picorules-compiler-js-db-manager` (npm)
- **EADV mocker**: `picorules-compiler-js-eadv-mocker` (npm)

## Picorules Language Essentials

### EADV Data Model
All clinical data lives in a four-column table: `eid` (patient), `att` (attribute name), `dt` (date), `val` (value). Attribute naming follows prefixes: `lab_bld_`, `lab_ua_`, `icd_`, `rx_`, `enc_`, `proc_`, `demo_`.

### Ruleblock Structure
Every `.prb` file follows this strict order:
1. `#define_ruleblock()` — metadata (id, description, is_active)
2. **Functional statements** (`=>`) — data retrieval/aggregation (must come before conditionals)
3. **Conditional statements** (`:`) — logic/transformation with `{ condition => value }` syntax
4. `#define_attribute()` / `#doc()` — output metadata and documentation

### Key Syntax Patterns
```
// Functional: fetch last value of an attribute
hb_last => eadv.lab_bld_haemoglobin.val.last();

// Functional with date filter
cr_recent => eadv.lab_bld_creatinine.val.where(dt > sysdate-365).min();

// Functional with multi-source
sbp => eadv.[bp_device_systolic,bp_manual_systolic]._.lastdv();

// Functional with wildcard + presence check
has_cvd => eadv.icd_I21%.dt.max();

// Cross-ruleblock binding
egfr_val => rout_ckd_egfr_metrics.egfr_l_val.val.bind();

// Conditional with default
is_anaemic : { hb_last < 120 => 1 }, { => 0 };

// Multi-case conditional
ckd_stage : { egfr >= 90 => `G1` }, { egfr >= 60 => `G2` }, { => `NA` };
```

### Column Specifiers
- `.val` — value only
- `.dt` — date only
- `._` — both (creates `var_val` and `var_dt` columns)

### Aggregation Functions
`last()`, `first()`, `max()`, `min()`, `count()`, `sum()`, `avg()`, `median()`, `distinct_count()`
DV (date-value) pairs: `lastdv()`, `firstdv()`, `maxldv()`, `minldv()`
Statistical: `regr_slope()`, `regr_intercept()`, `regr_r2()`

### Operators
Comparison: `=`, `!=`, `<>`, `<`, `>`, `<=`, `>=`
Logical: `and`, `or`, `not` (precedence: not > and > or)
NULL checks: `!?` (is not null), `?` (is null)

### Critical Rules
- All functional statements MUST precede conditional statements
- Conditional chains evaluate left-to-right; first match wins
- Every conditional MUST have a default case `{ => value }`
- Semicolons are mandatory
- String literals use backticks: `` `G1` ``
- `sysdate` is the current date reference for time-window calculations

## Compiler Usage

```js
import { compile, Dialect } from 'picorules-compiler-js-core';

const result = compile(
  [{ name: 'ckd', text: ruleblockSource, is_active: 2 }],
  { dialect: Dialect.TSQL }  // or Dialect.ORACLE, Dialect.POSTGRES
);
```

The compiler generates SQL with temp tables (T-SQL) or CTEs (other dialects), handling window functions, self-joins, NULL handling, and patient-level aggregation automatically.
