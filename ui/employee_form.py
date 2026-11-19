import re

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)

from models.employee import Employee


class EmployeeForm(QDialog):
#Dialog zum Anlegen und Bearbeiten eines Mitarbeiters
    DEPARTMENTS = ["", "IT", "HR", "Sales", "Finance", "Marketing", "Other"]

    def __init__(self, parent=None, employee=None):
        super().__init__(parent)
        self.employee = employee
        self.setWindowTitle("Mitarbeiter bearbeiten" if employee else "Mitarbeiter hinzufügen")
        self.setMinimumWidth(380)

        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()

        self.department_input = QComboBox()
        self.department_input.setEditable(True)
        self.department_input.addItems(self.DEPARTMENTS)

        self.birth_date_input = QDateEdit()
        self.birth_date_input.setCalendarPopup(True)
        self.birth_date_input.setDisplayFormat("yyyy-MM-dd")
        self.birth_date_input.setDate(QDate.currentDate())
        self.birth_date_input.setSpecialValueText("Nicht angegeben")
        self.birth_date_input.setMinimumDate(QDate(1900, 1, 1))
        self.birth_date_input.setDate(self.birth_date_input.minimumDate())

        form_layout = QFormLayout()
        form_layout.addRow("Vorname *", self.first_name_input)
        form_layout.addRow("Nachname *", self.last_name_input)
        form_layout.addRow("E-Mail *", self.email_input)
        form_layout.addRow("Telefon", self.phone_input)
        form_layout.addRow("Abteilung", self.department_input)
        form_layout.addRow("Geburtsdatum", self.birth_date_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form_layout)
        layout.addWidget(buttons)

        if employee:
            self._load_employee(employee)

    def _load_employee(self, employee):
        self.first_name_input.setText(employee.first_name)
        self.last_name_input.setText(employee.last_name)
        self.email_input.setText(employee.email)
        self.phone_input.setText(employee.phone)
        self.department_input.setCurrentText(employee.department)

        if employee.birth_date:
            date = QDate.fromString(str(employee.birth_date), "yyyy-MM-dd")
            if date.isValid():
                self.birth_date_input.setDate(date)

    def _validate_and_accept(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        email = self.email_input.text().strip()

        if not first_name or not last_name or not email:
            QMessageBox.warning(
                self, "Fehlende Angaben",
                "Vorname, Nachname und E-Mail sind Pflichtfelder."
            )
            return

        # Einfache Formatprüfung. Die umfassende Datenqualitätsprüfung
        # gehört laut Projektbrief in das Modul von Learner 5.
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_pattern, email):
            QMessageBox.warning(
                self, "Ungültige E-Mail",
                "Bitte gib eine gültige E-Mail-Adresse ein."
            )
            self.email_input.setFocus()
            return

        self.accept()

    def get_employee_data(self):
        date = self.birth_date_input.date()
        birth_date = ""
        if date > self.birth_date_input.minimumDate():
            birth_date = date.toString("yyyy-MM-dd")

        return Employee(
            id=self.employee.id if self.employee else None,
            first_name=self.first_name_input.text().strip(),
            last_name=self.last_name_input.text().strip(),
            email=self.email_input.text().strip(),
            phone=self.phone_input.text().strip(),
            department=self.department_input.currentText().strip(),
            birth_date=birth_date,
        )
