# SpellEffect

Spell effects including crafted item output.

## Columns

| Column | Type | Description |
|--------|------|-------------|
| ID | int | Primary key |
| DifficultyID | int | Difficulty modifier |
| EffectIndex | int | Effect index within spell |
| Effect | int | Effect type ID |
| EffectAmplitude | float | Effect amplitude |
| EffectAttributes | int | Effect attributes flags |
| EffectAura | int | Aura type if applicable |
| EffectAuraPeriod | int | Aura tick period |
| EffectBasePoints | int | Base points (yield - 1 for crafting) |
| EffectBonusCoefficient | float | Bonus coefficient |
| EffectChainAmplitude | float | Chain effect amplitude |
| EffectChainTargets | int | Number of chain targets |
| EffectDieSides | int | Random range (yield = BasePoints + DieSides) |
| EffectItemType | int | Crafted item ID |
| EffectMechanic | int | Effect mechanic type |
| EffectPointsPerResource | float | Points per resource |
| EffectPos_facing | float | Position facing |
| EffectRealPointsPerLevel | float | Points per level |
| EffectTriggerSpell | int | Triggered spell ID |
| BonusCoefficientFromAP | float | Attack power coefficient |
| PvpMultiplier | float | PvP damage multiplier |
| Coefficient | float | General coefficient |
| Variance | float | Variance modifier |
| ResourceCoefficient | float | Resource coefficient |
| GroupSizeBasePointsCoefficient | float | Group size modifier |
| EffectBasePointsF | float | Base points (float) |
| EffectMiscValue_0 | int | Misc value 1 |
| EffectMiscValue_1 | int | Misc value 2 |
| EffectRadiusIndex_0 | int | Radius index 1 |
| EffectRadiusIndex_1 | int | Radius index 2 |
| EffectSpellClassMask_0 | int | Spell class mask 1 |
| EffectSpellClassMask_1 | int | Spell class mask 2 |
| EffectSpellClassMask_2 | int | Spell class mask 3 |
| EffectSpellClassMask_3 | int | Spell class mask 4 |
| ImplicitTarget_0 | int | Implicit target 1 |
| ImplicitTarget_1 | int | Implicit target 2 |
| SpellID | int | Parent spell ID |

## Relationships

- `SpellID` → `Spell.ID`
- `EffectItemType` → `Item.ID` (crafted item)
- `EffectTriggerSpell` → `Spell.ID`

## Notes

- For crafting recipes, look for effects where EffectItemType > 0
- Yield calculation: EffectBasePoints + EffectDieSides
- Multiple effects per spell possible (different EffectIndex)
