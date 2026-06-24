# db2-parser

[![License: All Rights Reserved](https://img.shields.io/badge/License-All_Rights_Reserved-red.svg)](LICENSE)

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

## Known Limitations

### Recipe Difficulty (SkillLineAbility)

DB2 does **not** contain the orange difficulty value (skill required to learn):

| Difficulty | DB2 Field | Available |
|------------|-----------|-----------|
| Orange | (not stored) | ❌ |
| Yellow | TrivialSkillLineRankLow | ✓ |
| Green | (not stored) | ❌ |
| Gray | TrivialSkillLineRankHigh | ✓ |

The `MinSkillLineRank` field is often 1 for all recipes and cannot be relied upon.

**Solution:** Consuming projects must fetch difficulty from Wowhead. See `schema/SkillLineAbility.md` for details.

## Expansion Version Mapping

| Major Version | Expansion |
|---------------|-----------|
| 1.x | Classic Era (Vanilla) |
| 2.x | TBC |
| 3.x | WotLK |
| 4.x | Cataclysm |
| 5.x | MoP |

## Season of Discovery (Classic Era)

Season of Discovery has **no separate build or product**. The live SoD data ships inside the
`wow_classic_era` product; the current SoD build is **`1.15.8.67156`**. That single build already
contains the base 1-300 recipes, the SoD-only seasonal recipes, and the SoD-tuned difficulty
thresholds, so the SoD dataset is fetched **wholesale** from it (no vanilla-baseline + overlay merge).

```bash
# Fetch the SoD / Classic Era build explicitly (reproducible)
make -C vendor/db2-parser fetch VERSION=1.15.8.67156

# ...or resolve the latest 1.x build automatically
make -C vendor/db2-parser latest EXPANSION=1
```

Notes:

- `latest EXPANSION=1` matches the highest `1.x` version across products. Pin the explicit
  `VERSION` when you need reproducibility.
- The **Anniversary** client is a *different* product (`wow_anniversary`, `2.5.5.x`). Pin it
  explicitly when regenerating the non-seasonal dataset; do not reuse a `wow_classic` /
  `wow_classic_era` build for it.
- `SkillLineAbility` rows with `TrivialSkillLineRankHigh == 0` are profession-rank entries
  (Apprentice/Journeyman/...), not craftable recipes - skip them. Use `SupercedesSpell` to
  collapse rank chains.
- DB2 has **no** season column. Whether a recipe is SoD-only (`seasonId == 2`) is known only from
  Wowhead's profession listview, not from these tables.

### What SoD difficulty looks like (worked example)

`Ironvine Belt` (spell `1213709`, Blacksmithing, SkillLine 164) - a seasonal recipe above the old
300 cap, cross-checked against Wowhead's `/classic/` page:

| Color | DB2 (this tool) | Wowhead | Agree? |
|-------|-----------------|---------|--------|
| Yellow | `TrivialSkillLineRankLow` = 320 | `colors[1]` = 320 | ✓ |
| Gray | `TrivialSkillLineRankHigh` = 340 | `colors[3]` = 340 | ✓ |
| Green | not stored | `colors[2]` = 330 (= midpoint of 320/340) | n/a |
| Orange | `MinSkillLineRank` = 1 (useless) | `learnedat` / `colors[0]` = 300 | n/a |

Takeaway: DB2 gives **yellow + gray** reliably (and they cross-validate Wowhead); **green** and
**orange** come only from Wowhead. Wowhead's `green` is the arithmetic midpoint of yellow/gray;
`orange` is the recipe's learn-at skill (`colors[0]` may be a `0` sentinel - prefer `learnedat`).

## Requirements

- Python 3.10+
- No external dependencies (stdlib only)

## License

All Rights Reserved - See [LICENSE](LICENSE) for details.
