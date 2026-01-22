#!/usr/bin/env python3
"""Validate schema documentation matches downloaded CSV columns.

Usage:
    python validate.py --version 2.5.5.65463 --schema schema --artifacts artifacts
"""

import argparse
import csv
import re
import sys
from pathlib import Path


def get_csv_columns(csv_path: Path) -> list[str]:
    """Read column names from CSV header row."""
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        return header


def get_schema_columns(schema_path: Path) -> list[str]:
    """Parse column names from schema markdown file.

    Expects format:
    | Column | Type | Description |
    |--------|------|-------------|
    | ID | int | Primary key |
    """
    columns = []

    with open(schema_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find table rows (lines starting with |)
    in_columns_section = False
    for line in content.split("\n"):
        line = line.strip()

        # Start of Columns section
        if line == "## Columns":
            in_columns_section = True
            continue

        # End of Columns section (next heading)
        if in_columns_section and line.startswith("## "):
            break

        # Skip non-table lines
        if not in_columns_section or not line.startswith("|"):
            continue

        # Skip header and separator rows
        if "Column" in line and "Type" in line:
            continue
        if re.match(r"^\|[-:\s|]+\|$", line):
            continue

        # Extract first column (the column name)
        parts = line.split("|")
        if len(parts) >= 2:
            column_name = parts[1].strip()
            if column_name and not column_name.startswith("-"):
                columns.append(column_name)

    return columns


def validate_table(table_name: str, schema_dir: Path, artifacts_dir: Path, version: str) -> tuple[bool, str]:
    """Validate a single table's schema against CSV.

    Returns (is_valid, message).
    """
    schema_path = schema_dir / f"{table_name}.md"
    csv_path = artifacts_dir / version / f"{table_name}.csv"

    # Check files exist
    if not schema_path.exists():
        return False, f"schema not found: {schema_path}"

    if not csv_path.exists():
        return False, f"CSV not found: {csv_path}"

    # Get columns
    try:
        schema_columns = set(get_schema_columns(schema_path))
    except Exception as e:
        return False, f"error parsing schema: {e}"

    try:
        csv_columns = set(get_csv_columns(csv_path))
    except Exception as e:
        return False, f"error parsing CSV: {e}"

    # Compare
    missing = schema_columns - csv_columns  # In schema but not CSV
    extra = csv_columns - schema_columns    # In CSV but not schema

    if not missing and not extra:
        return True, "OK"

    parts = []
    if missing:
        parts.append(f"missing from CSV: {', '.join(sorted(missing))}")
    if extra:
        parts.append(f"extra in CSV: {', '.join(sorted(extra))}")

    return False, "MISMATCH - " + "; ".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate schema matches downloaded CSVs")
    parser.add_argument("--version", required=True, help="Build version to validate")
    parser.add_argument("--schema", type=Path, default=Path("schema"), help="Schema directory")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"), help="Artifacts directory")
    args = parser.parse_args()

    # Find all schema files
    schema_files = list(args.schema.glob("*.md"))
    if not schema_files:
        print(f"No schema files found in {args.schema}", file=sys.stderr)
        return 1

    print(f"Validating against version {args.version}")
    print()

    all_valid = True
    for schema_file in sorted(schema_files):
        table_name = schema_file.stem
        is_valid, message = validate_table(table_name, args.schema, args.artifacts, args.version)

        status = "OK" if is_valid else "FAIL"
        print(f"{table_name}: {message}")

        if not is_valid:
            all_valid = False

    print()
    if all_valid:
        print("All schemas valid")
        return 0
    else:
        print("Schema validation failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
