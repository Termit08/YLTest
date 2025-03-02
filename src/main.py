from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QPixmap, QKeyEvent
from PyQt6 import uic
from PyQt6.QtCore import Qt
import sys
from get_map_image import get_map_image


class Main(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./data/design.ui", self)
        self.setWindowTitle("Карта")
        self.ready_btn.clicked.connect(self.set_map_image)
        self.scale = 0.005  
        self.longitude_value = 0
        self.lattitude_value = 0

    def set_map_image(self):
        self.longitude_value = self.longitude.text()
        self.lattitude_value = self.width.text()
        self.scale = int(self.coord.text())

        img = get_map_image(self.longitude_value, self.lattitude_value, self.scale)

        if img[0] == 200:
            self.map.setPixmap(QPixmap(img[1])) 
        else:
            print('Не удалось получить изображение карты...')
            print(img)
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_PageUp:
            if self.scale < 21:
                self.scale += 1 
                self.update_map()

        elif event.key() == Qt.Key.Key_PageDown:
            if self.scale > 0:
                self.scale -= 1
                self.update_map()
        
    
    def update_map(self):
        img = get_map_image(self.longitude_value, self.lattitude_value, self.scale)

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
