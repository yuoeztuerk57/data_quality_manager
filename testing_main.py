import sys

from PyQt6.QtWidgets import QApplication
from ui.testing_dashboard import TestingDashboard


def main():

    app = QApplication(sys.argv)

    window = TestingDashboard()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()