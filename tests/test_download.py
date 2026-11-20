import contextlib
import io
import tempfile
import unittest
import urllib.error
from pathlib import Path

from tests import _path  # noqa: F401
from tests.fakes import http_error

import fetch

CSV = b"ID,Name\n1,a\n"


def fetcher_for(outcomes: dict):
    """A fetcher keyed by table name: bytes are returned, exceptions raised."""

    def fetcher(url, timeout=60):
        table = url.split("/db2/")[1].split("/")[0]
        outcome = outcomes[table]
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome

    return fetcher


class DownloadTableTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def download(self, outcome):
        with contextlib.redirect_stdout(io.StringIO()):
            return fetch.download_table("T", "1.2.3.4", self.dir, fetcher=fetcher_for({"T": outcome}))

    def test_ok_writes_csv_and_no_tmp(self):
        self.assertEqual(self.download(CSV), fetch.OK)
        self.assertEqual((self.dir / "T.csv").read_bytes(), CSV)
        self.assertFalse((self.dir / "T.csv.tmp").exists())

    def test_http_400_is_missing(self):
        self.assertEqual(self.download(http_error(400)), fetch.MISSING)
        self.assertFalse((self.dir / "T.csv").exists())

    def test_other_4xx_is_failed(self):
        self.assertEqual(self.download(http_error(403)), fetch.FAILED)

    def test_empty_body_failed(self):
        self.assertEqual(self.download(b""), fetch.FAILED)

    def test_html_body_failed(self):
        self.assertEqual(self.download(b"<!DOCTYPE html><html></html>"), fetch.FAILED)

    def test_json_body_failed(self):
        self.assertEqual(self.download(b'{"errors":"Table not found."}'), fetch.FAILED)
        self.assertFalse((self.dir / "T.csv").exists())

    def test_failure_keeps_existing_csv(self):
        (self.dir / "T.csv").write_bytes(b"old")
        self.assertEqual(self.download(urllib.error.URLError("down")), fetch.FAILED)
        self.assertEqual((self.dir / "T.csv").read_bytes(), b"old")
        self.assertFalse((self.dir / "T.csv.tmp").exists())


class FetchTablesTests(unittest.TestCase):
    def run_fetch(self, outcomes, tables, optional):
        out = io.StringIO()
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(out):
            code = fetch.fetch_tables("1.2.3.4", tables, optional, Path(tmp), fetcher=fetcher_for(outcomes))
        return code, out.getvalue()

    def test_fetch_tables_required_missing_fails(self):
        code, out = self.run_fetch({"A": CSV, "B": http_error(400)}, ["A", "B"], [])
        self.assertEqual(code, 1)
        self.assertIn("NOT IN BUILD", out)

    def test_fetch_tables_optional_missing_ok(self):
        code, out = self.run_fetch({"A": CSV, "X": http_error(400)}, ["A"], ["X"])
        self.assertEqual(code, 0)
        self.assertIn("NOT IN BUILD", out)
        self.assertIn("optional", out)


if __name__ == "__main__":
    unittest.main()
