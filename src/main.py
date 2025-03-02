from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
import sys
from get_map_image import get_map_image


class Main(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./data/design.ui", self)
        self.setWindowTitle("Карта")
        self.ready_btn.clicked.connect(self.set_map_image)

    def set_map_image(self):
        long = self.longitude.text()
        latt = self.width.text()
        sc = int(self.coord.text())

        img = get_map_image(longitude=long, lattitude=latt, scale=sc)

        if img[0] == 200:
            self.map.setPixmap(QPixmap(img[1])) 
        else:
            print('Не удалось получить изображение карты...')
            print(img)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
