import sys

from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QPixmap
from frontend.designs.design import Ui_Main

from backend.get_map_image import get_map_image


class Main(QMainWindow, Ui_Main):
    def __init__(self):
        super.__init__()
        self.ready_btn.clicked.connect(self.set_map_image)

    def set_map_image(self):
        long = int(self.longitude.text())
        latt = int(self.width.text())
        sc = int(self.coord.text())

        img = get_map_image(longitude=long, lattitude=latt, scale=sc)

        if img:
            self.map.setPixmap(QPixmap(img)) 
        else:
            print('Не удалось получить изображение карты...')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
