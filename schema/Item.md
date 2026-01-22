# Item

Core item data including stats and equipment properties.

## Columns

| Column | Type | Description |
|--------|------|-------------|
| ID | int | Primary key, item ID |
| ClassID | int | Item class (weapon, armor, consumable, etc.) |
| SubclassID | int | Item subclass within class |
| Material | int | Material type for sounds |
| InventoryType | int | Equipment slot type |
| RequiredLevel | int | Level required to use |
| SheatheType | int | How item is sheathed |
| RandomSelect | int | Random enchantment pool |
| ItemRandomSuffixGroupID | int | Random suffix group |
| Sound_override_subclassID | int | Sound override |
| ScalingStatDistributionID | int | Stat scaling distribution |
| IconFileDataID | int | Icon file reference |
| ItemGroupSoundsID | int | Sound group |
| ContentTuningID | int | Content tuning reference |
| MaxDurability | int | Maximum durability |
| AmmunitionType | int | Ammo type if applicable |
| ScalingStatValue | int | Stat scaling value |
| DamageType_0 | int | Primary damage type |
| DamageType_1 | int | Secondary damage type |
| DamageType_2 | int | Tertiary damage type |
| DamageType_3 | int | Fourth damage type |
| DamageType_4 | int | Fifth damage type |
| Resistances_0 | int | Armor |
| Resistances_1 | int | Holy resistance |
| Resistances_2 | int | Fire resistance |
| Resistances_3 | int | Nature resistance |
| Resistances_4 | int | Frost resistance |
| Resistances_5 | int | Shadow resistance |
| Resistances_6 | int | Arcane resistance |
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

## Relationships

- `ID` is referenced by SpellEffect.EffectItemType, SpellReagents.Reagent_*

## Notes

- Item names are in ItemSparse.Display_lang, not this table
- Damage/resistance arrays support multiple damage types
