#!/usr/bin/env python3
"""Find and fetch the latest build for an expansion.

Usage:
    python latest.py --expansion 2 --tables Spell SpellName --output artifacts
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path


WAGO_BUILDS_URL = "https://wago.tools/api/builds"


def get_all_builds() -> dict:
    """Fetch all builds from wago.tools API."""
    request = urllib.request.Request(
        WAGO_BUILDS_URL,
        headers={"User-Agent": "db2-parser/1.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def find_latest_for_expansion(builds: dict, expansion: int) -> str | None:
    """Find the latest version matching expansion.x.x.x pattern.

    Searches all products for versions starting with the expansion number.
    Returns the highest version found.
    """
    matching_versions = []

    for product, product_builds in builds.items():
        for build in product_builds:
            version = build.get("version", "")
            # Check if version starts with expansion number
            if version.startswith(f"{expansion}."):
                matching_versions.append(version)

    if not matching_versions:
        return None

    # Sort versions and return the latest
    # Version format: X.X.X.XXXXX - sort by parts
    def version_key(v):
        parts = v.split(".")
        return tuple(int(p) for p in parts)

    matching_versions.sort(key=version_key, reverse=True)
    return matching_versions[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="Find and fetch latest build for expansion")
    parser.add_argument("--expansion", type=int, required=True, help="Expansion number (2=TBC, 3=WotLK, etc.)")
    parser.add_argument("--tables", nargs="+", required=True, help="Table names to download")
    parser.add_argument("--output", type=Path, default=Path("artifacts"), help="Output directory")
    args = parser.parse_args()

    print(f"Finding latest build for expansion {args.expansion}...")

    try:
        builds = get_all_builds()
    except Exception as e:
        print(f"Error fetching builds: {e}", file=sys.stderr)
        return 1

    version = find_latest_for_expansion(builds, args.expansion)

    if not version:
        print(f"No builds found for expansion {args.expansion}", file=sys.stderr)
        return 1

    print(f"Latest: {version}")
    print()

    # Import and call fetch logic
    from fetch import download_table

    # Create versioned output directory
    version_dir = args.output / version
    version_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading to {version_dir}/")
    print()

    # Download each table
    results = {}
    for table in args.tables:
        results[table] = download_table(table, version, version_dir)

    # Summary
    print()
    success = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"Downloaded {success}/{total} tables")

    if success < total:
        failed = [k for k, v in results.items() if not v]
        print(f"Failed: {', '.join(failed)}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
