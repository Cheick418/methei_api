import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel,
                             QVBoxLayout, QPushButton, QLineEdit)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QBuffer, QByteArray
import requests


def get_image(url):
    url = f"https:{url}"
    response = requests.get(url)
    if response.status_code == 200:
        image_data = QByteArray(response.content)
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        return pixmap


def get_weather_infos(country):
    api_key = "152ad6d6938147bfb9d72129241911"
    request_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={country}&aqi=no"

    response = requests.get(request_url)
    if response.status_code == 200:
        response = response.json()
        temperature = response.get("current").get("temp_c")
        state = response.get("current").get("condition").get("text")
        icon_url = response.get("current").get("condition").get("icon")
        return [temperature, state, icon_url]
    else:
        return None



class Weather(QWidget):
    def __init__(self):
        super().__init__()
        self.prompt = QLabel("Enter city name:")
        self.line = QLineEdit()
        self.get_weatherb = QPushButton("get weather")
        self.icon = QLabel()
        self.temperature = QLabel()
        self.state = QLabel()

        self.ui()

    def ui(self):
        self.setWindowTitle("weather")
        vb = QVBoxLayout(self)

        vb.addWidget(self.prompt)
        vb.addWidget(self.line)
        vb.addWidget(self.get_weatherb)
        vb.addWidget(self.temperature)
        vb.addWidget(self.icon)
        vb.addWidget(self.state)

        self.prompt.setAlignment(Qt.AlignCenter)
        self.line.setAlignment(Qt.AlignCenter)
        self.icon.setAlignment(Qt.AlignCenter)
        self.temperature.setAlignment(Qt.AlignCenter)
        self.state.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
            QLabel{
                font-size:30px;
                font-family:Arial;
            }
            QLineEdit{
                font-size:40px;
                }
        
        """)

        self.setLayout(vb)
        self.get_weatherb.clicked.connect(self.get_weather)

    def get_weather(self):
        data = get_weather_infos(self.line.text())
        if data:
            temperature, info, icon_url = data[0], data[1], data[2]
            self.temperature.setStyleSheet("color:black;")
            self.temperature.setText(f"{temperature}°C")
            self.state.setText(info)
            pixmap = get_image(icon_url)
            self.icon.setPixmap(pixmap)
            self.icon.show()
        else:
            self.temperature.setText(f"error in input")
            self.temperature.setStyleSheet("color:red;")
            self.state.setText("")
            self.icon.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather = Weather()
    weather.show()
    sys.exit(app.exec_())


