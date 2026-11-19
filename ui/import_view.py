from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt6.QtCore import pyqtSignal
from services.csv_importer import read_csv


class ImportView(QWidget):
    records_imported = pyqtSignal(list, str)  # Emits (rows, filename)

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("CSV Data Import")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.btn_select = QPushButton("Select CSV File to Import")
        self.btn_select.setMinimumHeight(40)
        self.lbl_status = QLabel("No file imported yet.")

        self.btn_select.clicked.connect(self._open_file)

        layout.addWidget(title)
        layout.addWidget(self.btn_select)
        layout.addWidget(self.lbl_status)
        layout.addStretch()

    def _open_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "data/", "CSV Files (*.csv)")
        if not file_path:
            return

        rows, errors = read_csv(file_path)
        if errors:
            QMessageBox.warning(self, "Import Error", "\n".join(errors))
            self.lbl_status.setText("Import failed due to file/header errors.")
            return

        self.lbl_status.setText(f"Successfully loaded {len(rows)} rows from {file_path}")
        self.records_imported.emit(rows, file_path)
