# Faction

Faction definitions including names and reputation data. Used to display faction names for reputation-gated recipes.

## Source

- Table: `Faction`
- API: `https://wago.tools/db2/Faction/csv?build={version}`

## CraftLib Usage

Used by `extract_db2_sources.py` and `generate_recipes.py` to get faction names:
- `ID` - Faction identifier (matches `ItemSparse.MinFactionID`)
- `Name_lang` - Display name (e.g., "Cenarion Expedition")

## Columns

Columns as of build `1.15.8.67156` (Classic Era / Season of Discovery).

| Column | Type | Description |
|--------|------|-------------|
| ReputationRaceMask_0 | int | Race restriction for standing 0 |
| ReputationRaceMask_1 | int | Race restriction for standing 1 |
| ReputationRaceMask_2 | int | Race restriction for standing 2 |
| ReputationRaceMask_3 | int | Race restriction for standing 3 |
| Name_lang | string | **Localized faction name** |
| Description_lang | string | Localized faction description |
| ID | int | Primary key (faction ID) |
| ReputationIndex | int | Index in reputation panel (-1 = hidden) |
| ParentFactionID | int | Parent faction for reputation spillover |
| Expansion | int | Expansion this faction was added |
| FriendshipRepID | int | Friendship reputation system ID |
| Flags | int | Faction flags |
| ParagonFactionID | int | Paragon faction ID (0 in Classic-family builds) |
| RenownFactionID | int | Renown faction ID (0 in Classic-family builds) |
| RenownCurrencyID | int | Renown currency ID (0 in Classic-family builds) |
| ReputationClassMask_0 | int | Class restriction for standing 0 |
| ReputationClassMask_1 | int | Class restriction for standing 1 |
| ReputationClassMask_2 | int | Class restriction for standing 2 |
| ReputationClassMask_3 | int | Class restriction for standing 3 |
| ReputationFlags_0 | int | Reputation flags for standing 0 |
| ReputationFlags_1 | int | Reputation flags for standing 1 |
| ReputationFlags_2 | int | Reputation flags for standing 2 |
| ReputationFlags_3 | int | Reputation flags for standing 3 |
| ReputationBase_0 | int | Base reputation for standing 0 |
| ReputationBase_1 | int | Base reputation for standing 1 |
| ReputationBase_2 | int | Base reputation for standing 2 |
| ReputationBase_3 | int | Base reputation for standing 3 |
| ReputationMax_0 | int | Max reputation for standing 0 |
| ReputationMax_1 | int | Max reputation for standing 1 |
| ReputationMax_2 | int | Max reputation for standing 2 |
| ReputationMax_3 | int | Max reputation for standing 3 |
| ParentFactionMod_0 | float | Reputation spillover modifier 0 |
| ParentFactionMod_1 | float | Reputation spillover modifier 1 |
| ParentFactionCap_0 | int | Reputation spillover cap 0 |
| ParentFactionCap_1 | int | Reputation spillover cap 1 |

## Build differences

Column-set differences of the other pinned builds (see `BUILDS.md`) from the list above.

- `2.5.5.65895` (TBC Anniversary): lacks `Flags`, `ParagonFactionID`, `RenownCurrencyID`, `RenownFactionID`; adds `Field_3_4_1_46722_008`, `Field_3_4_1_46722_009`, `Field_3_4_1_46722_010`, `Field_3_4_1_46722_011`.
- `3.4.5.63697` (WotLK Classic): lacks `Flags`, `ParagonFactionID`, `RenownCurrencyID`, `RenownFactionID`; adds `Field_3_4_1_46722_008`, `Field_3_4_1_46722_009`, `Field_3_4_1_46722_010`, `Field_3_4_1_46722_011`.
- `3.80.1.68318` (Titan): same columns.
- `1.60.1.71037` (WoW Forever): lacks `ReputationRaceMask_0`, `ReputationRaceMask_1`, `ReputationRaceMask_2`, `ReputationRaceMask_3`; adds `RenownThresholdCurveID`, `ReputationRaceMasks0_0`, `ReputationRaceMasks0_1`, `ReputationRaceMasks1_0`, `ReputationRaceMasks1_1`, `ReputationRaceMasks2_0`, `ReputationRaceMasks2_1`, `ReputationRaceMasks3_0`, `ReputationRaceMasks3_1`.

## Relationships

- `ParentFactionID` → `Faction.ID` - Parent faction hierarchy
- Referenced by `ItemSparse.MinFactionID` - Recipe faction requirements

## Example

Cenarion Expedition (faction 942) sells Alchemy recipes at Honored/Revered.

```csv
ID,Name_lang,ReputationIndex,...
942,Cenarion Expedition,59,...
```
