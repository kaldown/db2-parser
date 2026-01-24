# SkillLineAbility

Maps spells/recipes to professions with skill requirements.

## Columns

| Column | Type | Description |
|--------|------|-------------|
| RaceMask | int | Race restrictions bitmask |
| ID | int | Primary key |
| SkillLine | int | Profession skill line ID |
| Spell | int | Spell/recipe ID |
| MinSkillLineRank | int | Minimum skill to learn |
| ClassMask | int | Class restrictions bitmask |
| SupercedesSpell | int | Spell this replaces (rank upgrades) |
| AcquireMethod | int | How recipe is learned (0=trainer, 1=auto, 2=racial) |
| TrivialSkillLineRankHigh | int | Skill level where recipe turns gray |
| TrivialSkillLineRankLow | int | Skill level where recipe turns yellow |
| Flags | int | Ability flags |
| NumSkillUps | int | Number of skill points gained |
| UniqueBit | int | Unique identifier bit |
| TradeSkillCategoryID | int | Trade skill category |
| SkillupSkillLineID | int | Skill line for skill ups |
| CharacterPoints_0 | int | Character points 1 |
| CharacterPoints_1 | int | Character points 2 |

## Relationships

- `SkillLine` → `SkillLine.ID`
- `Spell` → `Spell.ID` / `SpellName.ID`
- `SupercedesSpell` → `Spell.ID` (for rank upgrades)

## Notes

- Key for mapping recipes to professions
- AcquireMethod values:
  - 0 = Learn from trainer
  - 1 = Auto-learn when skill obtained
  - 2 = Racial skill

## Difficulty Colors

DB2 provides **only yellow and gray** values:

| Color | DB2 Field | Available |
|-------|-----------|-----------|
| Orange | (not stored) | ❌ Must fetch from Wowhead |
| Yellow | TrivialSkillLineRankLow | ✓ |
| Green | (not stored) | ❌ Calculate: (yellow + gray) / 2 |
| Gray | TrivialSkillLineRankHigh | ✓ |

### Why Orange Cannot Be Calculated

The orange value (skill required to learn) is NOT reliably derivable from DB2:
- `MinSkillLineRank` is often 1 for all recipes (unreliable)
- Formula `2 * yellow - gray` works for some recipes but not all
- Example: Silver Contact has orange=90, yellow=110, gray=140
  - Formula gives: 2*110-140 = 80 (wrong)
  - Gap orange→yellow (20) ≠ gap yellow→gray (30)

**Solution:** Fetch difficulty from Wowhead spell pages using `fetch_wowhead_sources.py --difficulty`
