from pathlib import Path
from database.connection import get_connection, DB_PATH
from models.employee import Employee
from models.validation_result import ValidationResult


class EmployeeRepository:
    def __init__(self, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path

    def add_employee(self, emp: Employee) -> int:
        query = """
            INSERT INTO employees (first_name, last_name, email, phone, department, birth_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        with get_connection(self.db_path) as conn:
            cursor = conn.execute(
                query,
                (emp.first_name, emp.last_name, emp.email, emp.phone, emp.department, emp.birth_date),
            )
            return int(cursor.lastrowid)

    def get_all_employees(self) -> list[Employee]:
        query = "SELECT id, first_name, last_name, email, phone, department, birth_date FROM employees"
        with get_connection(self.db_path) as conn:
            rows = conn.execute(query).fetchall()
        return [
            Employee(
                id=row["id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                phone=row["phone"],
                department=row["department"],
                birth_date=row["birth_date"],
            )
            for row in rows
        ]

    def update_employee(self, emp: Employee) -> bool:
        if emp.id is None:
            return False
        query = """
            UPDATE employees
            SET first_name = ?, last_name = ?, email = ?, phone = ?, department = ?, birth_date = ?
            WHERE id = ?
        """
        with get_connection(self.db_path) as conn:
            cursor = conn.execute(
                query,
                (emp.first_name, emp.last_name, emp.email, emp.phone, emp.department, emp.birth_date, emp.id),
            )
            return cursor.rowcount > 0

    def delete_employee(self, emp_id: int) -> bool:
        query = "DELETE FROM employees WHERE id = ?"
        with get_connection(self.db_path) as conn:
            cursor = conn.execute(query, (emp_id,))
            return cursor.rowcount > 0

    def save_validation_results(self, results: list[ValidationResult]) -> None:
        query = """
            INSERT INTO validation_results (employee_id, column_name, error_message, severity)
            VALUES (?, ?, ?, ?)
        """
        with get_connection(self.db_path) as conn:
            conn.executemany(
                query,
                [(r.employee_id, r.column_name, r.error_message, r.severity) for r in results],
            )
