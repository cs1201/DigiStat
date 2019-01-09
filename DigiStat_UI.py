# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DigiStat.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
import time
from functools import partial
import requests
import json


# Custom Stack Widget with background
class DigiStat_Stack(QtWidgets.QWidget):
    def __init__(self):
        super(DigiStat_Stack, self).__init__()
        self.bg = QtWidgets.QLabel(self)
        self.bg.setGeometry(QtCore.QRect(0,0,320,240))
        self.bg.setPixmap(QtGui.QPixmap(os.getcwd() + "/bg_image.jpg"))

class QLabel_White(QtWidgets.QLabel):
    def __init__(self, parent):
        QtWidgets.QLabel.__init__(self, parent)
        self.setStyleSheet("color : white; font-size : 20pt")

# Main GUI Class
class DigiStat_MainWindow(object):

    room_temp = 23

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 240)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.toolbarwidget = QtWidgets.QWidget(self.centralwidget)
        # self.toolbarwidget.hide()
        
        # TODO: Put Toolbar on it's own widget that can be hidden unless screen is tapped
        # Setup toolbar
        self.config_toolbar()

        # Setup Stacked Widget to hold windows
        self.stack = QtWidgets.QStackedWidget(self.centralwidget)
        self.stack.setGeometry(QtCore.QRect(0, 0, 320, 240))
        self.stack_temp = DigiStat_Stack()
        self.stack_schedule = DigiStat_Stack()
        self.stack_weather = DigiStat_Stack()
        self.stack_calendar = DigiStat_Stack()
        self.stack_settings = DigiStat_Stack()
        
        # Add pages to stack
        self.stack.addWidget(self.stack_temp)
        self.stack.addWidget(self.stack_schedule)
        self.stack.addWidget(self.stack_weather)
        self.stack.addWidget(self.stack_calendar)
        self.stack.addWidget(self.stack_settings)

        # Config all stacks
        self.stack_temp_config()
        self.stack_schedule_config()
        self.stack_calendar_config()
        self.stack_weather_config()

        # Setup time label
        self.timeLabel = QtWidgets.QLabel(self.centralwidget)
        self.timeLabel.setGeometry(QtCore.QRect(10, 290, 50, 20))

        # Settings label on separate stack pane
        self.settingsLabel = QtWidgets.QLabel(self.stack_settings)
        self.settingsLabel.setGeometry(QtCore.QRect(100, 100, 50, 20))

        self.toolbarwidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        # Set temp page as intial window
        self.stack.setCurrentIndex(2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Temp_UP.setText(_translate("MainWindow", "+"))
        self.Temp_DOWN.setText(_translate("MainWindow", "-"))
        self.label.setText(_translate("MainWindow", "{}°C".format(self.room_temp)))
        self.label.setStyleSheet("color: white; font-size: 48pt")
        self.timeLabel.setText(_translate("MainWindow", "00:00"))
        self.timeLabel.setStyleSheet("color: white")
        self.settingsLabel.setText(_translate("MainWindow", "Settings"))
        self.settingsLabel.setStyleSheet("color: white")

    def config_toolbar(self):
        # Add 5 buttons
        self.toolbar_temp = QtWidgets.QPushButton(self.toolbarwidget)
        self.toolbar_schedule = QtWidgets.QPushButton(self.toolbarwidget)
        self.toolbar_weather = QtWidgets.QPushButton(self.toolbarwidget)
        self.toolbar_calendar = QtWidgets.QPushButton(self.toolbarwidget)
        self.toolbar_settings = QtWidgets.QPushButton(self.toolbarwidget)

        # Set geometry
        self.toolbar_temp.setGeometry(QtCore.QRect(0, 0, 64, 40))
        self.toolbar_schedule.setGeometry(QtCore.QRect(64, 0, 64, 40))
        self.toolbar_weather.setGeometry(QtCore.QRect(128, 0, 64, 40))
        self.toolbar_calendar.setGeometry(QtCore.QRect(192, 0, 64, 40))
        self.toolbar_settings.setGeometry(QtCore.QRect(256, 0, 64, 40))

        # Set signal connectors
        self.toolbar_temp.clicked.connect(partial(self.changeStack, 0))
        self.toolbar_schedule.clicked.connect(partial(self.changeStack, 1))
        self.toolbar_weather.clicked.connect(partial(self.changeStack, 2))
        self.toolbar_calendar.clicked.connect(partial(self.changeStack, 3))
        self.toolbar_settings.clicked.connect(partial(self.changeStack, 4))

        
    def changeStack(self, index):
        self.stack.setCurrentIndex(index)

    # CONFIGURE TEMPERATURE CONTROL STACK
    def stack_temp_config(self):

         # Setup temperature buttons
        self.Temp_UP = QtWidgets.QPushButton(self.stack_temp)
        self.Temp_UP.setGeometry(QtCore.QRect(240, 50, 51, 51))
        self.Temp_DOWN = QtWidgets.QPushButton(self.stack_temp)
        self.Temp_DOWN.setGeometry(QtCore.QRect(240, 150, 51, 51))

        # Configure signals for +/- Buttons
        self.Temp_UP.clicked.connect(self.temp_up)
        self.Temp_DOWN.clicked.connect(self.temp_down)

        # Setup temp labels
        self.label = QtWidgets.QLabel(self.stack_temp)
        self.label.setGeometry(QtCore.QRect(100, 70, 100, 110))

    def stack_schedule_config(self):
        # 2 Sliders for start and end time
        return

    # TODO: Calendar should resize when toolbar auto-hides
    def stack_calendar_config(self):
        self.calendar = QtWidgets.QCalendarWidget(self.stack_calendar)
        self.calendar.setGeometry(QtCore.QRect(0, 40, 320, 200))

    def stack_weather_config(self):
        self.weather_icon = QtWidgets.QLabel(self.stack_weather)
        self.weather_icon.setGeometry(QtCore.QRect(20, 40, 150, 150))
        self.weather_icon.setPixmap(QtGui.QPixmap(os.getcwd() + "/curr_weather_icon.png"))
        self.weather_icon.setScaledContents(True)

        self.curr_temp = QLabel_White(self.stack_weather)
        self.max_temp = QLabel_White(self.stack_weather)
        self.min_temp = QLabel_White(self.stack_weather)
        self.curr_temp.setGeometry(QtCore.QRect(160, 80, 150, 50))
        self.max_temp.setGeometry(QtCore.QRect(200, 140, 120, 25))
        self.min_temp.setGeometry(QtCore.QRect(200, 165, 120, 25))
        self.curr_temp.setText("12°C")
        # Override class stylesheet for CurrTemp [maybe can have it's own sub-class?]
        self.curr_temp.setStyleSheet("color: white; font-size: 48pt")
        self.max_temp.setText("Max: 14°C")
        self.min_temp.setText("Min: 5°C")

    # Signal function for Temp Button UP
    def temp_up(self):
        _translate = QtCore.QCoreApplication.translate
        self.room_temp += 1
        self.label.setText(_translate("MainWindow", "{}°C".format(self.room_temp)))
        temp_change(self.room_temp)

    # Signal function for Temp Button UP
    def temp_down(self):
        _translate = QtCore.QCoreApplication.translate
        self.room_temp -= 1
        self.label.setText(_translate("MainWindow", "{}°C".format(self.room_temp)))
        temp_change(self.room_temp)

    # Update time label
    def update_time(self, time_str):
        _translate = QtCore.QCoreApplication.translate
        self.timeLabel.setText(_translate("MainWindow", time_str))

    def update_weather(self, temp, temp_min, temp_max):
        self.weather_icon.setPixmap(QtGui.QPixmap(os.getcwd() + "/curr_weather_icon.png"))
        self.curr_temp.setText("{}°C".format(temp))
        self.min_temp.setText("Min: {}°C".format(temp_min))
        self.max_temp.setText("Max: {}°C".format(temp_max))
        
    def update_target_temp(self, val):
        return
    def update_actual_temp(self, val):
        return

#END OF CLASS

def getWeather():

    city = "Swindon"
    forecast_api_url = "https://api.openweathermap.org/data/2.5/forecast?"
    appkey = "45e2590c09906f78a25e34ba0307ecd7"

    forecast_request = requests.get(forecast_api_url, params={"q":city, "appid": appkey, "units": "metric", "cnt": "5"})
    forecast_data = json.loads(forecast_request.content).get('list')
    print(forecast_data)

    # Over length of list, retreieve min and max temp, average these. and output
    avg_min = 0
    avg_max = 0

    # Get average over 15hrs [5x 3hr increments as determined by cnt param in request]
    for timepoint in range(len(forecast_data)):

        temp_min = float(forecast_data[timepoint].get("main").get("temp_min"))
        temp_max = float(forecast_data[timepoint].get("main").get("temp_max"))

        avg_min = ( avg_min + temp_min ) / (timepoint+1)
        avg_max = ( avg_max + temp_max ) / (timepoint+1)

    # Retrieve Current Temp and Description from content
    temp_curr= float(forecast_data[0].get("main").get("temp"))
    weather_desc = forecast_data[0].get("weather")[0].get("description").title()
    # Get icon code from response content
    icon_code = forecast_data[0].get("weather")[0].get('icon')
    # Download weather icon based on curren weather
    base_icon_url = "http://openweathermap.org/img/w/"
    icon_url = base_icon_url + icon_code + ".png"
    icon_response = requests.get(icon_url)
    if icon_response.status_code == 200:
        with open("curr_weather_icon.png", 'wb') as f:
            f.write(icon_response.content)

    return temp_curr, temp_min, temp_max, weather_desc

def temp_change(curr_temp):
    print(curr_temp)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # MainWindow.showFullScreen()
    ui = DigiStat_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

