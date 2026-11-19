from typing import Optional
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
)
from models.employee import Employee


class EmployeeDialog(QDialog):
    def __init__(self, employee: Optional[Employee] = None, parent=None) -> None:
        super().__init__(parent)
        self.employee = employee
        self.setWindowTitle("Edit Employee" if employee else "Add Employee")
        self.setMinimumWidth(380)

        layout = QFormLayout(self)

        self.first_name_input = QLineEdit(employee.first_name if employee else "")
        self.last_name_input = QLineEdit(employee.last_name if employee else "")
        self.email_input = QLineEdit(employee.email if employee else "")
        self.phone_input = QLineEdit(employee.phone or "" if employee else "")
        self.department_input = QLineEdit(employee.department or "" if employee else "")
        self.birth_date_input = QLineEdit(employee.birth_date or "" if employee else "")
        self.birth_date_input.setPlaceholderText("YYYY-MM-DD")

        layout.addRow("First Name *:", self.first_name_input)
        layout.addRow("Last Name *:", self.last_name_input)
        layout.addRow("Email *:", self.email_input)
        layout.addRow("Phone:", self.phone_input)
        layout.addRow("Department:", self.department_input)
        layout.addRow("Birth Date:", self.birth_date_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def _validate_and_accept(self) -> None:
        if not self.first_name_input.text().strip() or not self.last_name_input.text().strip():
            QMessageBox.warning(self, "Missing Data", "First Name and Last Name are required.")
            return
        if not self.email_input.text().strip():
            QMessageBox.warning(self, "Missing Data", "Email address is required.")
            return
        self.accept()

    def get_employee(self) -> Employee:
        return Employee(
            id=self.employee.id if self.employee else None,
            first_name=self.first_name_input.text().strip(),
            last_name=self.last_name_input.text().strip(),
            email=self.email_input.text().strip(),
            phone=self.phone_input.text().strip() or None,
            department=self.department_input.text().strip() or None,
            birth_date=self.birth_date_input.text().strip() or None,
        )
