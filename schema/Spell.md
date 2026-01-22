# Spell

Core spell data including descriptions and subtexts.

## Columns

| Column | Type | Description |
|--------|------|-------------|
| ID | int | Primary key, spell ID |
| NameSubtext_lang | string | Spell subtext (e.g., "Rank 2") |
| Description_lang | string | Full spell description |
| AuraDescription_lang | string | Aura/buff description |

## Relationships

- `ID` is referenced by SpellName, SpellReagents, SpellEffect, SkillLineAbility

## Notes

- Spell names are in SpellName table, not here
- Use SpellName.Name_lang for display names
