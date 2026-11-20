import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests import _path  # noqa: F401

import latest

BUILDS = {
    "wow_classic_era": [
        {"version": "1.15.8.67156", "created_at": "2025-01-01"},
        {"version": "1.15.9.70576", "created_at": "2026-10-01"},
    ],
    "wowf": [{"version": "1.60.1.71037", "created_at": "2026-11-01"}],
    "wow_cn_beta": [{"version": "1.60.1.70450", "created_at": "2026-10-15"}],
    "wow_anniversary": [{"version": "2.5.5.65895", "created_at": "2025-06-01"}],
}
EXPANSION_1 = ["wow_classic_era", "wow_cn_beta", "wowf"]


class LatestTests(unittest.TestCase):
    def test_version_key_numeric_order(self):
        self.assertGreater(latest.version_key("1.15.10.1"), latest.version_key("1.15.9.99999"))
        self.assertLess(latest.version_key("x.y"), latest.version_key("0.0.0.1"))

    def test_product_filter_era(self):
        self.assertEqual(latest.find_latest_for_expansion(BUILDS, 1, "wow_classic_era"),
                         ("1.15.9.70576", "wow_classic_era"))

    def test_product_filter_forever(self):
        self.assertEqual(latest.find_latest_for_expansion(BUILDS, 1, "wowf"), ("1.60.1.71037", "wowf"))

    def test_ambiguous_without_product(self):
        with self.assertRaises(latest.AmbiguousProductError) as ctx:
            latest.find_latest_for_expansion(BUILDS, 1)
        self.assertEqual(ctx.exception.products, EXPANSION_1)

    def test_single_product_without_product(self):
        self.assertEqual(latest.find_latest_for_expansion(BUILDS, 2), ("2.5.5.65895", "wow_anniversary"))

    def test_unknown_product(self):
        with self.assertRaises(latest.NoBuildsError) as ctx:
            latest.find_latest_for_expansion(BUILDS, 1, "wow_classic_eraa")
        self.assertEqual(ctx.exception.available, EXPANSION_1)

    def test_no_builds_for_major(self):
        with self.assertRaises(latest.NoBuildsError) as ctx:
            latest.find_latest_for_expansion(BUILDS, 9)
        self.assertEqual(ctx.exception.available, [])

    def test_list_builds(self):
        rows = latest.list_builds(BUILDS, 1, "wow_classic_era")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ("wow_classic_era", "1.15.9.70576", "2026-10-01"))

    def test_import_from_other_cwd(self):
        script = Path(_path.SCRIPTS) / "latest.py"
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(script), "--help"], cwd=tmp,
                                    capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
