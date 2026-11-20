import re
from PyQt6.QtCore import QDate
from datetime import datetime
from typing import Optional
from PyQt6.QtWidgets import *
from models.employee import Employee


class EmployeeDialog(QDialog):
    DEPARTMENTS = [ "IT", "HR", "Sales", "Finance", "Marketing", "Other"]

    def __init__(self, employee: Optional[Employee] = None, parent=None) -> None:
        super().__init__(parent)
        self.employee = employee
        self.setWindowTitle("Edit Employee" if employee else "Add Employee")
        self.setMinimumWidth(380)

        layout = QFormLayout(self)

        self.first_name_input = QLineEdit(employee.first_name if employee else "")
        self.first_name_input.setPlaceholderText("Enter first name")

        self.last_name_input = QLineEdit(employee.last_name if employee else "")
        self.last_name_input.setPlaceholderText("Enter last name")

        self.email_input = QLineEdit(employee.email if employee else "")
        self.email_input.setPlaceholderText("Enter email address")

        self.phone_input = QLineEdit(employee.phone or "" if employee else "")
        self.phone_input.setPlaceholderText("Enter phone number")

        self.department_input = QComboBox()
        
        self.department_input.setEditable(False)  # Remove this line if you only want fixed choices
        self.department_input.addItems(self.DEPARTMENTS)
        
       
                   

        current_dept = (employee.department or "").strip() if employee else ""
        
        if current_dept:
            if self.department_input.findText(current_dept) == -1:
                self.department_input.addItem(current_dept)
            self.department_input.setCurrentText(current_dept)
        else:
            self.department_input.setPlaceholderText("Choose department")
            self.department_input.setCurrentIndex(-1)
            #self.department_input.setCurrentIndex(0)
            
           

        # self.birth_date_input = QLineEdit(employee.birth_date or "" if employee else "")
        # self.birth_date_input.setPlaceholderText("YYYY-MM-DD")

        self.birth_date_input = QDateEdit()
        self.birth_date_input.setCalendarPopup(True)
        self.birth_date_input.setDisplayFormat("yyyy-MM-dd")
        self.birth_date_input.setDate(QDate.currentDate())
        self.birth_date_input.setSpecialValueText("Nicht angegeben")
        self.birth_date_input.setMinimumDate(QDate(1900, 1, 1))
        self.birth_date_input.setMaximumDate(QDate.currentDate())

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
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        email = self.email_input.text().strip()
        birth_date = self.birth_date_input.text().strip()
        phone = self.phone_input.text().strip()

        if not first_name or not last_name or not email:
            QMessageBox.warning(self, "Fehlende Angaben", "Vorname, Nachname und E-Mail sind Pflichtfelder.")
            return

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            QMessageBox.warning(self, "Ungültige E-Mail", "Bitte eine gültige E-Mail-Adresse eingeben.")
            return

        if any(ch.isdigit() for ch in first_name + last_name):
            QMessageBox.warning(self, "Ungültiger Name", "Vor- und Nachname dürfen keine Zahlen enthalten.")
            return
        if not re.match(r"^\+?[0-9\s\-()]{6,20}$", phone):
            QMessageBox.warning(self, "Ungültige Phone-number", "Bitte eine gültige Telefon nummer eingeben.")
            return


        if birth_date:
            try:
                datetime.strptime(birth_date, "%Y-%m-%d")
            except ValueError:
                QMessageBox.warning(self, "Ungültiges Datum", "Geburtsdatum muss im Format JJJJ-MM-TT vorliegen.")
                return

        self.accept()

    def get_employee(self) -> Employee:
        return Employee(
            id=self.employee.id if self.employee else None,
            first_name=self.first_name_input.text().strip(),
            last_name=self.last_name_input.text().strip(),
            email=self.email_input.text().strip(),
            phone=self.phone_input.text().strip() or None,
            department=self.department_input.currentText().strip() or None,
            birth_date=self.birth_date_input.text().strip() or None,
        )