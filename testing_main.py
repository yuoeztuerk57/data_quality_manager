import json
import sys

from PyQt6.QtWidgets import QApplication
from ui.testing_dashboard import TestingDashboard

def load_default_language():
    with open("testing_config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
    return config.get("default_language", "en")


def main():

    app = QApplication(sys.argv)
    default_lang = load_default_language()
    window = TestingDashboard(lang=default_lang)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()