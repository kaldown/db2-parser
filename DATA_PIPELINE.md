# Data Pipeline Runbook - fetch, enrich, transform, consume

This is the canonical operational runbook for the crafting-data pipeline: how to pull raw
game data, enrich it, transform it into the Lua tables CraftLib serves, and - importantly -
how to **drive it to full completion even after a partial failure**.

It is anchored in db2-parser because that is the data foundation every downstream repo depends
on. Note the boundary: db2-parser owns only **Stage 1 (fetch)**; the enrich/transform code
(**Stages 2-3**) lives in **CraftLib's** `scripts/` (db2-parser is consumed as CraftLib's
submodule at `vendor/db2-parser`, so from CraftLib those are `scripts/*.py` and this repo is
`vendor/db2-parser/`). This runbook documents the whole workflow; it does not move any code.

## Network prerequisite

The pipeline reaches two external hosts. In a sandboxed session, allow them first (a blocked
request returns HTTP 403 with a "network policy" body):

```
sbx policy allow network wago.tools,www.wowhead.com
```

`wago.tools` serves the DB2 CSVs; `www.wowhead.com` serves difficulty colors + source types.

## The three stages

| Stage | What | Code | Output |
|-------|------|------|--------|
| 1. Fetch | Download DB2 table CSVs for one pinned build | db2-parser `scripts/fetch.py` (via `make fetch`/`make latest`) | `artifacts/<build>/*.csv` (cached) |
| 2. Extract + enrich | Join CSVs into per-recipe sources; fill orange/green + vendor/drop + seasonId from Wowhead | CraftLib `scripts/extract_db2_sources.py`, `scripts/fetch_wowhead_sources.py` | `Data/Sources/<Bucket>/<Prof>.json` |
| 3. Transform | Emit the consumable Lua (CraftLib's schema) | CraftLib `scripts/generate_recipes.py` | `Data/<Bucket>/<Prof>/Recipes.lua` |

Build pinning is **per-product** (never mix): Classic Era/SoD `wow_classic_era 1.15.8.x`,
TBC `wow_anniversary/wow_classic 2.5.5.x`, WotLK `wow_classic 3.4.x`. `make latest EXPANSION=n`
takes a global max across products and is **NOT product-aware** - it can return a wrong-product
build (e.g. a `wow_classic_titan 3.80.x` for `EXPANSION=3` instead of WotLK `3.4.x`). Always
confirm the resolved build is the product you want, and pin an explicit `VERSION` for
reproducibility.

## Happy path (one continuous-tier bucket, e.g. WotLK)

Run from the CraftLib repo root:

```bash
make -C vendor/db2-parser latest EXPANSION=3          # Stage 1: resolve+fetch the 3.4.x build
# per profession (or use the make tier target wotlk-all):
python3 scripts/extract_db2_sources.py  --version <build> --profession Tailoring --expansion wotlk
python3 scripts/fetch_wowhead_sources.py --profession Tailoring --expansion wotlk
python3 scripts/assert_no_pending.py    Data/Sources/WotLK/Tailoring.json
python3 scripts/generate_recipes.py     --version <build> --expansion 3 \
        --data-dir vendor/db2-parser/artifacts --profession Tailoring
luac5.1 -p Data/WotLK/Tailoring/Recipes.lua
```

## Error handling (verified behavior, by stage)

**Stage 1 - wago (`fetch.py`):** minimal by design. On `HTTPError`/`URLError`/timeout it prints
the code/reason and returns False (**no retry, no backoff, bare UA**); empty (<10 bytes) or an
HTML error page is rejected as EMPTY/NOT FOUND. `make` exits non-zero and names the failed
tables. There is no partial-file corruption risk (each table is written whole). **Recovery:
re-run `make fetch VERSION=<build>`** - already-fetched tables are simply rewritten; the
`artifacts/<build>/` cache fills in. If a build 404s, wago may have retired it - re-resolve
with `make latest EXPANSION=n` and pin the new build.

**Stage 2 - Wowhead (`fetch_wowhead_sources.py`):** hardened.
- Full CloudFront-WAF-clearing browser headers (UA + Accept-Language + Referer + Sec-Fetch-* +
  gzip). A bare UA 403s - do not strip the headers.
- `_fetch_page(retries=3)`: on transient **403/503** it sleeps `2*(attempt+1)` (2s, 4s) and
  retries up to 3x; any other error prints to stderr and returns None (gives up on that page).
- A page that yields nothing -> that recipe is counted `failed`, **skipped, and the run
  continues** (exit code 2 if any failed). A spell-data blob that won't parse returns failure
  with **no fallback-guess** (deliberate: report failure, never fabricate).
- Throttle: `time.sleep(0.5)` between per-spell fetches; the Make tier loop adds `sleep 2`
  between professions. WotLK/Vanilla use the 1-request-per-profession **listview** path; TBC
  uses the per-spell path.

**Stage 3 + gates - the correctness backstop:** `assert_no_pending.py` fails if any source is
still PENDING; `generate_recipes.py` **raises** on a PENDING source, a VENDOR entry missing
cost/itemId, or an unknown expansion/source type; `luac5.1 -p` rejects malformed Lua. These
gates make it **impossible to "complete" with gaps** - a fetch hole becomes a loud failure, not
a silent false value. This is the data-truth mantra enforced mechanically.

## Resume to FULL completion after a partial failure (the important part)

The pipeline is **idempotent and resumable** at profession + recipe granularity. To finish a
run that died partway (network drop, WAF block, killed process):

1. **Re-run the same profession's fetch.** `fetch_wowhead_sources.py` calls `_needs_fetch`,
   which **skips any recipe that already has WOWHEAD difficulty and a non-PENDING source**, and
   the per-spell path **saves progress every 10 recipes**. So a re-run only re-fetches the gaps.
   (Listview mode writes the file once at the end and is effectively atomic per profession - a
   failed single request leaves the file untouched, so just re-run it; it is one request.)
2. **Repeat until the run reports `failed=0`** and `assert_no_pending.py` exits 0. That pair is
   the completion criterion for a bucket.
3. **Persistent WAF block (CloudFront cold-start / rate):** wait a minute, then fetch **one
   profession at a time** with the default throttle; the 403/503 backoff usually clears it. Do
   not remove the headers or hammer it.
4. **Recipes Wowhead genuinely lacks** (content removed from the game / never on Wowhead) will
   never resolve and show as persistent `no_colors`/`failed`. These are the *only* legitimate
   permanent gaps: add their spell ids to `Data/Sources/removed_recipes.json` (or
   `removed_recipes.sod.json`) so `generate_recipes.py` filters them. Never instead inject a
   fake source/difficulty to clear the gate.
5. **Then transform:** once a bucket's sources pass `assert_no_pending`, run
   `generate_recipes.py` and `luac5.1 -p`. Generate is pure (no network) and rerunnable.

Completion is reached when, for every profession in the bucket: fetch `failed=0`,
`assert_no_pending` exits 0, `generate` succeeds, `luac5.1 -p` is clean.

> **WARNING - `make tbc-retag` is UNSAFE to run as-is.** Re-extracting TBC strips the
> Wowhead-verified difficulty and the per-spell re-fetch 403s under volume, silently losing
> recipes. To re-tag an already-complete bucket's `profile=`, edit the generated files
> surgically (or fix the tier target to preserve WOWHEAD entries) rather than regenerating.

## The consumable schema (Stage 3 output)

`generate_recipes.py` emits `Data/<Bucket>/<Prof>/Recipes.lua`, which calls
`CraftLib:RegisterProfession(key, {...})`. Per-recipe shape (authoritative copy in CraftLib's
`SCHEMA.md`):

```
recipe = {
  id, name, itemId?,            -- itemId nil for enchant-on-gear
  skillRequired,
  skillRange = { orange, yellow, green, gray },
  reagents = { { itemId, name, count }, ... },
  source   = { type, certainty, itemId?, cost?, factionId?, ... },
  expansion = C.EXPANSION.<TIER>,   -- per-recipe era, from skill range
}
-- registration table also carries: id, name, expansion, profile, milestones, recipes
```

`profile` is the runtime load-guard key (`VANILLA`/`TBC`/`WOTLK`/`SOD`); only the file whose
`profile` matches the running client registers. Difficulty truth: yellow+gray from DB2,
orange+green+seasonId from Wowhead.

## Known limitations (improvements are tracked in the backlogs, not done inline)

- Stage 1 (`fetch.py`) has no retry/backoff and a bare UA - a transient wago failure needs a
  manual re-run. (db2-parser backlog: harden HTTP + a resumable driver.)
- `make latest` is not product-aware (can pick the wrong product for `EXPANSION=3`).
- There is no single "fetch-until-complete" driver that auto-retries failed professions until
  the gates pass; today that loop is manual (steps 1-2 above). (CraftLib backlog.)
- The resumable per-spell checkpoint is coarse (every 10); the SoD trainer-verifier has a
  stronger backoff ladder + `.fetch_state/` checkpoint that could be generalized to all tiers.
  (CraftLib backlog.)
- `make tbc-retag` is unsafe (see warning above). (CraftLib backlog.)

See `README.md` (usage), `schema/<Table>.md` (CSV column contracts), and CraftLib's
`docs/development/` + `SCHEMA.md` for stage-specific detail.
