# SpellTotems

Tools a spell needs in the caster's bags: a tool category (any item of that category, e.g. a
Skinning Knife or a runed enchanting rod) and/or a specific item.

## Source

- Table: `SpellTotems`
- API: `https://wago.tools/db2/SpellTotems/csv?build={version}`
- Present in every pinned build (see `BUILDS.md`).

## Columns

| Column | Type | Description |
|--------|------|-------------|
| ID | int | Primary key |
| SpellID | int | **Spell that needs the tools** |
| RequiredTotemCategoryID_0 | int | **First required tool category** (0 = none) |
| RequiredTotemCategoryID_1 | int | Second required tool category (0 = none) |
| Totem_0 | int | First required specific item (0 = none) |
| Totem_1 | int | Second required specific item (0 = none) |

## Relationships

- `SpellID` -> `Spell.ID` / `SpellName.ID`
- `RequiredTotemCategoryID_n` -> `TotemCategory.ID`
- `Totem_n` -> `Item.ID`
- An item belongs to a tool category through `ItemSparse.TotemCategoryID`.

## Example

Skinning (spell 8613) needs a Skinning Knife (tool category 363) in build `1.15.8.67156`:

```csv
ID,SpellID,RequiredTotemCategoryID_0,RequiredTotemCategoryID_1,Totem_0,Totem_1
12538,8613,363,0,0,0
```
