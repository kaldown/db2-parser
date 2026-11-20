#!/usr/bin/env python3
"""Download DB2 CSV tables from wago.tools.

Usage:
    python fetch.py --version 2.5.5.65463 --tables Spell SpellName \
        [--optional-tables ItemXItemEffect] --output artifacts
"""

import argparse
import gzip
import http.client
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


WAGO_BASE_URL = "https://wago.tools/db2"

# A full browser-like header set. wago.tools accepts a bare User-Agent today, but
# CDN-fronted WoW sites have started rejecting bare clients with HTTP 403, so we
# send what a browser sends rather than wait for that to happen here.
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/csv,application/json;q=0.9,text/html;q=0.8,*/*;q=0.5",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip",
}

# Errors worth another attempt: the network, not the request, was the problem.
# HTTPError is a URLError subclass and is handled separately (4xx never retried).
_TRANSIENT_ERRORS = (urllib.error.URLError, TimeoutError, ConnectionError, http.client.HTTPException)


def http_get(
    url: str,
    timeout: float = 60,
    *,
    opener=urllib.request.urlopen,
    sleep=time.sleep,
    attempts: int = 3,
) -> bytes:
    """GET a URL with browser headers, gzip decoding and retry.

    Retries network errors and HTTP 5xx with 2 s, 4 s, ... backoff. An HTTP 4xx
    is the server's answer about this request, so it is raised at once.
    Redirects are followed by urllib. Returns the decoded body.
    """
    for attempt in range(attempts):
        last_attempt = attempt == attempts - 1
        request = urllib.request.Request(url, headers=BROWSER_HEADERS)
        try:
            with opener(request, timeout=timeout) as response:
                body = response.read()
                if (response.headers.get("Content-Encoding") or "").lower() == "gzip":
                    body = gzip.decompress(body)
                return body
        except urllib.error.HTTPError as e:
            if e.code < 500 or last_attempt:
                raise
        except _TRANSIENT_ERRORS:
            if last_attempt:
                raise
        sleep(2 * 2 ** attempt)
    raise AssertionError("unreachable")  # loop always returns or raises


def get_csv_url(table_name: str, version: str) -> str:
    """Generate wago.tools CSV download URL."""
    return f"{WAGO_BASE_URL}/{table_name}/csv?build={version}"


# download_table outcomes. MISSING means wago.tools says the table does not exist
# in that build (HTTP 400); FAILED is anything else that left us without a CSV.
OK = "ok"
MISSING = "missing"
FAILED = "failed"


def _not_csv_reason(content: bytes) -> str | None:
    """Return why a response body is not a CSV, or None if it looks like one."""
    if not content or len(content) < 10:
        return "EMPTY"
    head = content.lstrip()[:16].lower()
    if head.startswith(b"<!doctype") or head.startswith(b"<html"):
        return "NOT CSV (HTML)"
    # wago.tools answers errors as JSON ({"errors": ...}); never save that as data.
    if head.startswith(b"{") or head.startswith(b"["):
        return "NOT CSV (JSON)"
    return None


def download_table(table_name: str, version: str, output_dir: Path, *, fetcher=http_get) -> str:
    """Download one table CSV into output_dir. Returns OK, MISSING or FAILED.

    The body goes to <Table>.csv.tmp first and is renamed into place, so an
    interrupted or rejected download never truncates or replaces a good CSV.
    """
    url = get_csv_url(table_name, version)
    output_path = output_dir / f"{table_name}.csv"
    tmp_path = output_dir / f"{table_name}.csv.tmp"

    print(f"Fetching {table_name}.csv... ", end="", flush=True)

    try:
        content = fetcher(url, timeout=60)
        reason = _not_csv_reason(content)
        if reason:
            print(reason, end="")
            return FAILED
        tmp_path.write_bytes(content)
        os.replace(tmp_path, output_path)
        print(f"done ({len(content) / 1024:.1f} KB)", end="")
        return OK
    except urllib.error.HTTPError as e:
        if e.code == 400:
            print("NOT IN BUILD", end="")
            return MISSING
        print(f"HTTP {e.code}", end="")
        return FAILED
    except urllib.error.URLError as e:
        print(f"ERROR: {e.reason}", end="")
        return FAILED
    except Exception as e:
        print(f"ERROR: {e}", end="")
        return FAILED
    finally:
        tmp_path.unlink(missing_ok=True)


def fetch_tables(
    version: str,
    tables: list[str],
    optional: list[str],
    output_root: Path,
    *,
    fetcher=http_get,
) -> int:
    """Download required and optional tables for one build into output_root/<version>/.

    Returns the process exit code: 1 if any required table is not OK or any
    optional table FAILED, else 0. An optional table is skipped only when the
    build does not have it (MISSING); any other failure would leave the run
    green with the table silently absent or stale.
    """
    version_dir = output_root / version
    version_dir.mkdir(parents=True, exist_ok=True)
    print(f"Downloading to {version_dir}/")
    print()

    results: dict[str, str] = {}
    optional_set = set(optional)
    for table in list(tables) + [t for t in optional if t not in tables]:
        results[table] = download_table(table, version, version_dir, fetcher=fetcher)
        is_optional = table in optional_set and table not in tables
        print(" (optional, skipped)" if is_optional and results[table] == MISSING else "")

    def label(table: str) -> str:
        return f"{table} (optional)" if table in optional_set and table not in tables else table

    print()
    ok = sum(1 for status in results.values() if status == OK)
    print(f"Downloaded {ok}/{len(results)} tables")
    missing = [label(t) for t, status in results.items() if status == MISSING]
    failed = [label(t) for t, status in results.items() if status == FAILED]
    if missing:
        print(f"Not in build: {', '.join(missing)}")
    if failed:
        print(f"Failed: {', '.join(failed)}")

    required_bad = [t for t in tables if results[t] != OK]
    optional_failed = [t for t, status in results.items() if t not in tables and status == FAILED]
    return 1 if required_bad or optional_failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Download DB2 CSV tables from wago.tools")
    parser.add_argument("--version", required=True, help="Build version (e.g., 2.5.5.65463)")
    parser.add_argument("--tables", nargs="+", required=True, help="Required table names")
    parser.add_argument("--optional-tables", nargs="*", default=[],
                        help="Tables fetched best-effort (absent in some builds)")
    parser.add_argument("--output", type=Path, default=Path("artifacts"), help="Output directory")
    args = parser.parse_args()
    return fetch_tables(args.version, args.tables, args.optional_tables, args.output)


if __name__ == "__main__":
    sys.exit(main())
