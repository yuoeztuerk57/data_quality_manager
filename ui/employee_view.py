from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
from models.employee import Employee
from ui.employee_dialog import EmployeeDialog


class EmployeeView(QWidget):
    add_requested = pyqtSignal(Employee)
    edit_requested = pyqtSignal(Employee)
    delete_requested = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self._all_employees: list[Employee] = []
        self._issue_employee_ids: set[int] = set()
        layout = QVBoxLayout(self)

        # Toolbar: Search + Department Filter + Status Filter + CRUD buttons
        top_bar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or email...")
        self.search_input.textChanged.connect(self._apply_filter)

        self.dept_filter = QComboBox()
        self.dept_filter.addItem("All Departments")
        self.dept_filter.currentTextChanged.connect(self._apply_filter)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["All Statuses", "Valid Only", "Has Issues"])
        self.status_filter.currentTextChanged.connect(self._apply_filter)

        self.btn_add = QPushButton("Add Employee")
        self.btn_edit = QPushButton("Edit Selected")
        self.btn_delete = QPushButton("Delete Selected")

        self.btn_add.clicked.connect(self._handle_add)
        self.btn_edit.clicked.connect(self._handle_edit)
        self.btn_delete.clicked.connect(self._handle_delete)

        top_bar.addWidget(self.search_input, 2)
        top_bar.addWidget(self.dept_filter, 1)
        top_bar.addWidget(self.status_filter, 1)
        top_bar.addWidget(self.btn_add)
        top_bar.addWidget(self.btn_edit)
        top_bar.addWidget(self.btn_delete)

        # Employee table
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "First Name", "Last Name", "Email", "Phone", "Department", "Birth Date"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addLayout(top_bar)
        layout.addWidget(self.table)

    def set_employees(self, employees: list[Employee], issue_ids: set[int] | None = None) -> None:
        self._all_employees = employees
        self._issue_employee_ids = issue_ids or set()

        # Refresh department dropdown options while preserving current selection
        current_dept = self.dept_filter.currentText()
        departments = sorted({e.department.strip() for e in employees if e.department and e.department.strip()})
        self.dept_filter.blockSignals(True)
        self.dept_filter.clear()
        self.dept_filter.addItem("All Departments")
        self.dept_filter.addItems(departments)
        idx = self.dept_filter.findText(current_dept)
        self.dept_filter.setCurrentIndex(idx if idx >= 0 else 0)
        self.dept_filter.blockSignals(False)

        self._apply_filter()

    def _apply_filter(self) -> None:
        query = self.search_input.text().strip().lower()
        selected_dept = self.dept_filter.currentText()
        selected_status = self.status_filter.currentText()

        filtered: list[Employee] = []
        for e in self._all_employees:
            matches_text = (
                query in e.first_name.lower()
                or query in e.last_name.lower()
                or query in e.email.lower()
            )
            matches_dept = (
                selected_dept == "All Departments"
                or (e.department or "").strip() == selected_dept
            )
            has_issue = e.id in self._issue_employee_ids
            matches_status = (
                selected_status == "All Statuses"
                or (selected_status == "Valid Only" and not has_issue)
                or (selected_status == "Has Issues" and has_issue)
            )
            if matches_text and matches_dept and matches_status:
                filtered.append(e)

        self._populate_table(filtered)

    def _populate_table(self, employees: list[Employee]) -> None:
        self.table.setRowCount(len(employees))
        for row_idx, emp in enumerate(employees):
            values = [
                str(emp.id or ""),
                emp.first_name,
                emp.last_name,
                emp.email,
                emp.phone or "",
                emp.department or "",
                emp.birth_date or "",
            ]
            for col_idx, val in enumerate(values):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(val))

    def _get_selected_employee(self) -> Employee | None:
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return None
        row = selected_rows[0].row()
        emp_id_text = self.table.item(row, 0).text()
        if not emp_id_text.isdigit():
            return None
        emp_id = int(emp_id_text)
        return next((e for e in self._all_employees if e.id == emp_id), None)

    def _handle_add(self) -> None:
        dialog = EmployeeDialog(parent=self)
        if dialog.exec():
            self.add_requested.emit(dialog.get_employee())

    def _handle_edit(self) -> None:
        emp = self._get_selected_employee()
        if not emp:
            QMessageBox.information(self, "No Selection", "Please select an employee row to edit.")
            return
        dialog = EmployeeDialog(employee=emp, parent=self)
        if dialog.exec():
            self.edit_requested.emit(dialog.get_employee())

    def _handle_delete(self) -> None:
        emp = self._get_selected_employee()
        if not emp or emp.id is None:
            QMessageBox.information(self, "No Selection", "Please select an employee row to delete.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {emp.first_name} {emp.last_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_requested.emit(emp.id)
