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

### Handling orange=0 Recipes

Some Wowhead recipes return `orange=0`, meaning "always 100% skillup until yellow". This appears in two contexts:

| Context | Example | Orange | Yellow | Intended Use |
|---------|---------|--------|--------|--------------|
| Early-game | Delicate Copper Wire (JC) | 0 | 20 | Available from skill 1 |
| Late-game | Flask of Fortification (Alchemy) | 0 | 390 | Requires skill 375+ |

**Problem:** Naively using `skillRequired = 1` for all orange=0 recipes causes late-game recipes (flasks, transmutes) to appear as candidates at skill 1 in pathfinding algorithms.

**Recommended solution:** Use a threshold based on the first profession milestone (skill 75):

```python
EARLY_GAME_THRESHOLD = 75  # First milestone (Apprentice → Journeyman)

if orange > 0:
    skill_required = orange
elif yellow <= EARLY_GAME_THRESHOLD:
    skill_required = 1        # Early-game: available from start
else:
    skill_required = yellow   # Late-game: use yellow as requirement
```

This heuristic correctly categorizes:
- Starter recipes (yellow ≤ 75) → available from skill 1
- Progression recipes (yellow > 75) → require higher skill to obtain

See CraftLib's `scripts/generate_recipes.py` for the reference implementation.
