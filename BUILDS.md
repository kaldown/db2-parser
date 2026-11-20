# Pinned builds

The builds the downstream data is generated from. `artifacts/` is not committed, so this file is
what lets a fresh clone rebuild the same cache (see "Rebuild the cache" in `README.md`).

| Product | Version | Used for | Fetched | Tables absent |
|---------|---------|----------|---------|---------------|
| `wow_classic_era` | `1.15.8.67156` | Vanilla, Season of Discovery | 2026-11-20 | `ItemXItemEffect` |
| `wow_anniversary` | `2.5.5.65895` | TBC | 2026-11-20 | `ItemXItemEffect` |
| `wow_classic` | `3.4.5.63697` | WotLK | 2026-11-20 | `ItemXItemEffect` |
| `wow_classic_titan` | `3.80.1.68318` | Titan (no dataset of its own yet; uses WotLK) | 2026-11-20 | `ItemXItemEffect` |
| `wowf` | `1.60.1.71037` | WoW Forever (planned) | 2026-11-20 | none |

"Tables absent" lists tables of the default set (`make list-tables`) that wago.tools reports as
not existing in that build (HTTP 400). Only optional tables may be absent; a missing required
table fails the fetch.

## Changing a pin

Pins move only on purpose, never as a side effect of `make latest`. Newer builds already exist
for some products (on 2026-11-20: `wow_classic_era 1.15.9.70576`, `wow_anniversary 2.5.6.70577`,
`wow_classic_titan 3.80.2.70522`). To move a pin:

1. `make list-builds EXPANSION=<n> PRODUCT=<product>` to see what is available.
2. `make fetch VERSION=<new>` and `make validate VERSION=<new>`. Validate is advisory for now:
   the `schema/*.md` column lists follow `1.15.8.67156`, so other builds report the column
   differences listed under each schema's "Build differences" (and, for WoW Forever, more
   tables than those list). Read the mismatches; do not expect a clean pass.
3. Update the row above (version, date, absent tables) in the same commit as the data that
   was regenerated from it.

Several games share a major version (`1.x` is Classic Era, WoW Forever, and others), so always
name the product: `make latest EXPANSION=1 PRODUCT=wow_classic_era`.
