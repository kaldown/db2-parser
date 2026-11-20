# TotemCategory

Names of tool categories referenced by `SpellTotems` and `ItemSparse.TotemCategoryID`.

## Source

- Table: `TotemCategory`
- API: `https://wago.tools/db2/TotemCategory/csv?build={version}`
- Present in every pinned build (see `BUILDS.md`).

## Columns

| Column | Type | Description |
|--------|------|-------------|
| ID | int | Primary key (tool category ID) |
| Name_lang | string | **Localized category name** (e.g. "Skinning Knife") |
| TotemCategoryType | int | Category type |
| TotemCategoryMask | int | Mask; categories of the same type match when masks overlap |

## Relationships

- `ID` <- `SpellTotems.RequiredTotemCategoryID_n`
- `ID` <- `ItemSparse.TotemCategoryID`

## Example

```csv
ID,Name_lang,TotemCategoryType,TotemCategoryMask
363,"Skinning Knife",1,1
```
