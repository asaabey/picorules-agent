# Copilot Instructions for `picorules-agent`

## Build and validation commands

```bash
npm install
```

```bash
# Compile one ruleblock (the main per-file validation workflow)
npm run compile -- new_rules/cd_masld.prb mssql
```

```bash
# Equivalent direct command; dialects: mssql (default), oracle, postgresql
node scripts/compile.mjs path/to/file.prb postgresql
```

- There is currently **no working automated test suite** in `package.json`; `npm test` is a placeholder that exits with an error.
- There is currently **no lint script** configured in `package.json`.

## High-level architecture

- This repository is an authoring workspace for **Picorules** clinical decision support ruleblocks, not a conventional Node application. The primary artifact is the `.prb` ruleblock.
- `scripts/compile.mjs` is the thin CLI wrapper around `picorules-compiler-js-core`. It reads a single `.prb` file, maps `mssql` / `oracle` / `postgresql` to compiler dialects, prints SQL to stdout, and prints errors, warnings, and timing to stderr.
- `new_rules/` is the main working area for authored and iterated ruleblocks. `reference/rules/picodomain_rule_pack/rule_blocks/` is the large upstream rule library used for examples, reuse, and `.bind()` dependencies.
- `reference/dictionaries/eadv-att.csv` is the canonical EADV attribute dictionary. Use it to confirm attribute names before introducing new EADV lookups.
- `.claude/skills/picorule/SKILL.md` captures the expected workflow for single-rule authoring, explanation, compilation, and validation. `.claude/skills/rule-cataloger/SKILL.md` covers bulk review/catalog work across many ruleblocks.
- `jobs/` and `new_templates/` contain source materials, wireframes, and supporting artifacts that feed new rule creation and recommendation content.

## Key conventions

- Before changing or writing a ruleblock, search `reference/rules/picodomain_rule_pack/rule_blocks/` for related logic and prefer `.bind()` reuse (`rout_*`) over re-deriving the same clinical concept locally.
- Also search `reference/dictionaries/eadv-att.csv` before adding any new EADV attribute reference; canonical attribute naming matters more here than in a typical DSL project.
- In `.prb` files, **all functional statements** (`=>`) must come before **all conditional statements** (`:`). `#doc()` blocks are commonly used between sections, but they do not relax the functional-before-conditional rule.
- Ruleblocks commonly expose their primary output through `[[rb_id]] : { . => ... };` near the end, followed by `#define_attribute(...)` metadata for reportable outputs.
- When a functional statement uses `._` or a DV function such as `lastdv()`, downstream logic should reference the generated `_val` and `_dt` fields rather than the base variable name.
- Clinical rationale is often preserved in top-of-file comments and `#doc()` sections, including citations and threshold notes. When logic changes, update those comments along with the rule.
- Treat `reference/` content as upstream reference data unless the task explicitly calls for editing it; most new or revised work belongs in `new_rules/`.
