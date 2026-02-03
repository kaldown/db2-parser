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

| Column | Type | Description |
|--------|------|-------------|
| ID | int | Primary key (faction ID) |
| Name_lang | string | **Localized faction name** |
| Description_lang | string | Localized faction description |
| ReputationIndex | int | Index in reputation panel (-1 = hidden) |
| ParentFactionID | int | Parent faction for reputation spillover |
| Expansion | int | Expansion this faction was added |
| FriendshipRepID | int | Friendship reputation system ID |
| Field_3_4_1_46722_008 | int | Unknown field |
| Field_3_4_1_46722_009 | int | Unknown field |
| Field_3_4_1_46722_010 | int | Unknown field |
| Field_3_4_1_46722_011 | int | Unknown field |
| ReputationRaceMask_0 | int | Race restriction for standing 0 |
| ReputationRaceMask_1 | int | Race restriction for standing 1 |
| ReputationRaceMask_2 | int | Race restriction for standing 2 |
| ReputationRaceMask_3 | int | Race restriction for standing 3 |
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

## Relationships

- `ParentFactionID` → `Faction.ID` - Parent faction hierarchy
- Referenced by `ItemSparse.MinFactionID` - Recipe faction requirements

## Example

Cenarion Expedition (faction 942) sells Alchemy recipes at Honored/Revered.

```csv
ID,Name_lang,ReputationIndex,...
942,Cenarion Expedition,59,...
```
