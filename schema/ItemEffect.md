# ItemEffect

Maps items to the spells they teach when used. Used to identify recipe items (items that teach crafting spells).

## Source

- Table: `ItemEffect`
- API: `https://wago.tools/db2/ItemEffect/csv?build={version}`

## CraftLib Usage

Used by `extract_db2_sources.py` and `generate_recipes.py` to identify recipe items:
- `SpellID` - The spell the item teaches
- `ParentItemID` - The item ID of the recipe

WoW Forever (`1.60.1.71037`) has no `ParentItemID`; there the item is found through
`ItemXItemEffect` (`ItemID` -> `ItemEffectID` -> `ItemEffect.ID`). See `schema/ItemXItemEffect.md`.

## Columns

Columns as of build `1.15.8.67156` (Classic Era / Season of Discovery).

| Column | Type | Description |
|--------|------|-------------|
| ID | int | Primary key |
| LegacySlotIndex | int | Legacy slot index |
| TriggerType | int | When the effect triggers (0=use, 1=equip, etc.) |
| Charges | int | Number of charges (-1 = infinite) |
| CoolDownMSec | int | Cooldown in milliseconds |
| CategoryCoolDownMSec | int | Category cooldown in milliseconds |
| SpellCategoryID | int | Spell category |
| SpellID | int | **Spell taught when item is used** |
| ChrSpecializationID | int | Class specialization restriction |
| ParentItemID | int | **Item that has this effect** |

## Build differences

Column-set differences of the other pinned builds (see `BUILDS.md`) from the list above.

- `2.5.5.65895` (TBC Anniversary): adds `PlayerConditionID`.
- `3.4.5.63697` (WotLK Classic): same columns.
- `3.80.1.68318` (Titan): adds `PlayerConditionID`.
- `1.60.1.71037` (WoW Forever): lacks `ParentItemID`; adds `PlayerConditionID`.

## Relationships

- `SpellID` → `Spell.ID` - The spell this item teaches
- `ParentItemID` → `Item.ID` - The item with this effect (builds that have the column)
- `ID` ← `ItemXItemEffect.ItemEffectID` - item link in builds without `ParentItemID`

## Example

Recipe: Pattern: Nethercleft Leg Armor (item 29698) teaches spell 35554.

```csv
ID,SpellID,ParentItemID,...
12345,35554,29698,...
```
