# SpellReagents

Crafting reagent requirements for spells/recipes.

## Columns

| Column | Type | Description |
|--------|------|-------------|
| ID | int | Primary key |
| SpellID | int | Spell/recipe ID |
| Reagent_0 | int | First reagent item ID |
| Reagent_1 | int | Second reagent item ID |
| Reagent_2 | int | Third reagent item ID |
| Reagent_3 | int | Fourth reagent item ID |
| Reagent_4 | int | Fifth reagent item ID |
| Reagent_5 | int | Sixth reagent item ID |
| Reagent_6 | int | Seventh reagent item ID |
| Reagent_7 | int | Eighth reagent item ID |
| ReagentCount_0 | int | First reagent quantity |
| ReagentCount_1 | int | Second reagent quantity |
| ReagentCount_2 | int | Third reagent quantity |
| ReagentCount_3 | int | Fourth reagent quantity |
| ReagentCount_4 | int | Fifth reagent quantity |
| ReagentCount_5 | int | Sixth reagent quantity |
| ReagentCount_6 | int | Seventh reagent quantity |
| ReagentCount_7 | int | Eighth reagent quantity |

## Relationships

- `SpellID` → `Spell.ID`
- `Reagent_*` → `Item.ID`

## Notes

- Max 8 reagents per spell
- Unused slots have value 0
- Reagent_N pairs with ReagentCount_N
