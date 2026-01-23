# db2-parser

WoW DB2 data fetcher for crafting-related tables from [wago.tools](https://wago.tools/db2).

## Overview

Downloads raw DB2 CSV files from wago.tools and stores them in versioned directories. Designed to be used as a git submodule by consuming projects (like CraftLib).

## Adding as Submodule

```bash
cd your-project
git submodule add <repo-url> vendor/db2-parser
git submodule update --init --recursive
```

## Usage

### Fetch Specific Version

```bash
make -C vendor/db2-parser fetch VERSION=2.5.5.65463
```

### Fetch Latest for Expansion

```bash
# 2 = TBC, 3 = WotLK, 4 = Cata, etc.
make -C vendor/db2-parser latest EXPANSION=2
```

### Validate Schema

```bash
make -C vendor/db2-parser validate VERSION=2.5.5.65463
```

### Clean Artifacts

```bash
make -C vendor/db2-parser clean
```

## Data Location

After fetching, CSVs are at:

```
vendor/db2-parser/artifacts/{version}/{Table}.csv
```

Example:
```
vendor/db2-parser/artifacts/2.5.5.65463/Spell.csv
vendor/db2-parser/artifacts/2.5.5.65463/SpellName.csv
vendor/db2-parser/artifacts/2.5.5.65463/Item.csv
...
```

## Available Tables

| Table | Description |
|-------|-------------|
| Spell | Spell descriptions and subtexts |
| SpellName | Spell/recipe display names |
| Item | Core item properties |
| ItemSparse | Extended item data with names |
| ItemEffect | Recipe item to spell mapping |
| SkillLine | Profession metadata |
| SkillLineAbility | Recipe-to-profession mapping |
| SpellReagents | Crafting reagent requirements |
| SpellEffect | Spell effects (crafted items, yields) |
| Faction | Faction names for reputation vendors |

## Schema Documentation

See `schema/{Table}.md` for column definitions and relationships.

## Expansion Version Mapping

| Major Version | Expansion |
|---------------|-----------|
| 1.x | Classic Era (Vanilla) |
| 2.x | TBC |
| 3.x | WotLK |
| 4.x | Cataclysm |
| 5.x | MoP |

## Requirements

- Python 3.10+
- No external dependencies (stdlib only)

## License

MIT
