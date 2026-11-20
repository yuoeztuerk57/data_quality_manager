from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QStatusBar, QHeaderView, QFrame
)
from PyQt6.QtGui import QColor
from database.connection import init_db
from database.employee_repository import EmployeeRepository
from models.employee import Employee
from models.validation_result import ValidationResult
from services.csv_importer import read_csv
from services.data_validator import validate_records
from services.csv_exporter import export_employees_csv
from services.report_generator import export_quality_report_json
from ui.employee_dialog import EmployeeDialog


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("DataQuality Manager")
        self.resize(1180, 760)

        init_db()
        self.repo = EmployeeRepository()
        self._db_employees: list[Employee] = []
        self._staged_rows: list[Employee] = []
        self._staged_findings: dict[int, list[ValidationResult]] = {}

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(12)

        # 1. TOP HEADER: Badges + Import-Historie
        top_bar = QHBoxLayout()
        self.badge_db = self._make_badge("DB Gesamt: 0", "#6c757d", "white")
        self.badge_csv = self._make_badge("CSV Geprüft: 0", "#868e96", "white")
        self.badge_valid = self._make_badge("Gültig: 0", "#2f9e44", "white")
        self.badge_warn = self._make_badge("Warnungen: 0", "#fcc419", "black")
        self.badge_err = self._make_badge("Fehler: 0", "#e03131", "white")

        for b in [self.badge_db, self.badge_csv, self.badge_valid, self.badge_warn, self.badge_err]:
            top_bar.addWidget(b)
        top_bar.addStretch()

        self.history_combo = QComboBox()
        self.history_combo.setMinimumWidth(360)
        top_bar.addWidget(self.history_combo)
        root.addLayout(top_bar)

        # 2. UPPER PANEL: SQLite Datenbank - Mitarbeiter
        db_title = QLabel("SQLite Datenbank - Mitarbeiter")
        db_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        root.addWidget(db_title)

        db_toolbar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Suche")
        self.search_input.textChanged.connect(self._filter_db_table)

        db_toolbar.addWidget(self.search_input, 2)
        db_toolbar.addWidget(QLabel("Abteilung:"))
        self.dept_filter = QComboBox()
        self.dept_filter.addItem("Alle")
        self.dept_filter.currentTextChanged.connect(self._filter_db_table)
        db_toolbar.addWidget(self.dept_filter)

        self.btn_db_del = QPushButton("Delete")
        self.btn_db_edit = QPushButton("Edit")
        self.btn_db_new = QPushButton("+ Neu")
        self.btn_export_csv = QPushButton("CSV exportieren")
        self.btn_export_json = QPushButton("JSON-Report exportieren")

        self.btn_db_del.clicked.connect(self._delete_db_employee)
        self.btn_db_edit.clicked.connect(self._edit_db_employee)
        self.btn_db_new.clicked.connect(self._add_db_employee)
        self.btn_export_csv.clicked.connect(self._export_csv)
        self.btn_export_json.clicked.connect(self._export_json)

        for btn in [self.btn_db_del, self.btn_db_edit, self.btn_db_new, self.btn_export_csv, self.btn_export_json]:
            db_toolbar.addWidget(btn)
        root.addLayout(db_toolbar)

        self.db_table = QTableWidget(0, 7)
        self.db_table.setHorizontalHeaderLabels(["ID", "Vorname", "Nachname", "E-Mail", "Telefon", "Abteilung", "Geburtsdatum"])
        self.db_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.db_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.db_table.setSortingEnabled(True)
        self._setup_db_sort_arrows()
        self.db_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        root.addWidget(self.db_table, 2)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(line)

        # 3. LOWER PANEL: CSV Import-Vorschau & Validierung
        csv_title = QLabel("CSV Import-Vorschau & Validierung")
        csv_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        root.addWidget(csv_title)

        csv_toolbar = QHBoxLayout()
        self.btn_load_csv = QPushButton("CSV laden")
        self.btn_load_csv.clicked.connect(self._load_csv)
        csv_toolbar.addWidget(self.btn_load_csv)
        csv_toolbar.addStretch()

        self.btn_stage_edit = QPushButton("Bearbeiten")
        self.btn_stage_del = QPushButton("Löschen")
        self.btn_commit_db = QPushButton("In DB übernehmen")
        self.btn_commit_db.setStyleSheet("background-color: #2f9e44; color: white; font-weight: bold; padding: 5px 12px;")

        self.btn_stage_edit.clicked.connect(self._edit_staged_row)
        self.btn_stage_del.clicked.connect(self._delete_staged_row)
        self.btn_commit_db.clicked.connect(self._commit_valid_to_db)

        for btn in [self.btn_stage_edit, self.btn_stage_del, self.btn_commit_db]:
            csv_toolbar.addWidget(btn)
        root.addLayout(csv_toolbar)

        self.preview_table = QTableWidget(0, 9)
        self.preview_table.setHorizontalHeaderLabels(
            ["Zeile", "Vorname", "Nachname", "E-Mail", "Telefon", "Abteilung", "Geburtsdatum", "Status", "Fehlermeldung"]
        )
        self.preview_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.preview_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        root.addWidget(self.preview_table, 2)

        self.setStatusBar(QStatusBar())
        self._last_csv_name = ""
        self._refresh_db_view()
        self._refresh_history_combo()

    def _make_badge(self, text: str, bg: str, fg: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(f"background-color: {bg}; color: {fg}; padding: 4px 10px; border-radius: 10px; font-weight: bold;")
        return lbl

    def _setup_db_sort_arrows(self) -> None:
        headers = ["ID", "Vorname", "Nachname", "E-Mail", "Telefon", "Abteilung", "Geburtsdatum"]
        header = self.db_table.horizontalHeader()
        header.setSortIndicatorShown(False)
        header.setStyleSheet("QHeaderView::up-arrow, QHeaderView::down-arrow { width: 0px; height: 0px; }")
        self.db_table.setHorizontalHeaderLabels([f"{h}  ▲ ▼" for h in headers])

        def on_header_clicked(col: int) -> None:
            arrow = "▲" if header.sortIndicatorOrder() == Qt.SortOrder.AscendingOrder else "▼"
            self.db_table.setHorizontalHeaderLabels(
                [f"{h}  {arrow}" if i == col else f"{h}  ▲ ▼" for i, h in enumerate(headers)]
            )

        header.sectionClicked.connect(on_header_clicked)

    # --- DB TABLE LOGIC ---
    def _refresh_db_view(self) -> None:
        self._db_employees = self.repo.get_all_employees()
        self.badge_db.setText(f"DB Gesamt: {len(self._db_employees)}")

        current = self.dept_filter.currentText()
        depts = sorted({e.department.strip() for e in self._db_employees if e.department and e.department.strip()})
        self.dept_filter.blockSignals(True)
        self.dept_filter.clear()
        self.dept_filter.addItem("Alle")
        self.dept_filter.addItems(depts)
        idx = self.dept_filter.findText(current)
        self.dept_filter.setCurrentIndex(idx if idx >= 0 else 0)
        self.dept_filter.blockSignals(False)

        self._filter_db_table()

    def _filter_db_table(self) -> None:
        q = self.search_input.text().strip().lower()
        dept = self.dept_filter.currentText()

        filtered = []
        for e in self._db_employees:
            searchable_fields = [
                str(e.id) if e.id is not None else "",
                e.first_name or "",
                e.last_name or "",
                e.email or "",
                e.phone or "",
                e.department or "",
                e.birth_date or "",
            ]
            matches_search = (not q) or any(q in field.lower() for field in searchable_fields)
            matches_dept = (dept == "Alle") or ((e.department or "").strip() == dept)

            if matches_search and matches_dept:
                filtered.append(e)

        self.db_table.setSortingEnabled(False)
        self.db_table.setRowCount(len(filtered))
        for r, emp in enumerate(filtered):
            id_item = QTableWidgetItem()
            if emp.id is not None:
                id_item.setData(Qt.ItemDataRole.DisplayRole, emp.id)
            self.db_table.setItem(r, 0, id_item)

            other_vals = [emp.first_name, emp.last_name, emp.email, emp.phone or "", emp.department or "", emp.birth_date or ""]
            for c, val in enumerate(other_vals, start=1):
                self.db_table.setItem(r, c, QTableWidgetItem(val))
        self.db_table.setSortingEnabled(True)
        self.db_table.horizontalHeader().setSortIndicatorShown(False)

    def _get_selected_db_emp(self) -> Employee | None:
        rows = self.db_table.selectionModel().selectedRows()
        if not rows:
            return None
        id_item = self.db_table.item(rows[0].row(), 0)
        if not id_item or not id_item.text().strip().isdigit():
            return None
        emp_id = int(id_item.text().strip())
        return next((e for e in self._db_employees if e.id == emp_id), None)

    def _add_db_employee(self) -> None:
        dlg = EmployeeDialog(parent=self)
        if dlg.exec():
            candidate = dlg.get_employee()
            findings = validate_records(self._db_employees + [candidate])
            new_row_index = len(self._db_employees) + 1
            row_issues = [f for f in findings if f.row_index == new_row_index]
            if any(f.severity == "ERROR" for f in row_issues):
                msgs = "\n".join(f.error_message for f in row_issues)
                QMessageBox.warning(self, "Ungültige Daten", f"Speichern abgebrochen:\n{msgs}")
                return
            self.repo.add_employee(candidate)
            self._refresh_db_view()
            if self._staged_rows:
                self._revalidate_staged()

    def _edit_db_employee(self) -> None:
        emp = self._get_selected_db_emp()
        if not emp:
            QMessageBox.information(self, "Auswahl", "Bitte einen Mitarbeiter in der DB-Tabelle auswählen.")
            return
        dlg = EmployeeDialog(employee=emp, parent=self)
        if dlg.exec():
            self.repo.update_employee(dlg.get_employee())
            self._refresh_db_view()
            if self._staged_rows:
                self._revalidate_staged()

    def _delete_db_employee(self) -> None:
        emp = self._get_selected_db_emp()
        if not emp or emp.id is None:
            QMessageBox.information(self, "Auswahl", "Bitte einen Mitarbeiter zum Löschen auswählen.")
            return
        if QMessageBox.question(self, "Löschen bestätigen", f"{emp.first_name} {emp.last_name} wirklich löschen?") == QMessageBox.StandardButton.Yes:
            self.repo.delete_employee(emp.id)
            self._refresh_db_view()
            if self._staged_rows:
                self._revalidate_staged()

    # --- CSV STAGING & VALIDATION LOGIC ---
    def _load_csv(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "CSV laden", "data/", "CSV (*.csv)")
        if not path:
            return
        rows, errors = read_csv(path)
        if errors:
            QMessageBox.warning(self, "CSV Fehler", "\n".join(errors))
            return

        self._last_csv_name = path.split("/")[-1].split("\\")[-1]
        self._staged_rows = [
            Employee(
                first_name=r.get("first_name", ""),
                last_name=r.get("last_name", ""),
                email=r.get("email", ""),
                phone=r.get("phone") or None,
                department=r.get("department") or None,
                birth_date=r.get("birth_date") or None,
            )
            for r in rows
        ]
        self._revalidate_staged()

    def _revalidate_staged(self) -> None:
        combined = self._db_employees + self._staged_rows
        all_findings = validate_records(combined)
        offset = len(self._db_employees)
        self._staged_findings.clear()
        for f in all_findings:
            if f.row_index and f.row_index > offset:
                self._staged_findings.setdefault(f.row_index - offset - 1, []).append(f)

        valid_cnt = warn_cnt = err_cnt = 0
        self.preview_table.setRowCount(len(self._staged_rows))
        for idx, emp in enumerate(self._staged_rows):
            issues = self._staged_findings.get(idx, [])
            if any(i.severity == "ERROR" for i in issues):
                status, bg = "Fehler", QColor("#ffc9c9")
                err_cnt += 1
            elif any(i.severity == "WARNING" for i in issues):
                status, bg = "Warnung", QColor("#fff3bf")
                warn_cnt += 1
            else:
                status, bg = "Gültig", QColor("#d3f9d8")
                valid_cnt += 1

            msg = "; ".join(f"{i.error_message} ({i.severity})" for i in issues) or "OK"
            vals = [str(idx + 1), emp.first_name, emp.last_name, emp.email, emp.phone or "", emp.department or "", emp.birth_date or "", status, msg]
            for c, val in enumerate(vals):
                item = QTableWidgetItem(val)
                item.setBackground(bg)
                self.preview_table.setItem(idx, c, item)

        self.badge_csv.setText(f"CSV Geprüft: {len(self._staged_rows)}")
        self.badge_valid.setText(f"Gültig: {valid_cnt}")
        self.badge_warn.setText(f"Warnungen: {warn_cnt}")
        self.badge_err.setText(f"Fehler: {err_cnt}")

    def _edit_staged_row(self) -> None:
        rows = self.preview_table.selectionModel().selectedRows()
        if not rows:
            return
        idx = rows[0].row()
        dlg = EmployeeDialog(employee=self._staged_rows[idx], parent=self)
        if dlg.exec():
            self._staged_rows[idx] = dlg.get_employee()
            self._revalidate_staged()

    def _delete_staged_row(self) -> None:
        rows = self.preview_table.selectionModel().selectedRows()
        if not rows:
            return
        del self._staged_rows[rows[0].row()]
        self._revalidate_staged()

    def _commit_valid_to_db(self) -> None:
        if not self._staged_rows:
            return
        imported = 0
        remaining: list[Employee] = []
        for idx, emp in enumerate(self._staged_rows):
            if self._staged_findings.get(idx, []):
                remaining.append(emp)
            else:
                self.repo.add_employee(emp)
                imported += 1

        all_findings = [f for flist in self._staged_findings.values() for f in flist]
        if all_findings:
            self.repo.save_validation_results(all_findings)

        self.repo.add_import_history(
            self._last_csv_name or "manual.csv",
            datetime.now().strftime("%d.%m.%Y"),
            imported,
            len(remaining)
        )

        self._staged_rows = remaining
        self._refresh_db_view()
        self._revalidate_staged()
        self._refresh_history_combo()
        self.statusBar().showMessage(f"{imported} übernommen, {len(remaining)} abgelehnt.")

    def _refresh_history_combo(self) -> None:
        self.history_combo.clear()
        rows = self.repo.get_import_history()
        if not rows:
            self.history_combo.addItem("Import-Historie: Noch keine Importe")
            return
        for r in rows:
            self.history_combo.addItem(f"Import-Historie: {r['filename']} ({r['import_date']} | {r['records_imported']} importiert, {r['records_rejected']} abgelehnt)")

    def _export_csv(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "CSV exportieren", "reports/employees_clean.csv", "CSV (*.csv)")
        if path:
            export_employees_csv(self._db_employees, path)
            QMessageBox.information(self, "Export", f"CSV gespeichert unter:\n{path}")

    def _export_json(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "JSON-Report exportieren", "reports/quality_report.json", "JSON (*.json)")
        if path:
            flat_findings = [f for flist in self._staged_findings.values() for f in flist]
            export_quality_report_json(len(self._db_employees), len(self._db_employees), flat_findings, path)
            QMessageBox.information(self, "Export", f"JSON-Report gespeichert unter:\n{path}")