import json
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from testing.test_report import TestReport
from testing.test_runner import TestRunner

CONFIG_PATH = Path(__file__).resolve().parent.parent / "testing_config.json"

# Fallback-Sprachen, falls testing_config.json noch nicht existiert oder unvollstaendig ist
FALLBACK_LANGUAGES = {
    "en": "English",
    "de": "Deutsch",
    "uk": "Українська",
}

TEXTS = {
    "en": {
        "window_title": "DataQuality Testing Dashboard",
        "header_title": "DATAQUALITY TESTING DASHBOARD",
        "lang_label": "Language:",
        "stats_group": "Test Overview",
        "total": "Total",
        "passed": "Passed",
        "failed": "Failed",
        "skipped": "Skipped",
        "duration": "Duration",
        "sec": "sec",
        "buttons_group": "Test Control",
        "btn_all": "Run All Tests",
        "btn_database": "Database Tests",
        "btn_import": "Import Tests",
        "btn_validation": "Validation Tests",
        "btn_integration": "Integration Tests",
        "btn_failed": "Show Failed Tests",
        "btn_export": "Export JSON Report",
        "headers": ["Test Name", "Module", "Status", "Duration", "Message"],
    },
    "de": {
        "window_title": "DataQuality Test-Dashboard",
        "header_title": "DATAQUALITY TEST-DASHBOARD",
        "lang_label": "Sprache:",
        "stats_group": "Testübersicht",
        "total": "Gesamt",
        "passed": "Bestanden",
        "failed": "Fehlgeschlagen",
        "skipped": "Übersprungen",
        "duration": "Dauer",
        "sec": "Sek.",
        "buttons_group": "Teststeuerung",
        "btn_all": "Alle Tests starten",
        "btn_database": "Datenbank-Tests",
        "btn_import": "Import-Tests",
        "btn_validation": "Validierungs-Tests",
        "btn_integration": "Integrationstests",
        "btn_failed": "Fehlgeschlagene anzeigen",
        "btn_export": "JSON-Bericht exportieren",
        "headers": ["Testname", "Modul", "Status", "Dauer", "Nachricht"],
    },
    "uk": {
        "window_title": "DataQuality Панель тестування",
        "header_title": "DATAQUALITY ПАНЕЛЬ ТЕСТУВАННЯ",
        "lang_label": "Мова:",
        "stats_group": "Огляд тестів",
        "total": "Усього",
        "passed": "Пройдено",
        "failed": "Провалено",
        "skipped": "Пропущено",
        "duration": "Тривалість",
        "sec": "сек.",
        "buttons_group": "Керування тестами",
        "btn_all": "Запустити всі тести",
        "btn_database": "Тести БД",
        "btn_import": "Тести імпорту",
        "btn_validation": "Тести валідації",
        "btn_integration": "Інтеграційні тести",
        "btn_failed": "Показати провалені",
        "btn_export": "Експортувати JSON-звіт",
        "headers": ["Назва тесту", "Модуль", "Статус", "Тривалість", "Повідомлення"],
    },
}


def read_config():
    # Konfigurationsdatei sicher laden
    if not CONFIG_PATH.exists():
        return {}
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def load_languages_from_config(config_data=None):
    # Sprachen aus der Konfigurationsdatei lesen
    data = read_config() if config_data is None else config_data
    raw_languages = data.get("languages")

    if isinstance(raw_languages, dict):
        loaded = {
            str(code): str(label)
            for code, label in raw_languages.items()
            if str(code) in TEXTS
        }
        if loaded:
            return loaded

    return dict(FALLBACK_LANGUAGES)


def load_default_language(available_languages=None, config_data=None):
    # Standardsprache aus der Konfiguration ermitteln
    data = read_config() if config_data is None else config_data
    languages = (
        load_languages_from_config(data)
        if available_languages is None
        else available_languages
    )
    fallback = next(iter(languages))

    lang = data.get("default_language", fallback)
    return lang if lang in languages else fallback


def save_default_language(lang, available_languages=None):
    # Gewaehlte Sprache in testing_config.json speichern, ohne andere Felder zu loeschen
    languages = (
        load_languages_from_config()
        if available_languages is None
        else available_languages
    )
    if lang not in languages:
        return

    data = read_config()
    if "languages" not in data or not isinstance(data["languages"], dict):
        data["languages"] = dict(languages)
    data["default_language"] = lang

    with CONFIG_PATH.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


class TestingDashboard(QWidget):
    def __init__(self, lang=None):
        super().__init__()

        config_data = read_config()
        self.available_languages = load_languages_from_config(config_data)
        default_lang = load_default_language(self.available_languages, config_data)
        self.lang = lang if lang in self.available_languages else default_lang

        self.runner = TestRunner()
        self.report = TestReport()

        self.resize(1000, 650)

        self.init_ui()
        self.apply_language()

    def init_ui(self):
        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(
            "font-size: 22px; font-weight: bold; padding: 15px;"
        )

        self.lang_label = QLabel()
        self.lang_combo = QComboBox()

        for lang_code, lang_name in self.available_languages.items():
            self.lang_combo.addItem(lang_name, userData=lang_code)

        current_index = self.lang_combo.findData(self.lang)
        if current_index >= 0:
            self.lang_combo.setCurrentIndex(current_index)

        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)

        top_bar.addWidget(self.title_label, stretch=1)
        top_bar.addWidget(self.lang_label)
        top_bar.addWidget(self.lang_combo)

        layout.addLayout(top_bar)

        # Statistikbereich
        self.stats_group = QGroupBox()
        stats_layout = QHBoxLayout(self.stats_group)

        self.lbl_total = QLabel()
        self.lbl_passed = QLabel()
        self.lbl_failed = QLabel()
        self.lbl_skipped = QLabel()
        self.lbl_duration = QLabel()

        for label in (
            self.lbl_total,
            self.lbl_passed,
            self.lbl_failed,
            self.lbl_skipped,
            self.lbl_duration,
        ):
            label.setStyleSheet(
                "font-size: 14px; font-weight: bold; padding: 8px;"
            )
            stats_layout.addWidget(label)

        layout.addWidget(self.stats_group)

        # Steuerbuttons fuer Testlaeufe
        self.buttons_group = QGroupBox()
        buttons_layout = QHBoxLayout(self.buttons_group)

        self.btn_all = QPushButton()
        self.btn_database = QPushButton()
        self.btn_import = QPushButton()
        self.btn_validation = QPushButton()
        self.btn_integration = QPushButton()

        buttons_layout.addWidget(self.btn_all)
        buttons_layout.addWidget(self.btn_database)
        buttons_layout.addWidget(self.btn_import)
        buttons_layout.addWidget(self.btn_validation)
        buttons_layout.addWidget(self.btn_integration)

        layout.addWidget(self.buttons_group)

        # Ergebnistabelle
        self.table = QTableWidget()
        self.table.setColumnCount(5)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.table)

        # Zusatzaktionen unten
        bottom_layout = QHBoxLayout()

        self.btn_failed = QPushButton()
        self.btn_export = QPushButton()

        bottom_layout.addWidget(self.btn_failed)
        bottom_layout.addWidget(self.btn_export)

        layout.addLayout(bottom_layout)

        # Signale verbinden
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

    def on_language_changed(self, index):
        new_lang = self.lang_combo.itemData(index)
        if new_lang not in self.available_languages:
            return
        self.lang = new_lang
        save_default_language(new_lang, self.available_languages)
        self.apply_language()

    def apply_language(self):
        t = TEXTS[self.lang]

        self.setWindowTitle(t["window_title"])
        self.title_label.setText(t["header_title"])
        self.lang_label.setText(t["lang_label"])

        self.stats_group.setTitle(t["stats_group"])
        self.buttons_group.setTitle(t["buttons_group"])

        self.btn_all.setText(t["btn_all"])
        self.btn_database.setText(t["btn_database"])
        self.btn_import.setText(t["btn_import"])
        self.btn_validation.setText(t["btn_validation"])
        self.btn_integration.setText(t["btn_integration"])
        self.btn_failed.setText(t["btn_failed"])
        self.btn_export.setText(t["btn_export"])

        self.table.setHorizontalHeaderLabels(t["headers"])
        self.update_statistics()

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
                    result["stderr"] or result["stdout"],
                )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Testing Error",
                str(error),
            )

        finally:
            self.btn_all.setEnabled(True)

    def update_statistics(self):
        t = TEXTS[self.lang]
        summary = self.report.get_summary()

        self.lbl_total.setText(f"{t['total']}: {summary['total_tests']}")
        self.lbl_passed.setText(f"{t['passed']}: {summary['passed']}")
        self.lbl_failed.setText(f"{t['failed']}: {summary['failed']}")
        self.lbl_skipped.setText(f"{t['skipped']}: {summary['skipped']}")
        self.lbl_duration.setText(
            f"{t['duration']}: {summary['duration']} {t['sec']}"
        )

    def update_table(self, results):
        self.table.setRowCount(len(results))

        for row, item in enumerate(results):
            values = [
                item["test"],
                item["module"],
                item["status"],
                str(item["duration"]),
                item["message"],
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
                "No failed tests found.",
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
            "\n".join(messages),
        )

    def export_report(self):
        project_root = Path(__file__).resolve().parent.parent
        report_dir = project_root / "reports"

        report_dir.mkdir(parents=True, exist_ok=True)

        report_path = report_dir / "test_report.json"

        data = {
            "summary": self.report.get_summary(),
            "results": self.report.results,
        }

        try:
            with report_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            QMessageBox.information(
                self,
                "Export Report",
                f"Report saved:\n{report_path}",
            )

        except OSError as error:
            QMessageBox.critical(
                self,
                "Export Error",
                str(error),
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TestingDashboard()
    window.show()

    sys.exit(app.exec())