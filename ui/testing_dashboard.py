import sys

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QGroupBox,
    QMessageBox,
    QHeaderView,
)

from PyQt6.QtCore import Qt

from testing.test_runner import TestRunner
from testing.test_report import TestReport


class TestingDashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.runner = TestRunner()
        self.report = TestReport()

        self.setWindowTitle("DataQuality Testing Dashboard")
        self.resize(1000, 650)

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("DATAQUALITY TESTING DASHBOARD")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold; padding: 15px;"
        )

        layout.addWidget(title)

        # Statistics

        stats_group = QGroupBox("Test Overview")
        stats_layout = QHBoxLayout(stats_group)

        self.lbl_total = QLabel("Total: 0")
        self.lbl_passed = QLabel("Passed: 0")
        self.lbl_failed = QLabel("Failed: 0")
        self.lbl_skipped = QLabel("Skipped: 0")
        self.lbl_duration = QLabel("Duration: 0 sec")

        for label in (
            self.lbl_total,
            self.lbl_passed,
            self.lbl_failed,
            self.lbl_skipped,
            self.lbl_duration
        ):
            label.setStyleSheet(
                "font-size: 14px; font-weight: bold; padding: 8px;"
            )
            stats_layout.addWidget(label)

        layout.addWidget(stats_group)

        # Test buttons

        buttons_group = QGroupBox("Test Control")
        buttons_layout = QHBoxLayout(buttons_group)

        self.btn_all = QPushButton("Run All Tests")
        self.btn_database = QPushButton("Database Tests")
        self.btn_import = QPushButton("Import Tests")
        self.btn_validation = QPushButton("Validation Tests")
        self.btn_integration = QPushButton("Integration Tests")

        buttons_layout.addWidget(self.btn_all)
        buttons_layout.addWidget(self.btn_database)
        buttons_layout.addWidget(self.btn_import)
        buttons_layout.addWidget(self.btn_validation)
        buttons_layout.addWidget(self.btn_integration)

        layout.addWidget(buttons_group)

        # Results table

        self.table = QTableWidget()
        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "Test Name",
            "Module",
            "Status",
            "Duration",
            "Message"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.table)

        # Additional buttons

        bottom_layout = QHBoxLayout()

        self.btn_failed = QPushButton("Show Failed Tests")
        self.btn_export = QPushButton("Export JSON Report")

        bottom_layout.addWidget(self.btn_failed)
        bottom_layout.addWidget(self.btn_export)

        layout.addLayout(bottom_layout)

        # Connect buttons

        self.btn_all.clicked.connect(lambda: self.run_tests())
        self.btn_database.clicked.connect(
            lambda: self.run_tests("tests/test_database.py")
        )
        self.btn_import.clicked.connect(
            lambda: self.run_tests("tests/test_importer.py")
        )
        self.btn_validation.clicked.connect(
            lambda: self.run_tests("tests/test_validator.py")
        )
        self.btn_integration.clicked.connect(
            lambda: self.run_tests("tests/test_integration.py")
        )

        self.btn_failed.clicked.connect(self.show_failed_tests)
        self.btn_export.clicked.connect(self.export_report)

    def run_tests(self, test_path=None):

        self.btn_all.setEnabled(False)

        try:
            result = self.runner.run_tests(test_path)

            self.report.load_results(result["results"])

            self.update_statistics()
            self.update_table(result["results"])

            if result["return_code"] not in (0, 1, 5):
                QMessageBox.warning(
                    self,
                    "Test Execution",
                    result["stderr"] or result["stdout"]
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Testing Error",
                str(error)
            )

        finally:
            self.btn_all.setEnabled(True)

    def update_statistics(self):

        summary = self.report.get_summary()

        self.lbl_total.setText(
            f"Total: {summary['total_tests']}"
        )

        self.lbl_passed.setText(
            f"Passed: {summary['passed']}"
        )

        self.lbl_failed.setText(
            f"Failed: {summary['failed']}"
        )

        self.lbl_skipped.setText(
            f"Skipped: {summary['skipped']}"
        )

        self.lbl_duration.setText(
            f"Duration: {summary['duration']} sec"
        )

    def update_table(self, results):

        self.table.setRowCount(len(results))

        for row, item in enumerate(results):

            values = [
                item["test"],
                item["module"],
                item["status"],
                str(item["duration"]),
                item["message"]
            ]

            for column, value in enumerate(values):

                cell = QTableWidgetItem(value)

                if column == 2:

                    if value == "PASS":
                        cell.setForeground(Qt.GlobalColor.darkGreen)

                    elif value == "FAIL":
                        cell.setForeground(Qt.GlobalColor.red)

                    elif value == "SKIPPED":
                        cell.setForeground(Qt.GlobalColor.darkYellow)

                self.table.setItem(row, column, cell)

    def show_failed_tests(self):

        failed = [
            item for item in self.report.results
            if item["status"] == "FAIL"
        ]

        if not failed:

            QMessageBox.information(
                self,
                "Failed Tests",
                "No failed tests found."
            )
            return

        messages = []

        for item in failed:

            messages.append(
                f"{item['test']}\n"
                f"Module: {item['module']}\n"
                f"Error: {item['message']}\n"
            )

        QMessageBox.warning(
            self,
            "Failed Tests",
            "\n".join(messages)
        )

    def export_report(self):

        from pathlib import Path
        import json

        project_root = Path(__file__).resolve().parent.parent
        report_dir = project_root / "reports"

        report_dir.mkdir(parents=True, exist_ok=True)

        report_path = report_dir / "test_report.json"

        data = {
            "summary": self.report.get_summary(),
            "results": self.report.results
        }

        try:

            with report_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            QMessageBox.information(
                self,
                "Export Report",
                f"Report saved:\n{report_path}"
            )

        except OSError as error:

            QMessageBox.critical(
                self,
                "Export Error",
                str(error)
            )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = TestingDashboard()
    window.show()

    sys.exit(app.exec())