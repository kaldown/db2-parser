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
- TrivialSkillLineRankLow/High determine difficulty colors:
  - Orange: below TrivialSkillLineRankLow
  - Yellow: at TrivialSkillLineRankLow
  - Green: between Low and High
  - Gray: at or above TrivialSkillLineRankHigh
- AcquireMethod values:
  - 0 = Learn from trainer
  - 1 = Auto-learn when skill obtained
  - 2 = Racial skill
