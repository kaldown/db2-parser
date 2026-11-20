#!/usr/bin/env python3
"""Download DB2 CSV tables from wago.tools.

Usage:
    python fetch.py --version 2.5.5.65463 --tables Spell SpellName --output artifacts
"""

import argparse
import gzip
import http.client
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
