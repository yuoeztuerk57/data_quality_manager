from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class DashboardView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("DataQuality Manager — Dashboard")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")

        self.stats_label = QLabel("Total Employees: 0\nValidation Errors: 0\nValidation Warnings: 0")
        self.stats_label.setStyleSheet("font-size: 16px; line-height: 1.5;")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(title)
        layout.addWidget(self.stats_label)
        layout.addStretch()

    def update_stats(self, total: int, errors: int, warnings: int) -> None:
        self.stats_label.setText(
            f"Total Employees: {total}\n"
            f"Validation Errors: {errors}\n"
            f"Validation Warnings: {warnings}"
        )
