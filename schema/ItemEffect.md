# ItemEffect

Maps items to the spells they teach when used. Used to identify recipe items (items that teach crafting spells).

## Source

- Table: `ItemEffect`
- API: `https://wago.tools/db2/ItemEffect/csv?build={version}`

## CraftLib Usage

Used by `extract_db2_sources.py` and `generate_recipes.py` to identify recipe items:
- `SpellID` - The spell the item teaches
- `ParentItemID` - The item ID of the recipe

## Columns

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
| PlayerConditionID | int | Player condition requirement |
| ParentItemID | int | **Item that has this effect** |

## Relationships

- `SpellID` → `Spell.ID` - The spell this item teaches
- `ParentItemID` → `Item.ID` - The item with this effect

## Example

Recipe: Pattern: Nethercleft Leg Armor (item 29698) teaches spell 35554.

```csv
ID,SpellID,ParentItemID,...
12345,35554,29698,...
```
