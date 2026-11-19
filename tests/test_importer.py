import tempfile
import unittest
from pathlib import Path

from services.csv_importer import read_csv


class TestCsvImporter(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_read_valid_csv_and_trim_whitespace(self) -> None:
        csv_file = self.base_path / "valid.csv"
        csv_file.write_text(
            "first_name,last_name,email,phone,department,birth_date\n"
            "  Lukas  ,  Wagner  ,lukas@test.de,0171888999,Sales,1989-04-18\n",
            encoding="utf-8",
        )

        rows, errors = read_csv(str(csv_file))
        self.assertEqual(errors, [])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["first_name"], "Lukas")
        self.assertEqual(rows[0]["last_name"], "Wagner")

    def test_missing_file_returns_error(self) -> None:
        rows, errors = read_csv(str(self.base_path / "does_not_exist.csv"))
        self.assertEqual(rows, [])
        self.assertEqual(len(errors), 1)
        self.assertIn("File not found", errors[0])

    def test_missing_required_headers(self) -> None:
        csv_file = self.base_path / "bad_headers.csv"
        csv_file.write_text(
            "first_name,email\n"
            "Max,max@test.de\n",
            encoding="utf-8",
        )

        rows, errors = read_csv(str(csv_file))
        self.assertEqual(rows, [])
        self.assertEqual(len(errors), 1)
        self.assertIn("Missing required columns", errors[0])

    def test_empty_file_returns_error(self) -> None:
        csv_file = self.base_path / "empty.csv"
        csv_file.write_text("", encoding="utf-8")

        rows, errors = read_csv(str(csv_file))
        self.assertEqual(rows, [])
        self.assertEqual(len(errors), 1)
        self.assertIn("empty", errors[0].lower())


if __name__ == "__main__":
    unittest.main()
