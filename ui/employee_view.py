from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import csv
import re

app = QApplication([])

# Main window
window = QWidget()
window.setWindowTitle("Employees")
window.resize(1000, 800)

layout = QVBoxLayout()

# Title
title = QLabel("Employees")
layout.addWidget(title)

# -----------------------------
# Search and filter
input_layout = QHBoxLayout()

search_field = QLineEdit()
search_field.setPlaceholderText("Search...")

filter_label = QLabel("Filter by Department:")

filter_combo = QComboBox()
filter_combo.addItems(["All Company", "IT", "HR", "Sales", "Finance"])
input_layout.addWidget(search_field)
input_layout.addWidget(filter_label)
input_layout.addWidget(filter_combo)

layout.addLayout(input_layout)

# -----------------------------
# Buttons
action_layout = QHBoxLayout()

add_button = QPushButton("Add Employee")
edit_button = QPushButton("Edit Employee")
delete_button = QPushButton("Delete Employee")
save_to_csv_button = QPushButton("Export to CSV")

action_layout.addWidget(add_button)
action_layout.addWidget(edit_button)
action_layout.addWidget(delete_button)
action_layout.addWidget(save_to_csv_button)

layout.addLayout(action_layout)

# -----------------------------
# Employee table
table = QTableWidget()

table.setColumnCount(6)
table.setHorizontalHeaderLabels(["ID", "Name", "Last Name", "Phone", "Email", "Abteilung"])
table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

header_font = QFont()
header_font.setBold(True)
table.horizontalHeader().setFont(header_font)

table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

table.setStyleSheet("QTableWidget::item:selected {background-color: #D3D3D3; color: black;}")

table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
table.setSortingEnabled(True)

layout.addWidget(table)

# -----------------------------
# Employee data (temporary database), remove when wir csv file erstllen.
employees = [
    [1, "Max", "Mustermann", "0171234567", "max@test.de", "IT"],
    [2, "Anna", "Schmidt", "0171234568", "anna@test.de", "HR"],
    [3, "Peter", "Müller", "0171234569", "peter@test.de", "IT"],
    [4, "Lisa", "Meyer", "0171234560", "lisa@test.de", "Sales"],
    [5, "John", "Becker", "0171234561", "john@test.de", "Finance"]
]

# Status label
status_label = QLabel()
layout.addWidget(status_label)

# Display employees in table
def update_table():

    table.setSortingEnabled(False)
    table.setRowCount(0)

    search = search_field.text().lower()
    department = filter_combo.currentText()

    for employee in employees:
        # Search filter
        text = " ".join(map(str, employee)).lower()

        if search not in text:
            continue

        # Department filter
        if department != "All Company":
            if employee[5] != department:
                continue

        row = table.rowCount()
        table.insertRow(row)

        for column, value in enumerate(employee):
            table.setItem(row, column, QTableWidgetItem(str(value)))

    table.setSortingEnabled(True)

    status_label.setText(f"Total Employees: {table.rowCount()}")


# -----------------------------
# Add employee
def add_employee():
    form = QDialog(window)
    form.setWindowTitle("Add Employee")
    form_layout = QFormLayout()

    name = QLineEdit()
    form_layout.addRow("Name:*", name)

    lastname = QLineEdit()
    form_layout.addRow("Last Name:*", lastname)

    phone = QLineEdit()
    form_layout.addRow("Phone:*", phone)

    email = QLineEdit()
    form_layout.addRow("Email:*", email)

    department = QComboBox()
    department.addItems(["IT", "HR", "Sales", "Finance"])
    form_layout.addRow("Department:*", department)

    add = QPushButton("Add")
    cancel = QPushButton("Cancel")
    form_layout.addRow(add, cancel)

    form.setLayout(form_layout)

#handle erroe messages:
    def save():
        if not all([name.text(), lastname.text(),phone.text(), email.text()]):
            QMessageBox.warning(form, "Error", "Fill in mandatory fields!")
            return

        if not re.findall(r"[0-9]+", phone.text()):
            QMessageBox.warning(form, "Error", "Phone can contain only numbers.")
            return

        if not re.findall(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.text()):
            QMessageBox.warning(form, "Error", "Invalid email format")
            return

        new_id = max([e[0] for e in employees], default=0) + 1
        employees.append([new_id, name.text(), lastname.text(),phone.text(), email.text(), department.currentText()])
        update_table()
        form.accept()

        QMessageBox.information(window, "Success", "Employee added!")

    add.clicked.connect(save)
    cancel.clicked.connect(form.reject)
    form.exec()


# -----------------------------
# Get selected employee
def get_selected_employee():

    row = table.currentRow()

    if row < 0:
        QMessageBox.information(
            window, "Information", "Please select an employee!"
        )
        return None

    employee_id = int(table.item(row, 0).text())
    for employee in employees:
        if employee[0] == employee_id:
            return employee
    return None


# -----------------------------
# Edit employee
def edit_employee():

    employee = get_selected_employee()

    if employee is None:
        return

    form = QDialog(window)
    form.setWindowTitle("Edit Employee")

    form_layout = QFormLayout()

    id_field = QLineEdit(str(employee[0]))
    id_field.setEnabled(False)
    id_field.setStyleSheet("QLineEdit:disabled {background-color: #D3D3D3;color: #555555;}")
    form_layout.addRow("ID:*", id_field)

    name = QLineEdit(employee[1])
    form_layout.addRow("Name:*", name)

    lastname = QLineEdit(employee[2])
    form_layout.addRow("Last Name:*", lastname)

    phone = QLineEdit(employee[3])
    form_layout.addRow("Phone:*", phone)

    email = QLineEdit(employee[4])
    form_layout.addRow("Email:*", email)

    department = QComboBox()
    department.addItems(["IT", "HR", "Sales", "Finance"])
    department.setCurrentText(employee[5])
    form_layout.addRow("Department:*", department)

    save = QPushButton("Save")
    cancel = QPushButton("Cancel")
    form_layout.addRow(save, cancel)

    form.setLayout(form_layout)

    def update():

        if not all([name.text(), lastname.text(), phone.text(), email.text()]):
            QMessageBox.warning(form, "Error", "Fill in mandatory fields!")
            return

        if not re.fullmatch(r"[0-9]+", phone.text()):
            QMessageBox.warning(form, "Error", "Phone can contain only numbers")
            return

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.text()):
            QMessageBox.warning(form, "Error", "Invalid email format.")
            return

        employee[1:] = [name.text(), lastname.text(), phone.text(), email.text(), department.currentText()]

        update_table()
        form.accept()

        QMessageBox.information(window, "Success", "Edits saved to employee.")

    save.clicked.connect(update)
    cancel.clicked.connect(form.reject)

    form.exec()

# -----------------------------
# Delete employee
def delete_employee():

    employee = get_selected_employee()

    if employee is None:
        return

    answer = QMessageBox.question( window, "Delete Employee", "Are you sure you want to delete this employee?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    if answer == QMessageBox.StandardButton.Yes:
        employees.remove(employee)
        update_table()

        QMessageBox.information(window, "Success", "Employee deleted!")

# -----------------------------
# Export to CSV
def save_to_csv():

    filename, _ = QFileDialog.getSaveFileName(window, "Save CSV", "employees.csv", "CSV Files (*.csv)")

    if filename:
        with open(filename, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Last Name", "Phone", "Email", "Department"])

            for row in range(table.rowCount()):
                writer.writerow([table.item(row, col).text() for col in range(6)])

        QMessageBox.information(window, "Success", "CSV exported.")


# -----------------------------
# Connect buttons and filters
add_button.clicked.connect(add_employee)
edit_button.clicked.connect(edit_employee)
delete_button.clicked.connect(delete_employee)
save_to_csv_button.clicked.connect(save_to_csv)

search_field.textChanged.connect(update_table)
filter_combo.currentTextChanged.connect(update_table)

# Initial display
update_table()

# -----------------------------
window.setLayout(layout)
window.show()

app.exec()
