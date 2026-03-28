from gui import BulkRenamerApp
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    window = BulkRenamerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
