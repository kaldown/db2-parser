# ItemSparse

Extended item data including names, stats, and requirements.

## Columns

| Column | Type | Description |
|--------|------|-------------|
| ID | int | Primary key, item ID |
| AllowableRace | int | Race restrictions bitmask |
| Description_lang | string | Item description |
| Display3_lang | string | Display name variant 3 |
| Display2_lang | string | Display name variant 2 |
| Display1_lang | string | Display name variant 1 |
| Display_lang | string | Primary display name |
| DmgVariance | float | Damage variance |
| DurationInInventory | int | Duration in inventory (seconds) |
| QualityModifier | float | Quality modifier |
| BagFamily | int | Bag type restrictions |
| StartQuestID | int | Quest started by item |
| ItemRange | float | Item range |
| StatPercentageOfSocket_0 | float | Socket stat percentage 1 |
| StatPercentageOfSocket_1 | float | Socket stat percentage 2 |
| StatPercentageOfSocket_2 | float | Socket stat percentage 3 |
| StatPercentageOfSocket_3 | float | Socket stat percentage 4 |
| StatPercentageOfSocket_4 | float | Socket stat percentage 5 |
| StatPercentageOfSocket_5 | float | Socket stat percentage 6 |
| StatPercentageOfSocket_6 | float | Socket stat percentage 7 |
| StatPercentageOfSocket_7 | float | Socket stat percentage 8 |
| StatPercentageOfSocket_8 | float | Socket stat percentage 9 |
| StatPercentageOfSocket_9 | float | Socket stat percentage 10 |
| StatPercentEditor_0 | float | Stat percent editor 1 |
| StatPercentEditor_1 | float | Stat percent editor 2 |
| StatPercentEditor_2 | float | Stat percent editor 3 |
| StatPercentEditor_3 | float | Stat percent editor 4 |
| StatPercentEditor_4 | float | Stat percent editor 5 |
| StatPercentEditor_5 | float | Stat percent editor 6 |
| StatPercentEditor_6 | float | Stat percent editor 7 |
| StatPercentEditor_7 | float | Stat percent editor 8 |
| StatPercentEditor_8 | float | Stat percent editor 9 |
| StatPercentEditor_9 | float | Stat percent editor 10 |
| Field_1_15_3_55112_014_0 | int | Unknown field 1 |
| Field_1_15_3_55112_014_1 | int | Unknown field 2 |
| Field_1_15_3_55112_014_2 | int | Unknown field 3 |
| Field_1_15_3_55112_014_3 | int | Unknown field 4 |
| Field_1_15_3_55112_014_4 | int | Unknown field 5 |
| Field_1_15_3_55112_014_5 | int | Unknown field 6 |
| Field_1_15_3_55112_014_6 | int | Unknown field 7 |
| Field_1_15_3_55112_014_7 | int | Unknown field 8 |
| Field_1_15_3_55112_014_8 | int | Unknown field 9 |
| Field_1_15_3_55112_014_9 | int | Unknown field 10 |
| StatModifier_bonusStat_0 | int | Bonus stat type 1 |
| StatModifier_bonusStat_1 | int | Bonus stat type 2 |
| StatModifier_bonusStat_2 | int | Bonus stat type 3 |
| StatModifier_bonusStat_3 | int | Bonus stat type 4 |
| StatModifier_bonusStat_4 | int | Bonus stat type 5 |
| StatModifier_bonusStat_5 | int | Bonus stat type 6 |
| StatModifier_bonusStat_6 | int | Bonus stat type 7 |
| StatModifier_bonusStat_7 | int | Bonus stat type 8 |
| StatModifier_bonusStat_8 | int | Bonus stat type 9 |
| StatModifier_bonusStat_9 | int | Bonus stat type 10 |
| Stackable | int | Max stack size |
| MaxCount | int | Max inventory count |
| MinReputation | int | Min reputation required |
| RequiredAbility | int | Required ability ID |
| SellPrice | int | Vendor sell price (copper) |
| BuyPrice | int | Vendor buy price (copper) |
| VendorStackCount | int | Vendor stack size |
| PriceVariance | float | Price variance |
| PriceRandomValue | float | Random price modifier |
| Flags_0 | int | Item flags 1 |
| Flags_1 | int | Item flags 2 |
| Flags_2 | int | Item flags 3 |
| Flags_3 | int | Item flags 4 |
| Flags_4 | int | Item flags 5 |
| OppositeFactionItemID | int | Opposite faction equivalent |
| Field_1_15_7_59706_027 | int | Unknown field |
| ContentTuningID | int | Content tuning reference |
| Field_1_15_7_59706_029 | int | Unknown field |
| MaxDurability | int | Maximum durability |
| ItemNameDescriptionID | int | Name description ID |
| Field_1_15_7_59706_032 | int | Unknown field |
| RequiredHoliday | int | Required holiday event |
| LimitCategory | int | Limit category |
| Gem_properties | int | Gem properties |
| Socket_match_enchantment_ID | int | Socket bonus enchant |
| TotemCategoryID | int | Totem category |
| InstanceBound | int | Instance bound type |
| ZoneBound_0 | int | Zone bound 1 |
| ZoneBound_1 | int | Zone bound 2 |
| ItemSet | int | Item set ID |
| LockID | int | Lock ID for locked items |
| PageID | int | Readable page ID |
| ItemDelay | int | Attack delay |
| MinFactionID | int | Minimum faction ID |
| RequiredSkillRank | int | Required skill level |
| RequiredSkill | int | Required skill ID |
| ItemLevel | int | Item level |
| AllowableClass | int | Class restrictions |
| ItemRandomSuffixGroupID | int | Random suffix group |
| RandomSelect | int | Random enchant pool |
| MinDamage_0 | float | Primary min damage |
| MinDamage_1 | float | Secondary min damage |
| MinDamage_2 | float | Tertiary min damage |
| MinDamage_3 | float | Fourth min damage |
| MinDamage_4 | float | Fifth min damage |
| MaxDamage_0 | float | Primary max damage |
| MaxDamage_1 | float | Secondary max damage |
| MaxDamage_2 | float | Tertiary max damage |
| MaxDamage_3 | float | Fourth max damage |
| MaxDamage_4 | float | Fifth max damage |
| Resistances_0 | int | Armor |
| Resistances_1 | int | Holy resistance |
| Resistances_2 | int | Fire resistance |
| Resistances_3 | int | Nature resistance |
| Resistances_4 | int | Frost resistance |
| Resistances_5 | int | Shadow resistance |
| Resistances_6 | int | Arcane resistance |
| Field_1_15_7_59706_054 | int | Unknown field |
| StatModifier_bonusAmount_0 | int | Bonus stat amount 1 |
| StatModifier_bonusAmount_1 | int | Bonus stat amount 2 |
| StatModifier_bonusAmount_2 | int | Bonus stat amount 3 |
| StatModifier_bonusAmount_3 | int | Bonus stat amount 4 |
| StatModifier_bonusAmount_4 | int | Bonus stat amount 5 |
| StatModifier_bonusAmount_5 | int | Bonus stat amount 6 |
| StatModifier_bonusAmount_6 | int | Bonus stat amount 7 |
| StatModifier_bonusAmount_7 | int | Bonus stat amount 8 |
| StatModifier_bonusAmount_8 | int | Bonus stat amount 9 |
| StatModifier_bonusAmount_9 | int | Bonus stat amount 10 |
| ExpansionID | int | Expansion this item is from |
| Field_1_15_7_59706_057 | int | Unknown field |
| Field_1_15_7_59706_058 | int | Unknown field |
| Field_1_15_7_59706_059 | int | Unknown field |
| SocketType_0 | int | Socket type 1 |
| SocketType_1 | int | Socket type 2 |
| SocketType_2 | int | Socket type 3 |
| SheatheType | int | How item is sheathed |
| Material | int | Material type |
| PageMaterialID | int | Page material |
| LanguageID | int | Language for readable |
| Bonding | int | Binding type |
| DamageType | int | Damage school type |
| ContainerSlots | int | Bag slots if container |
| RequiredPVPMedal | int | Required PvP medal |
| RequiredPVPRank | int | Required PvP rank |
| InventoryType | int | Equipment slot |
| OverallQualityID | int | Item quality (rarity) |
| AmmunitionType | int | Ammo type |
| RequiredLevel | int | Level required to use |

## Relationships

- `ID` → `Item.ID`
- `RequiredSkill` → `SkillLine.ID`
- `ItemSet` → ItemSet table

## Notes

- Display_lang contains the item name
- Contains most item properties used by addons
- StatModifier arrays pair bonusStat (type) with bonusAmount (value)
