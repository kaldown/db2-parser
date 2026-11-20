import tempfile
import unittest
from pathlib import Path

from tests import _path  # noqa: F401

import validate

SCHEMA = """# T

## Columns

| Column | Type | Description |
|--------|------|-------------|
| ID | int | Primary key |
| Name | string | Name |

## Notes

| Column | Type | Description |
|--------|------|-------------|
| Foo | x | not a column of T |
"""


class ValidateTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.schema_dir = root / "schema"
        self.artifacts = root / "artifacts"
        self.schema_dir.mkdir()
        (self.artifacts / "1.2.3.4").mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, schema: str, header: str | None):
        (self.schema_dir / "T.md").write_text(schema)
        if header is not None:
            (self.artifacts / "1.2.3.4" / "T.csv").write_text(header + "\n1,a\n")

    def check(self, **kwargs):
        return validate.validate_table("T", self.schema_dir, self.artifacts, "1.2.3.4", **kwargs)

    def test_parses_columns_section_only(self):
        self.write(SCHEMA, None)
        self.assertEqual(validate.get_schema_columns(self.schema_dir / "T.md"), ["ID", "Name"])

    def test_match_ok(self):
        self.write(SCHEMA, "ID,Name")
        self.assertEqual(self.check(), (True, "OK"))

    def test_mismatch_lists_both_sides(self):
        self.write(SCHEMA.replace("| Name | string | Name |", "| Gone | int | x |"), "ID,Extra")
        ok, message = self.check()
        self.assertFalse(ok)
        self.assertIn("missing from CSV: Gone", message)
        self.assertIn("extra in CSV: Extra", message)

    def test_optional_absent_is_skipped(self):
        self.write(SCHEMA, None)
        self.assertEqual(self.check(optional=True), (True, "SKIPPED (optional, not in build)"))

    def test_required_absent_fails(self):
        self.write(SCHEMA, None)
        ok, message = self.check(optional=False)
        self.assertFalse(ok)
        self.assertTrue(message.startswith("CSV not found"))


if __name__ == "__main__":
    unittest.main()
