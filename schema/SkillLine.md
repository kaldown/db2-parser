# SkillLine

Profession and skill metadata.

## Columns

| Column | Type | Description |
|--------|------|-------------|
| DisplayName_lang | string | Localized skill name |
| AlternateVerb_lang | string | Alternate action verb |
| Description_lang | string | Skill description |
| HordeDisplayName_lang | string | Horde-specific name if different |
| NeutralDisplayName | string | Neutral faction name |
| ID | int | Primary key, skill line ID |
| CategoryID | int | Skill category |
| SpellIconFileID | int | Icon file reference |
| CanLink | int | Whether skill can be linked |
| ParentSkillLineID | int | Parent skill for specializations |
| ParentTierIndex | int | Tier within parent skill |
| Flags | int | Skill flags |
| SpellBookSpellID | int | Associated spell book entry |

## Relationships

- `ID` is referenced by SkillLineAbility.SkillLine

## Notes

- Key profession IDs:
  - 129 = First Aid
  - 164 = Blacksmithing
  - 165 = Leatherworking
  - 171 = Alchemy
  - 185 = Cooking
  - 186 = Mining
  - 197 = Tailoring
  - 202 = Engineering
  - 333 = Enchanting
  - 755 = Jewelcrafting
