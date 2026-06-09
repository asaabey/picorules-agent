# picorules-agent

An agentic framework for writing, validating, compiling, and explaining [Picorules](https://github.com/asaabey/picorules-docs) clinical decision support ruleblocks using [Claude Code](https://claude.ai/code).

## Quick Start

```bash
# Clone with submodules (rules library + EADV dictionary)
git clone <repo-url> --recurse-submodules
cd picorules-agent

# Install the compiler
npm install
```

## Using the `/picorule` Skill

The `/picorule` skill is a Claude Code slash command that handles the full ruleblock lifecycle. Open the project in Claude Code and use:

### Write a new ruleblock

```
/picorule write stage anaemia by haemoglobin levels
```

The skill will:
1. Search existing ruleblocks in `reference/rules/` for duplicates or related rules to `.bind()` to
2. Search `reference/dictionaries/eadv-att.csv` for correct EADV attribute names
3. Write the `.prb` file
4. Compile it to SQL and show the output

### Explain an existing ruleblock

```
/picorule explain reference/rules/picodomain_rule_pack/rule_blocks/ckd.prb
```

### Compile a ruleblock to SQL

```
/picorule compile new_rules/cd_masld.prb
```

Or directly from the command line:

```bash
# Dialects: mssql (default), oracle, postgresql
node scripts/compile.mjs new_rules/cd_masld.prb mssql
```

### Validate a ruleblock

```
/picorule validate new_rules/my_rule.prb
```

Checks for ordering violations, missing defaults, undefined variables, invalid attribute names, and other common errors.

## Project Structure

```
picorules-agent/
├── .claude/skills/picorule/   # Claude Code skill definition
│   └── SKILL.md
├── new_rules/                     # Your ruleblocks (new rules go here)
├── scripts/
│   └── compile.mjs            # Compiler CLI wrapper
├── reference/                 # Git submodules (read-only reference data)
│   ├── rules/                 # 168 existing .prb ruleblocks
│   └── dictionaries/          # EADV attribute dictionary (14,000+ attributes)
├── jobs/                      # Source materials (papers, specs)
├── CLAUDE.md                  # Claude Code project context
└── package.json               # picorules-compiler-js-core dependency
```

## What is Picorules?

Picorules is a domain-specific language for clinical decision support that compiles to SQL. It targets the Entity-Attribute-Date-Value (EADV) data model, enabling clinicians to author complex medical logic without writing SQL.

A simple ruleblock looks like:

```
#define_ruleblock([[rb_id]],
    { description: "Assess anaemia", is_active:2 }
);

hb => eadv.lab_bld_hb._.lastdv();

is_anaemic : { hb_val < 120 => 1 }, { => 0 };

[[rb_id]] : { . => is_anaemic };

#define_attribute(is_anaemic, { label:"Anaemia", is_reportable:1, type:1001 });
```

This compiles to optimized T-SQL/Oracle/PostgreSQL with window functions, temp tables, and patient-level joins.

## Updating Reference Data

```bash
# Pull latest rules and dictionaries from upstream
git submodule update --remote
```

## Key Dependencies

- [picorules-compiler-js-core](https://www.npmjs.com/package/picorules-compiler-js-core) - Picorules to SQL compiler
- [Claude Code](https://claude.ai/code) - AI coding assistant (required for the `/picorule` skill)
