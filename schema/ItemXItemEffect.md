# ItemXItemEffect

Links items to their `ItemEffect` rows. In builds whose `ItemEffect` has no `ParentItemID`
column, this is the only way to find which item (e.g. a recipe pattern) carries an effect.

## Source

- Table: `ItemXItemEffect`
- API: `https://wago.tools/db2/ItemXItemEffect/csv?build={version}`
- Fetched as an **optional** table (`OPTIONAL_TABLES` in the Makefile). Among the pinned builds
  (see `BUILDS.md`) it exists only in WoW Forever `1.60.1.71037`; the other builds answer
  HTTP 400 and use `ItemEffect.ParentItemID` instead.

## Columns

| Column | Type | Description |
|--------|------|-------------|
| ID | int | Primary key |
| ItemEffectID | int | **The effect** |
| ItemID | int | **The item that has the effect** |

## Relationships

- `ItemEffectID` -> `ItemEffect.ID`
- `ItemID` -> `Item.ID` / `ItemSparse.ID`

To find the spell a recipe item teaches: `ItemXItemEffect.ItemID` -> `ItemEffectID` ->
`ItemEffect.SpellID`. An item can have several effects (one row each).

## Example

Pattern: Green Winter Clothes (item 34261) in build `1.60.1.71037`:

```csv
ID,ItemEffectID,ItemID
6767,108687,34261
6768,108688,34261
```

`ItemEffect` 108688 has `SpellID` 44950 (the learn effect); 108687 is the item's other effect.
