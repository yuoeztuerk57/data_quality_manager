import tempfile
import unittest
import csv

from pathlib import Path

from database.connection import init_db
from database.employee_repository import EmployeeRepository

from services.csv_importer import read_csv
from services.data_validator import validate_records
from services.csv_exporter import export_employees_csv

from models.employee import Employee


class TestFullWorkflow(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_path = Path(self.temp_dir.name)

        self.csv_path = self.project_path / "employees.csv"
        self.db_path = self.project_path / "test.db"
        self.export_path = self.project_path / "export" / "employees.csv"

        self.csv_path.write_text(
            "first_name,last_name,email,phone,department,birth_date\n"
            "Max,Mustermann,max@test.de,0171234567,IT,1990-05-14\n"
            "Anna,Schmidt,anna@test.de,0171234568,HR,1988-11-23\n"
            "Peter,,peter@test.de,0171234569,IT,1995-02-10\n"
            "Max,Mustermann,max@test.de,0171234567,IT,1990-05-14\n"
            "Lisa,Meyer,invalid-email,0171234560,Sales,1992-07-19\n",
            encoding="utf-8"
        )

        init_db(self.db_path)
        self.repository = EmployeeRepository(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_complete_import_validation_database_export(self):

        # 1. Import CSV
        rows, errors = read_csv(str(self.csv_path))

        self.assertEqual(errors, [])
        self.assertEqual(len(rows), 5)

        # 2. Convert records into Employee objects
        employees = [
            Employee.from_record(row)
            for row in rows
        ]

        # 3. Validate employees
        findings = validate_records(employees)

        error_count = sum(
            result.severity == "ERROR"
            for result in findings
        )

        warning_count = sum(
            result.severity == "WARNING"
            for result in findings
        )

        self.assertEqual(error_count, 2)
        self.assertEqual(warning_count, 1)

        # 4. Save employees in SQLite
        employee_ids = []

        for employee in employees:
            employee_id = self.repository.add_employee(employee)
            employee_ids.append(employee_id)
            employee.id = employee_id

        self.assertEqual(len(employee_ids), 5)

        # 5. Save validation findings
        for finding in findings:
            if finding.row_index is not None:
                finding.employee_id = employee_ids[
                    finding.row_index - 1
                ]

        self.repository.save_validation_results(findings)

        # 6. Read employees from database
        saved_employees = self.repository.get_all_employees()

        self.assertEqual(len(saved_employees), 5)

        # 7. Export employees to CSV
        export_employees_csv(
            saved_employees,
            str(self.export_path)
        )

        self.assertTrue(self.export_path.exists())

        with self.export_path.open(
            encoding="utf-8",
            newline=""
        ) as file:

            exported_rows = list(csv.DictReader(file))

        self.assertEqual(len(exported_rows), 5)


if __name__ == "__main__":
    unittest.main()