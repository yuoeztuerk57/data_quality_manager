import unittest
from models.employee import Employee
from services.data_validator import validate_records


class TestDataValidator(unittest.TestCase):
    def test_sample_records(self) -> None:
        records = [
            Employee("Max", "Mustermann", "max@test.de", "0171234567", "IT", "1990-05-14"),
            Employee("Anna", "Schmidt", "anna@test.de", "0171234568", "HR", "1988-11-23"),
            Employee("Peter", "", "peter@test.de", "0171234569", "IT", "1995-02-10"),
            Employee("Max", "Mustermann", "max@test.de", "0171234567", "IT", "1990-05-14"),
            Employee("Lisa", "Meyer", "invalid-email", "0171234560", "Sales", "1992-07-19"),
        ]
        results = validate_records(records)
        severities = [r.severity for r in results]
        self.assertEqual(severities.count("ERROR"), 2)
        self.assertEqual(severities.count("WARNING"), 1)


if __name__ == "__main__":
    unittest.main()
