# db2-parser Design

WoW DB2 data fetcher for crafting-related tables from wago.tools.

## Overview

A standalone data layer that downloads and documents raw DB2 tables from wago.tools. Consumed by CraftLib (and potentially other projects) as a git submodule.

```
wago.tools
    ↓ (download)
db2-parser/artifacts/{version}/*.csv + schema docs
    ↓ (consumed by)
CraftLib → transforms into Lua addon format
```

## Scope

- **Expansions**: Version-based (2.x=TBC, 3.x=WotLK, 4.x=Cata, etc.)
- **Tables**: Crafting-focused only
  - Spell, SpellName
  - Item, ItemSparse
  - SkillLine, SkillLineAbility
  - SpellReagents, SpellEffect
- **Output**: Raw CSVs with schema documentation

## Project Structure

```
db2-parser/
├── Makefile                    # Build orchestration
├── .gitignore                  # Ignore artifacts, tmp files
├── README.md                   # Usage contract for consuming repos
│
├── scripts/
│   ├── fetch.py               # Download CSVs from wago.tools
│   ├── latest.py              # Query latest build for expansion
│   └── validate.py            # Check schema matches CSVs
│
├── schema/
│   ├── Spell.md               # Column documentation
│   ├── SpellName.md
│   ├── Item.md
│   ├── ItemSparse.md
│   ├── SkillLine.md
│   ├── SkillLineAbility.md
│   ├── SpellReagents.md
│   └── SpellEffect.md
│
└── artifacts/                  # Downloaded data (gitignored)
    └── 2.5.5.65463/
        ├── Spell.csv
        ├── SpellName.csv
        └── ...
```

## Makefile Interface

```makefile
# Configuration
PYTHON := python3
SCRIPTS := scripts
ARTIFACTS := artifacts
SCHEMA := schema

# Crafting-focused tables to download
TABLES := Spell SpellName Item ItemSparse SkillLine SkillLineAbility SpellReagents SpellEffect

# Fetch specific version
# Usage: make fetch VERSION=2.5.5.65463
fetch:
	@$(PYTHON) $(SCRIPTS)/fetch.py --version $(VERSION) --tables $(TABLES) --output $(ARTIFACTS)

# Fetch latest for expansion
# Usage: make latest EXPANSION=2
latest:
	@$(PYTHON) $(SCRIPTS)/latest.py --expansion $(EXPANSION) --tables $(TABLES) --output $(ARTIFACTS)

# Validate schema matches downloaded CSVs
# Usage: make validate VERSION=2.5.5.65463
validate:
	@$(PYTHON) $(SCRIPTS)/validate.py --version $(VERSION) --schema $(SCHEMA) --artifacts $(ARTIFACTS)

# Remove all artifacts
clean:
	rm -rf $(ARTIFACTS)/*

.PHONY: fetch latest validate clean
```

## Scripts Behavior

### fetch.py

- Takes `--version`, `--tables`, `--output`
- Downloads each table from `https://wago.tools/db2/{table}/csv?build={version}`
- Saves to `artifacts/{version}/{table}.csv`
- Creates version directory if needed
- Prints progress: `Fetching Spell.csv... done`

### latest.py

- Takes `--expansion`, `--tables`, `--output`
- Queries `https://wago.tools/api/builds` to find all products
- Filters for latest version matching `{expansion}.x.x.x` pattern
- Calls fetch logic with discovered version
- Prints: `Latest for expansion 2: 2.5.5.65463`

### validate.py

- Takes `--version`, `--schema`, `--artifacts`
- For each table, reads CSV header row
- Parses corresponding `schema/{table}.md` for expected columns
- Compares and reports mismatches
- Exit code 0 if valid, 1 if mismatch
- Output: `Spell.csv: OK` or `Spell.csv: MISMATCH - missing: Foo, extra: Bar`

### Constraints

- Standard library only (no pip dependencies)
- Uses `urllib`, `csv`, `pathlib`

## Schema Documentation Format

Each `schema/{Table}.md` file documents the table's columns:

```markdown
# SpellReagents

Defines reagent requirements for spells (crafting recipes).

## Columns

| Column | Type | Description |
|--------|------|-------------|
| ID | int | Primary key, matches Spell.ID |
| Reagent_0 | int | Item ID of first reagent (0 if none) |
| Reagent_1 | int | Item ID of second reagent |
| ReagentCount_0 | int | Quantity of first reagent |
| ReagentCount_1 | int | Quantity of second reagent |

## Relationships

- `Reagent_*` → `Item.ID`
- `ID` → `Spell.ID`

## Notes

- Max 8 reagents per spell
- Unused slots have value 0
```

The validate script parses the `| Column |` rows to extract expected column names.

## Submodule Contract

Consuming repos add db2-parser as a submodule:

```bash
cd your-project
git submodule add <repo-url> vendor/db2-parser
```

Usage from consuming repo:

```bash
# Fetch specific version
make -C vendor/db2-parser fetch VERSION=2.5.5.65463

# Fetch latest for expansion (2=TBC, 3=WotLK, etc.)
make -C vendor/db2-parser latest EXPANSION=2

# Validate schema
make -C vendor/db2-parser validate VERSION=2.5.5.65463
```

Data location after fetch:

```
vendor/db2-parser/artifacts/{version}/{Table}.csv
```

## .gitignore

```gitignore
# Downloaded artifacts (fetched, not committed)
artifacts/

# Agent-specific (local only)
.claude/
claude.md

# Python
__pycache__/
*.pyc
*.pyo

# OS
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
```

## Data Source

- **API**: https://wago.tools/db2
- **Builds**: https://wago.tools/api/builds
- **CSV format**: `https://wago.tools/db2/{table}/csv?build={version}`

## Follow-up Tasks (after db2-parser implementation)

After db2-parser is complete and added as submodule to CraftLib:

- [ ] Update CraftLib build scripts to call `make -C vendor/db2-parser`
- [ ] Create CraftLib CSV parser for Lua generation
- [ ] Document CraftLib's dependency on db2-parser in CraftLib README
