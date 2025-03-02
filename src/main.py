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
        self.theme_btn.clicked.connect(self.update_theme)
        self.scale = 0
        self.longitude_value = 0
        self.lattitude_value = 0
        self.theme = 'light'


    def set_map_image(self):
        try:
            self.longitude_value = float(self.longitude.text())
            self.lattitude_value = float(self.width.text())
            self.scale = int(self.coord.text())
        except:
            print("Введите числа")
            return 0

        img = get_map_image(self.longitude_value, self.lattitude_value, self.scale, self.theme)

        if img[0] == 200:
            self.map.setPixmap(QPixmap(img[1])) 
        else:
            print('Не удалось получить изображение карты...')
            print(img)
    
    def keyPressEvent(self, event: QKeyEvent):
        self.setFocus()
        if event.key() == Qt.Key.Key_PageUp:
            if self.scale < 21:
                self.scale += 1 
                self.update_map()

        elif event.key() == Qt.Key.Key_PageDown:
            if self.scale > 0:
                self.scale -= 1
                self.update_map()
        
        elif event.key() == Qt.Key.Key_Up:
            if self.scale > 0:
                self.longitude_value += 0.001
                self.update_map()

        elif event.key() == Qt.Key.Key_Down:
            if self.scale > 0:
                self.longitude_value -= 0.001
                self.update_map()
        
        elif event.key() == Qt.Key.Key_Left:
            if self.scale > 0:
                self.lattitude_value -= 0.001
                self.update_map()

        elif event.key() == Qt.Key.Key_Right:
            if self.scale > 0:
                self.lattitude_value += 0.001
                self.update_map()
    
    def update_theme(self):
        if self.theme == 'light':
            self.theme = 'dark'
            self.theme_btn.setText('Светлая')
        else:
            self.theme = 'light'
            self.theme_btn.setText('Тёмная')

        self.update_map()
    
    def update_map(self):
        img = get_map_image(self.longitude_value, self.lattitude_value, self.scale, self.theme)

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
