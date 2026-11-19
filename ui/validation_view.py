from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
from models.validation_result import ValidationResult


class ValidationView(QWidget):
    export_csv_requested = pyqtSignal(str)
    export_json_requested = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        btn_bar = QHBoxLayout()
        self.btn_export_csv = QPushButton("Export Valid Employees (CSV)")
        self.btn_export_json = QPushButton("Export Quality Report (JSON)")

        self.btn_export_csv.clicked.connect(self._choose_csv_path)
        self.btn_export_json.clicked.connect(self._choose_json_path)

        btn_bar.addWidget(self.btn_export_csv)
        btn_bar.addWidget(self.btn_export_json)

        self.findings_table = QTableWidget(0, 4)
        self.findings_table.setHorizontalHeaderLabels(["Row", "Severity", "Column", "Message"])
        self.findings_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addLayout(btn_bar)
        layout.addWidget(self.findings_table)

    def set_findings(self, findings: list[ValidationResult]) -> None:
        self.findings_table.setRowCount(len(findings))
        for row_idx, item in enumerate(findings):
            values = [
                str(item.row_index or "-"),
                item.severity,
                item.column_name,
                item.error_message,
            ]
            for col_idx, val in enumerate(values):
                self.findings_table.setItem(row_idx, col_idx, QTableWidgetItem(val))

    def _choose_csv_path(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Save Clean CSV", "reports/clean_employees.csv", "CSV (*.csv)")
        if path:
            self.export_csv_requested.emit(path)
            QMessageBox.information(self, "Export Complete", f"Clean employees exported to:\n{path}")

    def _choose_json_path(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Save Quality Report", "reports/quality_report.json", "JSON (*.json)")
        if path:
            self.export_json_requested.emit(path)
            QMessageBox.information(self, "Export Complete", f"Quality report saved to:\n{path}")
