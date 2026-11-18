from datetime import datetime
from models.employee import Employee
from models.validation_result import ValidationResult


class EmployeeRepository:
    def __init__(self, connection):
        self.conn = connection

    def add_employee(self, employee):
        query = """
                INSERT INTO employees (first_name, last_name, email, phone, department, birth_date)
                VALUES (?, ?, ?, ?, ?, ?) \
                """
        params = (
            employee.first_name,
            employee.last_name,
            employee.email,
            employee.phone,
            employee.department,
            employee.birth_date,
        )
        cr = self.conn.cursor()
        cr.execute(query, params)
        self.conn.commit()
        employee.id = cr.lastrowid
        cr.close()
        return employee.id

    def add_employees(self, employees):
        inserted_ids = []
        query = """
                INSERT INTO employees (first_name, last_name, email, phone, department, birth_date)
                VALUES (?, ?, ?, ?, ?, ?) \
                """
        cr = self.conn.cursor()
        for emp in employees:
            params = (
                emp.first_name,
                emp.last_name,
                emp.email,
                emp.phone,
                emp.department,
                emp.birth_date,
            )
            cr.execute(query, params)
            emp.id = cr.lastrowid
            inserted_ids.append(emp.id)
        self.conn.commit()
        cr.close()
        return inserted_ids

    def get_all_employees(self):
        query = """
                SELECT id, first_name, last_name, email, phone, department, birth_date
                FROM employees
                ORDER BY id ASC \
                """
        cr = self.conn.cursor()
        cr.execute(query)
        rows = cr.fetchall()
        cr.close()
        return [self._row_to_employee(row) for row in rows]

    def get_employee_by_id(self, employee_id):
        query = """
                SELECT id, first_name, last_name, email, phone, department, birth_date
                FROM employees
                WHERE id = ? \
                """
        cr = self.conn.cursor()
        cr.execute(query, (employee_id,))
        row = cr.fetchone()
        cr.close()
        if row is None:
            return None
        return self._row_to_employee(row)

    def update_employee(self, employee):
        if employee.id is None:
            raise ValueError("Mitarbeiter ohne ID kann nicht aktualisiert werden.")

        query = """
                UPDATE employees
                SET first_name = ?,
                    last_name  = ?,
                    email      = ?,
                    phone      = ?,
                    department = ?,
                    birth_date = ?
                WHERE id = ? \
                """
        params = (
            employee.first_name,
            employee.last_name,
            employee.email,
            employee.phone,
            employee.department,
            employee.birth_date,
            employee.id,
        )
        cr = self.conn.cursor()
        cr.execute(query, params)
        self.conn.commit()
        updated = cr.rowcount > 0
        cr.close()
        return updated

    def delete_employee(self, employee_id):
        query = "DELETE FROM employees WHERE id = ?"
        cr = self.conn.cursor()
        cr.execute(query, (employee_id,))
        self.conn.commit()
        deleted = cr.rowcount > 0
        cr.close()
        return deleted

    def save_validation_results(self, results):
        if not results:
            return

        query = """
                INSERT INTO validation_results (employee_id, column_name, error_message, severity)
                VALUES (?, ?, ?, ?) \
                """
        rows = [
            (res.employee_id, res.column_name, res.error_message, res.severity)
            for res in results
        ]
        cr = self.conn.cursor()
        cr.executemany(query, rows)
        self.conn.commit()
        cr.close()

    def get_validation_results(self, employee_id=None):
        cr = self.conn.cursor()
        if employee_id is not None:
            query = """
                    SELECT id, employee_id, column_name, error_message, severity
                    FROM validation_results
                    WHERE employee_id = ?
                    ORDER BY id ASC \
                    """
            cr.execute(query, (employee_id,))
        else:
            query = """
                    SELECT id, employee_id, column_name, error_message, severity
                    FROM validation_results
                    ORDER BY id ASC \
                    """
            cr.execute(query)

        results = [
            ValidationResult(
                id=res_id,
                employee_id=emp_id,
                column_name=column_name,
                error_message=error_message,
                severity=severity,
            )
            for res_id, emp_id, column_name, error_message, severity in cr.fetchall()
        ]
        cr.close()
        return results

    def clear_validation_results(self, employee_id=None):
        cr = self.conn.cursor()
        if employee_id is not None:
            cr.execute(
                "DELETE FROM validation_results WHERE employee_id = ?",
                (employee_id,),
            )
        else:
            cr.execute("DELETE FROM validation_results")
        self.conn.commit()
        cr.close()

    def add_import_history(self, filename, records_imported, records_rejected, import_date=None):
        timestamp = import_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
                INSERT INTO import_history (filename, import_date, records_imported, records_rejected)
                VALUES (?, ?, ?, ?) \
                """
        cr = self.conn.cursor()
        cr.execute(query, (filename, timestamp, records_imported, records_rejected))
        self.conn.commit()
        history_id = cr.lastrowid
        cr.close()
        return history_id

    def get_import_history(self):
        query = """
                SELECT id, filename, import_date, records_imported, records_rejected
                FROM import_history
                ORDER BY id DESC \
                """
        cr = self.conn.cursor()
        cr.execute(query)
        history = [
            {
                "id": hist_id,
                "filename": filename,
                "import_date": import_date,
                "records_imported": records_imported,
                "records_rejected": records_rejected,
            }
            for hist_id, filename, import_date, records_imported, records_rejected in cr.fetchall()
        ]
        cr.close()
        return history

    @staticmethod
    def _row_to_employee(row):
        emp_id, first_name, last_name, email, phone, department, birth_date = row
        return Employee(
            id=emp_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            department=department,
            birth_date=birth_date,
        )

    @staticmethod
    def _row_to_validation_result(row):
        res_id, employee_id, column_name, error_message, severity = row
        return ValidationResult(
            id=res_id,
            employee_id=employee_id,
            column_name=column_name,
            error_message=error_message,
            severity=severity
        )