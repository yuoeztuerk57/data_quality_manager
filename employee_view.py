from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView,
    QMessageBox, QLabel, QHeaderView, QAbstractItemView
)

from models.employee import Employee
from ui.employee_form import EmployeeForm


class EmployeeTableModel(QAbstractTableModel):
#Qt-Tabellenmodell: trennt die Daten von der Darstellung

    HEADERS = [
        "ID", "Vorname", "Nachname", "E-Mail",
        "Telefon", "Abteilung", "Geburtsdatum"
    ]

    def __init__(self, employees=None, parent=None):
        super().__init__(parent)
        self._employees = [Employee.from_record(e) for e in (employees or [])]

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self._employees)

    def columnCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self.HEADERS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        employee = self._employees[index.row()]
        values = [
            employee.id if employee.id is not None else "",
            employee.first_name,
            employee.last_name,
            employee.email,
            employee.phone,
            employee.department,
            employee.birth_date or "",
        ]

        if role == Qt.ItemDataRole.DisplayRole:
            return str(values[index.column()])
        if role == Qt.ItemDataRole.TextAlignmentRole and index.column() == 0:
            return int(Qt.AlignmentFlag.AlignCenter)
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return str(section + 1)

    def employee_at(self, row):
        if 0 <= row < len(self._employees):
            return self._employees[row]
        return None

    def set_employees(self, employees):
        self.beginResetModel()
        self._employees = [Employee.from_record(e) for e in employees]
        self.endResetModel()


class EmployeeView(QWidget):
    # Mitarbeiterverwaltung für Learner 3.

    # Erwartete Repository-Methoden von Learner 4:
    # get_all_employees() -> list[Employee | dict]
    # add_employee(employee) -> optional neue ID
    # update_employee(employee_id, employee) -> optional bool
    # delete_employee(employee_id) -> optional bool
    # Das Repository muss Employee-Objekte oder Dictionaries akzeptieren.

    def __init__(self, employee_repository, parent=None):
        super().__init__(parent)
        self.repository = employee_repository

        self.title_label = QLabel("Mitarbeiterverwaltung")
        self.add_button = QPushButton("＋ Mitarbeiter hinzufügen")
        self.edit_button = QPushButton("Bearbeiten")
        self.delete_button = QPushButton("Löschen")
        self.refresh_button = QPushButton("Aktualisieren")

        self.table = QTableView()
        self.table_model = EmployeeTableModel()
        self.table.setModel(self.table_model)
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.horizontalHeader().setStretchLastSection(True)

        top_buttons = QHBoxLayout()
        top_buttons.addWidget(self.add_button)
        top_buttons.addWidget(self.edit_button)
        top_buttons.addWidget(self.delete_button)
        top_buttons.addStretch()
        top_buttons.addWidget(self.refresh_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addLayout(top_buttons)
        layout.addWidget(self.table)

        self.add_button.clicked.connect(self.add_employee)
        self.edit_button.clicked.connect(self.edit_employee)
        self.delete_button.clicked.connect(self.delete_employee)
        self.refresh_button.clicked.connect(self.refresh_employees)
        self.table.doubleClicked.connect(lambda _index: self.edit_employee())

        self.refresh_employees()

    def _selected_employee(self):
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            QMessageBox.information(
                self, "Keine Auswahl",
                "Bitte wähle zuerst einen Mitarbeiter aus."
            )
            return None
        return self.table_model.employee_at(selected[0].row())

    def refresh_employees(self):
        try:
            employees = self.repository.get_all_employees()
            self.table_model.set_employees(employees)
        except Exception as exc:
            QMessageBox.critical(
                self, "Datenbankfehler",
                f"Mitarbeiter konnten nicht geladen werden:\n{exc}"
            )

    def add_employee(self):
        dialog = EmployeeForm(self)
        if dialog.exec():
            employee = dialog.get_employee_data()
            try:
                self.repository.add_employee(employee)
                self.refresh_employees()
                QMessageBox.information(
                    self, "Erfolgreich",
                    "Der Mitarbeiter wurde hinzugefügt."
                )
            except Exception as exc:
                QMessageBox.critical(
                    self, "Speicherfehler",
                    f"Der Mitarbeiter konnte nicht gespeichert werden:\n{exc}"
                )

    def edit_employee(self):
        employee = self._selected_employee()
        if employee is None:
            return

        dialog = EmployeeForm(self, employee)
        if dialog.exec():
            updated_employee = dialog.get_employee_data()
            try:
                self.repository.update_employee(
                    employee.id, updated_employee
                )
                self.refresh_employees()
                QMessageBox.information(
                    self, "Erfolgreich",
                    "Die Änderungen wurden gespeichert."
                )
            except Exception as exc:
                QMessageBox.critical(
                    self, "Speicherfehler",
                    f"Die Änderungen konnten nicht gespeichert werden:\n{exc}"
                )

    def delete_employee(self):
        employee = self._selected_employee()
        if employee is None:
            return

        answer = QMessageBox.question(
            self,
            "Löschen bestätigen",
            f"Soll {employee.first_name} {employee.last_name} wirklich gelöscht werden?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            self.repository.delete_employee(employee.id)
            self.refresh_employees()
            QMessageBox.information(
                self, "Erfolgreich",
                "Der Mitarbeiter wurde gelöscht."
            )
        except Exception as exc:
            QMessageBox.critical(
                self, "Löschfehler",
                f"Der Mitarbeiter konnte nicht gelöscht werden:\n{exc}"
            )
