import io
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow


class Ui_Main(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./src/frontend/designs/design.ui", self)
        self.setWindowTitle("Карта")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Ui_Main()
    ex.show()
    sys.exit(app.exec())
