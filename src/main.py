import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QLineEdit, QPushButton, QLabel
from PyQt6.QtGui import QPixmap, QKeyEvent, QIcon
from PyQt6 import uic
from PyQt6.QtCore import Qt
from utils import *
from io import BytesIO


class Main(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./data/design.ui", self)
        self.setWindowTitle("Карта")

        # Добавленные элементы
        self.search_input = QLineEdit(self)
        self.search_input.setStyleSheet("background-color: white;")
        self.search_input.setGeometry(42, 520, 317, 35)

        self.search_label = QLabel(self)
        self.search_label.setText("Введите объект:")
        self.search_label.setStyleSheet(
            "color: white; font-size: 20pt; font: large 'Times New Roman'"
        )
        self.search_label.setGeometry(42, 480, 317, 25)

        self.search_button = QPushButton(self)
        self.search_button.setText("Найти")
        self.search_button.setStyleSheet(
            "background-color: white; color: black; font-size: 17pt; font: large 'Times New Roman'"
        )
        self.search_button.setGeometry(42, 570, 230, 80)

        self.reset_button = QPushButton(self)
        self.reset_button.setStyleSheet("background-color: white;")
        self.reset_button.setGeometry(280, 570, 80, 80)
        self.reset_button.setIcon(QIcon('data/icons/trash-can.png'))

        self.ready_btn.clicked.connect(self.set_map_image)
        self.theme_btn.clicked.connect(self.update_theme)
        self.reset_button.clicked.connect(self.reset)
        self.search_button.clicked.connect(self.search_toponym)

        self.scale = 0
        self.longitude_value = 0
        self.lattitude_value = 0
        self.theme = "light"
        self.point_status = False
        self.address_label = self.findChild(QLabel, "address_label")  # Находим добавленный QLabel

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
            print("Не удалось получить изображение карты...")
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
                self.lattitude_value += 0.001
                self.update_map()

        elif event.key() == Qt.Key.Key_Down:
            if self.scale > 0:
                self.lattitude_value -= 0.001
                self.update_map()

        elif event.key() == Qt.Key.Key_Left:
            if self.scale > 0:
                self.longitude_value -= 0.001
                self.update_map()

        elif event.key() == Qt.Key.Key_Right:
            if self.scale > 0:
                self.longitude_value += 0.001
                self.update_map()
        elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.search_toponym()

    def update_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.theme_btn.setText("Светлая")
        else:
            self.theme = "light"
            self.theme_btn.setText("Тёмная")

        self.update_map()

    def update_map(self):
        img = get_map_image(
            self.longitude_value, self.lattitude_value, self.scale, self.theme)

        if img[0] == 200:
            if not self.point_status:
                self.map.setPixmap(QPixmap(img[1]))
            else:
                image = Image.open(img[1])
                image = draw_point(image)
                buffer = BytesIO()
                image.save(buffer, format="PNG")
                pixmap = QPixmap()
                pixmap.loadFromData(buffer.getvalue())
                self.map.setPixmap(pixmap)
                self.map.repaint()
        else:
            print("Не удалось получить изображение карты...")
            print(img)

    def search_toponym(self):
        toponym = self.search_input.text()

        if toponym:
            result = get_toponym_ll(toponym)
            if result:
                self.longitude_value, self.lattitude_value = float(result[0]), float(result[1])
                self.scale = 17
                self.point_status = True
                
                address = self.get_full_address(toponym)
                self.address_label.setText(f"Адрес: {address}")

        self.update_map()

    def get_full_address(self, toponym):
        geocoder_params = {
            "apikey": geocoder_apikey,
            "geocode": toponym,
            "format": "json"
        }

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            return toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        return "Адрес не найден"

    def reset(self):
        self.map.clear()
        self.search_input.clear()
        self.address_label.setText("Адрес: ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
