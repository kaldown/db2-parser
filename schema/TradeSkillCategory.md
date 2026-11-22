# TradeSkillCategory

Names of the categories a profession's recipes are grouped under in the profession window.
`SkillLineAbility.TradeSkillCategoryID` points here, so the name tells which group a recipe
belongs to (for example the groups holding recipes carried over from another client).

## Source

- Table: `TradeSkillCategory`
- API: `https://wago.tools/db2/TradeSkillCategory/csv?build={version}`
- Fetched as an **optional** table (`OPTIONAL_TABLES` in the Makefile). Among the pinned builds
  (see `BUILDS.md`) it exists only in WoW Forever `1.60.1.71037`; the other builds answer
  HTTP 400.

## Columns

| Column | Type | Description |
|--------|------|-------------|
| ID | int | Primary key (category ID) |
| Name_lang | string | **Localized category name** (e.g. "Smelted Bars") |
| HordeName_lang | string | Name shown to Horde characters when it differs |
| ParentTradeSkillCategoryID | int | Parent category, 0 for a top-level one |
| SkillLineID | int | Skill line the category belongs to |
| OrderIndex | int | Sort position in the profession window |
| Flags | int | Flags |

## Relationships

- `ID` <- `SkillLineAbility.TradeSkillCategoryID`
- `ParentTradeSkillCategoryID` -> `TradeSkillCategory.ID`
- `SkillLineID` -> `SkillLine.ID`

## Example

```csv
ID,Name_lang,HordeName_lang,ParentTradeSkillCategoryID,SkillLineID,OrderIndex,Flags
2399,"Jewelcrafting (PROTOTYPE)",,0,2933,0,0
```
