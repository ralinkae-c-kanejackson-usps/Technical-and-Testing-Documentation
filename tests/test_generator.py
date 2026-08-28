import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import generate_deliverables as generator  # noqa: E402


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples/usps/input.json").read_text())

    def test_validates_all_required_categories(self):
        data = dict(self.data)
        data["referenced_tables"] = []
        with self.assertRaisesRegex(ValueError, "referenced_tables"):
            generator.validate_input(data)
        for field in generator.NARRATIVE_FIELDS:
            data = dict(self.data)
            data[field] = ""
            with self.assertRaisesRegex(ValueError, field):
                generator.validate_input(data)

    def test_document_maps_template_and_enforces_parameterized_crid_filter(self):
        document = generator.technical_document(generator.validate_input(self.data))
        for section in generator.TEMPLATE_SECTIONS:
            self.assertIn(section, document)
        self.assertIn("WHERE crid = :crid", document)
        sql_example = document.split("```sql\n", 1)[1].split("\n```", 1)[0]
        self.assertNotIn("SELECT *", sql_example)
        self.assertIn("SELECT crid, <approved_column_1>", sql_example)
        self.assertIn("TBD", document)

    def test_cli_creates_both_deliverables(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/generate_deliverables.py"),
                 "--input", str(ROOT / "examples/usps/input.json"),
                 "--output", directory],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            output = Path(directory)
            self.assertTrue((output / "technical-documentation.md").is_file())
            self.assertTrue((output / "test-plan.md").is_file())

    def test_test_plan_includes_executable_crid_isolation_contract(self):
        plan = generator.test_plan(generator.validate_input(self.data))
        self.assertIn("Cross-CRID isolation", plan)
        self.assertIn('all(record["crid"] == requested_crid for record in response_records)', plan)


if __name__ == "__main__":
    unittest.main()
