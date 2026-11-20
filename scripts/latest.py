#!/usr/bin/env python3
"""Find and fetch the latest build for an expansion, within one product.

Usage:
    python latest.py --expansion 1 --product wow_classic_era --tables Spell SpellName --output artifacts
    python latest.py --expansion 1 --list
"""

import argparse
import json
import sys
from pathlib import Path

# Import the sibling module no matter which directory the script is run from.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fetch import fetch_tables, http_get  # noqa: E402


WAGO_BUILDS_URL = "https://wago.tools/api/builds"


class AmbiguousProductError(Exception):
    """More than one product has builds for the requested major version."""

    def __init__(self, products: list[str]):
        super().__init__(", ".join(products))
        self.products = products


class NoBuildsError(Exception):
    """No build matches; `available` lists the products that do have builds for the major."""

    def __init__(self, available: list[str]):
        super().__init__(", ".join(available))
        self.available = available


def get_all_builds() -> dict:
    """Fetch all builds from wago.tools API: {product: [{version, created_at, ...}]}."""
    return json.loads(http_get(WAGO_BUILDS_URL, timeout=30).decode("utf-8"))


def version_key(v: str) -> tuple[int, ...]:
    """Sort key for X.Y.Z.BUILD versions. Malformed versions sort lowest."""
    try:
        return tuple(int(p) for p in v.split("."))
    except ValueError:
        return (-1,)


def _builds_for_major(builds: dict, major: int) -> dict[str, list[dict]]:
    prefix = f"{major}."
    found: dict[str, list[dict]] = {}
    for product, product_builds in builds.items():
        matching = [b for b in product_builds if str(b.get("version", "")).startswith(prefix)]
        if matching:
            found[product] = matching
    return found


def products_for_major(builds: dict, major: int) -> list[str]:
    """Sorted product keys that have at least one <major>.x build."""
    return sorted(_builds_for_major(builds, major))


def find_latest_for_expansion(builds: dict, expansion: int, product: str | None = None) -> tuple[str, str]:
    """Return (version, product) of the newest <expansion>.x build.

    With `product`, only that product's builds count. Without it, the answer is
    only given when exactly one product has builds for the major: since several
    games now share a major version (e.g. Classic Era and WoW Forever are both
    1.x), a cross-product max would silently fetch the wrong game.
    """
    by_product = _builds_for_major(builds, expansion)
    if product is not None:
        if product not in by_product:
            raise NoBuildsError(sorted(by_product))
        candidates = {product: by_product[product]}
    elif len(by_product) > 1:
        raise AmbiguousProductError(sorted(by_product))
    elif not by_product:
        raise NoBuildsError([])
    else:
        candidates = by_product

    (chosen_product, product_builds), = candidates.items()
    newest = max((b["version"] for b in product_builds), key=version_key)
    return newest, chosen_product


def list_builds(builds: dict, major: int, product: str | None = None) -> list[tuple[str, str, str]]:
    """(product, version, created_at) rows, by product then newest version first."""
    rows = []
    for name, product_builds in sorted(_builds_for_major(builds, major).items()):
        if product is not None and name != product:
            continue
        for b in sorted(product_builds, key=lambda b: version_key(b["version"]), reverse=True):
            rows.append((name, b["version"], str(b.get("created_at", ""))))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Find and fetch latest build for expansion")
    parser.add_argument("--expansion", type=int, required=True, help="Major version (1=Classic Era/Forever, 2=TBC, 3=WotLK, ...)")
    parser.add_argument("--product", help="wago.tools product key (e.g. wow_classic_era, wowf)")
    parser.add_argument("--list", action="store_true", help="List matching builds and exit without fetching")
    parser.add_argument("--tables", nargs="+", help="Required table names")
    parser.add_argument("--optional-tables", nargs="*", default=[], help="Tables fetched best-effort")
    parser.add_argument("--output", type=Path, default=Path("artifacts"), help="Output directory")
    args = parser.parse_args()

    if not args.list and not args.tables:
        parser.error("--tables is required unless --list is given")

    try:
        builds = get_all_builds()
    except Exception as e:
        print(f"Error fetching builds: {e}", file=sys.stderr)
        return 1

    n = args.expansion
    if args.list:
        rows = list_builds(builds, n, args.product)
        if not rows:
            print(f"No builds for expansion {n}" + (f" in product {args.product}" if args.product else ""),
                  file=sys.stderr)
            return 1
        for product, version, created in rows:
            print(f"{product:<22} {version:<16} {created}")
        return 0

    print(f"Finding latest build for expansion {n}...")
    try:
        version, product = find_latest_for_expansion(builds, n, args.product)
    except AmbiguousProductError as e:
        print(f"Expansion {n} has builds in several products: {', '.join(e.products)}. "
              f"Pass PRODUCT=<key> (see 'make list-builds EXPANSION={n}').", file=sys.stderr)
        return 1
    except NoBuildsError as e:
        where = f" in product {args.product}" if args.product else ""
        available = ", ".join(e.available) or "none"
        print(f"No builds for expansion {n}{where}. Products with {n}.x builds: {available}", file=sys.stderr)
        return 1

    print(f"Latest: {version} (product {product})")
    print()
    return fetch_tables(version, args.tables, args.optional_tables, args.output)


if __name__ == "__main__":
    sys.exit(main())
