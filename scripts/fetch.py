#!/usr/bin/env python3
"""Download DB2 CSV tables from wago.tools.

Usage:
    python fetch.py --version 2.5.5.65463 --tables Spell SpellName --output artifacts
"""

import argparse
import sys
import urllib.request
import urllib.error
from pathlib import Path


WAGO_BASE_URL = "https://wago.tools/db2"


def get_csv_url(table_name: str, version: str) -> str:
    """Generate wago.tools CSV download URL."""
    return f"{WAGO_BASE_URL}/{table_name}/csv?build={version}"


def download_table(table_name: str, version: str, output_dir: Path) -> bool:
    """Download a single table CSV.

    Returns True on success, False on failure.
    """
    url = get_csv_url(table_name, version)
    output_path = output_dir / f"{table_name}.csv"

    print(f"Fetching {table_name}.csv... ", end="", flush=True)

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "db2-parser/1.0"}
        )

        with urllib.request.urlopen(request, timeout=60) as response:
            content = response.read()

            # Check for empty response
            if not content or len(content) < 10:
                print("EMPTY")
                return False

            # Check for HTML error page
            if content.startswith(b"<!DOCTYPE") or content.startswith(b"<html"):
                print("NOT FOUND")
                return False

            # Write to file
            with open(output_path, "wb") as f:
                f.write(content)

            size_kb = len(content) / 1024
            print(f"done ({size_kb:.1f} KB)")
            return True

    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}")
        return False
    except urllib.error.URLError as e:
        print(f"ERROR: {e.reason}")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Download DB2 CSV tables from wago.tools")
    parser.add_argument("--version", required=True, help="Build version (e.g., 2.5.5.65463)")
    parser.add_argument("--tables", nargs="+", required=True, help="Table names to download")
    parser.add_argument("--output", type=Path, default=Path("artifacts"), help="Output directory")
    args = parser.parse_args()

    # Create versioned output directory
    version_dir = args.output / args.version
    version_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading to {version_dir}/")
    print()

    # Download each table
    results = {}
    for table in args.tables:
        results[table] = download_table(table, args.version, version_dir)

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
