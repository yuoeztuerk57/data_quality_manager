import tempfile
import unittest
from pathlib import Path

from database.connection import init_db
from database.employee_repository import EmployeeRepository
from models.employee import Employee
from models.validation_result import ValidationResult


class TestEmployeeRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_quality.db"
        init_db(self.db_path)
        self.repo = EmployeeRepository(self.db_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_and_get_employee(self) -> None:
        emp = Employee("Max", "Mustermann", "max@test.de", "0171234567", "IT", "1990-05-14")
        new_id = self.repo.add_employee(emp)
        self.assertGreater(new_id, 0)

        employees = self.repo.get_all_employees()
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0].first_name, "Max")
        self.assertEqual(employees[0].email, "max@test.de")

    def test_update_employee(self) -> None:
        emp = Employee("Anna", "Schmidt", "anna@test.de", "0171234568", "HR", "1988-11-23")
        emp_id = self.repo.add_employee(emp)

        updated_emp = Employee("Anna", "Weber", "anna.weber@test.de", "0171234568", "Management", "1988-11-23", id=emp_id)
        success = self.repo.update_employee(updated_emp)
        self.assertTrue(success)

        employees = self.repo.get_all_employees()
        self.assertEqual(employees[0].last_name, "Weber")
        self.assertEqual(employees[0].department, "Management")

    def test_delete_employee(self) -> None:
        emp = Employee("Peter", "Parker", "peter@test.de", "0171234569", "IT", "1995-02-10")
        emp_id = self.repo.add_employee(emp)

        deleted = self.repo.delete_employee(emp_id)
        self.assertTrue(deleted)
        self.assertEqual(len(self.repo.get_all_employees()), 0)

    def test_save_validation_results(self) -> None:
        emp_id = self.repo.add_employee(Employee("Lisa", "Meyer", "invalid-email"))
        findings = [
            ValidationResult("email", "Invalid email format.", "ERROR", employee_id=emp_id)
        ]
        # Should execute cleanly without raising SQLite foreign key errors
        self.repo.save_validation_results(findings)


if __name__ == "__main__":
    unittest.main()
