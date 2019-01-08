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

# Custom Stack Widget with background
class DigiStat_Stack(QtWidgets.QWidget):
    def __init__(self):
        super(DigiStat_Stack, self).__init__()
        self.bg = QtWidgets.QLabel(self)
        self.bg.setGeometry(QtCore.QRect(0,0,320,240))
        self.bg.setPixmap(QtGui.QPixmap(os.getcwd() + "/bg_image.jpg"))


# Main GUI Class
class DigiStat_MainWindow(object):

    temp = 23

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 240)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Setup toolbar
        self.config_toolbar()

        # Setup Stacked Widget to hold windows
        self.stack = QtWidgets.QStackedWidget(self.centralwidget)
        self.stack.setGeometry(QtCore.QRect(0, 40, 320, 200))
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

        # Setup time label
        self.timeLabel = QtWidgets.QLabel(self.centralwidget)
        self.timeLabel.setGeometry(QtCore.QRect(10, 290, 50, 20))

        # Settings label on separate stack pane
        self.settingsLabel = QtWidgets.QLabel(self.stack_settings)
        self.settingsLabel.setGeometry(QtCore.QRect(100, 100, 50, 20))

        MainWindow.setCentralWidget(self.centralwidget)

        # Set temp page as intial window
        self.stack.setCurrentIndex(0)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Temp_UP.setText(_translate("MainWindow", "+"))
        self.Temp_DOWN.setText(_translate("MainWindow", "-"))
        self.label.setText(_translate("MainWindow", "{}degC".format(self.temp)))
        self.label.setStyleSheet("color: white")
        self.timeLabel.setText(_translate("MainWindow", "00:00"))
        self.timeLabel.setStyleSheet("color: white")
        self.settingsLabel.setText(_translate("MainWindow", "Settings"))
        self.settingsLabel.setStyleSheet("color: white")

    def config_toolbar(self):
        # Add 5 buttons
        self.toolbar_temp = QtWidgets.QPushButton(self.centralwidget)
        self.toolbar_schedule = QtWidgets.QPushButton(self.centralwidget)
        self.toolbar_weather = QtWidgets.QPushButton(self.centralwidget)
        self.toolbar_calendar = QtWidgets.QPushButton(self.centralwidget)
        self.toolbar_settings = QtWidgets.QPushButton(self.centralwidget)

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
        self.Temp_UP.setGeometry(QtCore.QRect(240, 20, 51, 51))
        self.Temp_DOWN = QtWidgets.QPushButton(self.stack_temp)
        self.Temp_DOWN.setGeometry(QtCore.QRect(240, 110, 51, 51))

        # Configure signals for +/- Buttons
        self.Temp_UP.clicked.connect(self.temp_up)
        self.Temp_DOWN.clicked.connect(self.temp_down)

        # Setup temp labels
        self.label = QtWidgets.QLabel(self.stack_temp)
        self.label.setGeometry(QtCore.QRect(120, 60, 91, 71))
        self.label.setObjectName("label")


    def stack_schedule_config(self):
        # 2 Sliders for start and end time
        return

    def stack_calendar_config(self):
        self.calendar = QtWidgets.QCalendarWidget(self.stack_calendar)
        self.calendar.setGeometry(QtCore.QRect(0, 0, 320, 200))

    # Signal function for Temp Button UP
    def temp_up(self):
        _translate = QtCore.QCoreApplication.translate
        self.temp += 1
        self.label.setText(_translate("MainWindow", "{}degC".format(self.temp)))
        temp_change(self.temp)

    # Signal function for Temp Button UP
    def temp_down(self):
        _translate = QtCore.QCoreApplication.translate
        self.temp -= 1
        self.label.setText(_translate("MainWindow", "{}degC".format(self.temp)))
        temp_change(self.temp)

    # Update time label
    def update_time(self, time_str):
        _translate = QtCore.QCoreApplication.translate
        self.timeLabel.setText(_translate("MainWindow", time_str))

    def update_target_temp(self, val):
        return
    def update_actual_temp(self, val):
        return

#END OF CLASS

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

