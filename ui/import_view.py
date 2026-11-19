from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
import csv
import json
from datetime import datetime

app = QApplication([])

# Main window
window = QWidget()
window.setWindowTitle("CSV Import & Validation")
window.resize(1150, 750)

layout = QVBoxLayout()

# Title
title = QLabel("CSV Import & Validation")
layout.addWidget(title)

# -----------------------------
# Top buttons
top_layout = QHBoxLayout()

import_button = QPushButton("Import CSV")
edit_button = QPushButton("Edit Record")
delete_button = QPushButton("Delete Record")
history_button = QPushButton("History")
export_button = QPushButton("Export to JSON")

top_layout.addWidget(import_button)
top_layout.addWidget(edit_button)
top_layout.addWidget(delete_button)
top_layout.addWidget(history_button)
top_layout.addWidget(export_button)

layout.addLayout(top_layout)

# File name
file_name = QLabel("No file selected")
layout.addWidget(file_name)

# -----------------------------
# Table
table = QTableWidget()
table.setColumnCount(7)
table.setHorizontalHeaderLabels(["Name", "Last Name", "Email", "Phone", "Department", "Status", "Error Message"])
table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

header_font = QFont()
header_font.setBold(True)
table.horizontalHeader().setFont(header_font)

table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

table.setStyleSheet("QTableWidget::item:selected {background-color: #D3D3D3; color: black;}")

layout.addWidget(table)

# -----------------------------
# Initial data, as per employees
records = [
    ["Max", "Mustermann", "max@test.de","0171234567", "IT", "Valid", "—"],
    ["Anna", "Schmidt", "anna@test.de","0171234568", "HR", "Valid", "—"],
    ["Peter", "", "peter@test.de", "0171234569", "IT", "Error", "Missing last name"],
    ["Max", "Mustermann", "max@test.de", "0171234567", "IT", "Warning", "Duplicate record"],
    ["Lisa", "Meyer", "invalid-email", "0171234560", "Sales", "Error", "Invalid email"]
]

# Import history
history = []

# -----------------------------
# Update table and statistics
def update_table():

    table.setRowCount(0)
    for record in records:
        row = table.rowCount()
        table.insertRow(row)

        for column, value in enumerate(record):
            item = QTableWidgetItem(str(value))
            if column == 5:
                item.setTextAlignment( Qt.AlignmentFlag.AlignCenter)
                if value == "Valid": item.setForeground(QColor("green"))
                elif value == "Warning": item.setForeground(QColor("orange"))
                elif value == "Error": item.setForeground(QColor("red"))
            table.setItem(row, column, item)

    total = len(records)
    valid = sum(1 for r in records if r[5] == "valid")
    warnings = sum(1 for r in records if r[5] == "Warning")
    errors = sum(1 for r in records if r[5] == "Error")

    total_label.setText(f"Total records: {total}")
    valid_label.setText(f"Valid: {valid}")
    warning_label.setText(f"Warnings: {warnings}")
    error_label.setText(f"Errors: {errors}")


# -----------------------------
# Import CSV
def import_csv():
    filename, _ = QFileDialog.getOpenFileName(window, "Select CSV file", "", "CSV Files (*.csv)")
    if not filename:
        return

    try:
        with open(filename, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.reader(file)
            imported_records = list(reader)

        if not imported_records:
            QMessageBox.warning(window, "Error", "CSV file is empty.")
            return

        # Remove headers
        imported_records = imported_records[1:]

        # Check columns - we need some validation here, or columns wil be mixed.
        
        records.clear()
        records.extend(imported_records)

        file_name.setText(f"File: {filename.split('/')[-1]}")

        history.append({"file": filename, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "total": len(records)})
        update_table()

        QMessageBox.information(window, "Success", "CSV imported successfully.")

    except Exception as e:
        QMessageBox.warning(window, "Error", str(e))

# -----------------------------
# Get selected record
def get_selected_record():
    row = table.currentRow()

    if row < 0:
        QMessageBox.information( window, "Information", "Please select a record!")
        return None

    return records[row]

# -----------------------------
# Edit record
def edit_record():
    record = get_selected_record()

    if record is None:
        return

    form = QDialog(window)
    form.setWindowTitle("Edit Record")

    form_layout = QFormLayout()

    fields = []

    labels = ["Name", "Last Name", "Email", "Phone", "Department", "Status", "Error Message"]

    for i, label in enumerate(labels):
        field = QLineEdit(record[i])
        fields.append(field)
        form_layout.addRow(label + ":", field)

    save_button = QPushButton("Save")
    cancel_button = QPushButton("Cancel")

    form_layout.addRow(save_button, cancel_button)

    form.setLayout(form_layout)

    def save():
        if not all(field.text().strip() for field in fields[:5]):
            QMessageBox.warning(form, "Error", "Fill in all mandatory fields" )
            return
        record[:] = [field.text() for field in fields]

        update_table()
        form.accept()

        QMessageBox.information(window, "Success", "Record updated.")

    save_button.clicked.connect(save)
    cancel_button.clicked.connect(form.reject)

    form.exec()

# -----------------------------
# Delete record
def delete_record():
    record = get_selected_record()
    if record is None:
        return

    answer = QMessageBox.question( window, "Delete Record", "Are you sure you want to delete this record?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    if answer == QMessageBox.StandardButton.Yes:
        records.remove(record)
        update_table()

        QMessageBox.information( window, "Success", "Record deleted!")

# -----------------------------
# Export current report to JSON
def export_json():
    if not records:
        QMessageBox.information(window, "Information", "No records to export.")
        return

    filename, _ = QFileDialog.getSaveFileName(window, "Export JSON", "import_report.json", "JSON Files (*.json)")

    if not filename:
        return

    report = {
        "file": file_name.text(), 
        "export_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "statistics": {"total": len(records), "valid": sum(1 for r in records if r[5] == "Valid"), "warnings": sum(1 for r in records if r[5] == "Warning"), "errors": sum(1 for r in records if r[5] == "Error")},
        "records": [{
                "first_name": r[0],
                "last_name": r[1],
                "email": r[2],
                "phone": r[3],
                "department": r[4],
                "status": r[5],
                "error_message": r[6]}
            for r in records]
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    QMessageBox.information(window, "Success", "JSON exported successfully.")

# -----------------------------
# History window
def show_history():
    history_window = QDialog(window)
    history_window.setWindowTitle("Import History")
    history_window.resize(600, 400)

    history_layout = QVBoxLayout()
    history_table = QTableWidget()
    history_table.setColumnCount(3)

    history_table.setHorizontalHeaderLabels([ "File", "Date", "Total Records" ])
    history_table.horizontalHeader().setSectionResizeMode( QHeaderView.ResizeMode.Stretch)
    history_table.setRowCount(len(history))

    for row, entry in enumerate(history):
        history_table.setItem(row, 0, QTableWidgetItem(entry["file"]))
        history_table.setItem(row, 1, QTableWidgetItem(entry["date"]))
        history_table.setItem(row, 2, QTableWidgetItem(str(entry["total"])))
    history_layout.addWidget(history_table)


    export_history_button = QPushButton("Export History to JSON")
    history_layout.addWidget(export_history_button)

    def export_history():
        filename, _ = QFileDialog.getSaveFileName(history_window, "Export History", "import_history.json", "JSON Files (*.json)")

        if not filename:
            return

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4, ensure_ascii=False)

        QMessageBox.information(history_window, "Success", "History exported successfully!")

    export_history_button.clicked.connect(export_history)

    history_window.setLayout(history_layout)
    history_window.exec()


# -----------------------------
# Statistics
statistics_layout = QHBoxLayout()

total_label = QLabel("Total records: 0")
valid_label = QLabel("Valid: 0")
warning_label = QLabel("Warnings: 0")
error_label = QLabel("Errors: 0")

statistics_layout.addWidget(total_label)
statistics_layout.addWidget(valid_label)
statistics_layout.addWidget(warning_label)
statistics_layout.addWidget(error_label)

layout.addLayout(statistics_layout)


# Save button
bottom_layout = QHBoxLayout()

bottom_layout.addStretch()
save_to_db_button = QPushButton("Save into DB")
bottom_layout.addWidget(save_to_db_button)

#after save - add message - QMessageBox.information(history_window, "Success", "Data is saved into DB.")

layout.addLayout(bottom_layout)

# -----------------------------
# Connect buttons
import_button.clicked.connect(import_csv)
edit_button.clicked.connect(edit_record)
delete_button.clicked.connect(delete_record)
history_button.clicked.connect(show_history)
export_button.clicked.connect(export_json)
#export_button.clicked.connect(save_to_db) #Yurrii code

# Initial display
update_table()

# -----------------------------
window.setLayout(layout)
window.show()

app.exec()
