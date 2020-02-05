# 
# DigiStat_UI.py
# 
# Created by Connor Stoner - Personal Home Therostat Automation project for Raspberry PI

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
import time
from functools import partial
import requests
import json
import matplotlib.pyplot as plot
import matplotlib.figure as Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import FuncFormatter

plot.rcParams['font.size'] = 4


class ListenerLabel(QtWidgets.QLabel):
    def __init__(self, parent):
        QtWidgets.QLabel.__init__(self, parent)
    
# Custom Stack Widget with background
class DigiStat_Stack(QtWidgets.QWidget):
    def __init__(self):
        super(DigiStat_Stack, self).__init__()
        self.setMouseTracking(True)
        self.bg = ListenerLabel(self)
        self.bg.setGeometry(QtCore.QRect(0,0,320,240))
        self.bg.setPixmap(QtGui.QPixmap(os.getcwd() + "/bg_image.jpg"))
    
    clicked = QtCore.pyqtSignal()
    
    def mousePressEvent(self, event):
        print("MouseClicked!s")
        # if event.button == QtCore.Qt.LeftButton:
        self.click_pos_x = event.globalX()   
        self.click_pos_y = event.globalY()
        self.clicked.emit()

# Custom White Font Label
class QLabel_White(QtWidgets.QLabel):
    def __init__(self, parent):
        QtWidgets.QLabel.__init__(self, parent)
        self.setStyleSheet("color : white; font-size : 20pt")

class TempPlot():
    def __init__(self, parent, data):
        # Intialise plot and formatting. To be redrawn when new data to be shown
    
        # Create figure for plot, add subplot axes and random data
        # Setup plot to fit in window
        fig_w = 320
        fig_h = 200
        fig_dpi = 200

        self.temp_plot_figure = plot.figure(figsize=(fig_w/fig_dpi, fig_h/fig_dpi), dpi=fig_dpi, frameon=False)
        self.temp_plot_figure.patch.set_facecolor("None")
        self.temp_plot= self.temp_plot_figure.add_subplot(111)
        rand_data = [3, 4, 5, 5 , 6]
        self.temp_line, = plot.plot(rand_data, linewidth=0.4, color='g')
        self.temp_plot.set_alpha(0.5)
        self.temp_plot_figure.tight_layout()
        self.temp_plot.yaxis.set_major_formatter(FuncFormatter(lambda x, y: "{}°C".format(x)))
        self.temp_plot.tick_params(axis="y", pad = 1)
        self.temp_plot.tick_params(axis="x", bottom=False, labelbottom=False)

        # Add plot to canvas which can be shown in parent widget
        self.plot_canvas = FigureCanvas(self.temp_plot_figure)
        self.plot_canvas.setParent(parent)
        self.plot_canvas.setGeometry(QtCore.QRect(0, 40, 320, 200))
        self.plot_canvas.setStyleSheet("background-color:transparent;")

    def redraw(self, data):
        print(data)
        self.temp_line.set_ydata(data)
        self.temp_line.set_xdata(range(data))
        # Reset limits
        self.temp_plot.relim()
        self.temp_plot.autoscale()
        self.temp_plot_figure.canvas.draw()
        self.temp_plot_figure.canvas.flush_events()


# Main GUI Class
class DigiStat_MainWindow(object):

    room_temp_val = 23
    toolbarToggle = False
    initial_stack_index = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("DigiStat")
        MainWindow.resize(320, 240)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.toolbarwidget = QtWidgets.QWidget(self.centralwidget)

        # Setup toolbar
        self.config_toolbar()
        self.toolbarAnimation()
    
        # Setup Stacked Widget to hold windows
        self.stack = QtWidgets.QStackedWidget(self.centralwidget)
        self.stack.setGeometry(QtCore.QRect(0, 0, 320, 240))
        self.stack_temp = DigiStat_Stack()
        self.stack_schedule = DigiStat_Stack()
        self.stack_weather = DigiStat_Stack()
        self.stack_calendar = DigiStat_Stack()
        self.stack_settings = DigiStat_Stack()
        # Create plot stack to be accessed through temp stack
        self.stack_plot = DigiStat_Stack()
        
        # Add pages to stack
        self.stack.addWidget(self.stack_temp)
        self.stack.addWidget(self.stack_schedule)
        self.stack.addWidget(self.stack_weather)
        self.stack.addWidget(self.stack_calendar)
        self.stack.addWidget(self.stack_settings)
        self.stack.addWidget(self.stack_plot)

        self.stacks = [self.stack_temp, self.stack_schedule, self.stack_weather, self.stack_calendar, self.stack_settings, self.stack_plot]
        
        for stack in self.stacks:
            stack.clicked.connect(self.autohideToolbar)

        # Config all stacks
        self.stack_temp_config()
        self.stack_schedule_config()
        self.stack_calendar_config()
        self.stack_weather_config()
        self.stack_plot_config()

        # Setup time label
        self.timeLabel = QtWidgets.QLabel(self.centralwidget)
        self.timeLabel.setGeometry(QtCore.QRect(10, 290, 50, 20))

        # Settings label on separate stack pane
        self.settingsLabel = QtWidgets.QLabel(self.stack_settings)
        self.settingsLabel.setGeometry(QtCore.QRect(100, 100, 50, 20))

        self.toolbarwidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        # Set temp page as intial window
        self.stack.setCurrentIndex(self.initial_stack_index)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    # TODO: This function was auto-generated by QtDesigner and not likely to be necessary, can explicitly add this formatting
    # during UI config
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Temp_UP.setText(_translate("MainWindow", "+"))
        self.Temp_DOWN.setText(_translate("MainWindow", "-"))
        self.room_temp.setText(_translate("MainWindow", "{}°C".format(self.room_temp_val)))
        self.room_temp.setStyleSheet("color: white; font-size: 48pt")
        self.timeLabel.setText(_translate("MainWindow", "00:00"))
        self.timeLabel.setStyleSheet("color: white")
        self.settingsLabel.setText(_translate("MainWindow", "Settings"))
        self.settingsLabel.setStyleSheet("color: white")
        
        
    def stack_plot_config(self):

        # REFACTOR THIS PLOT & FIGURE INTO SUBCLASS!
    
        # Create figure for plot, add subplot axes and random data
        # Setup plot to fit in window
        # fig_w = 320
        # fig_h = 200
        # fig_dpi = 200

        # self.temp_plot_figure = plot.figure(figsize=(fig_w/fig_dpi, fig_h/fig_dpi), dpi=fig_dpi, frameon=False)
        # self.temp_plot_figure.patch.set_facecolor("None")
        # self.temp_plot= self.temp_plot_figure.add_subplot(111)
        rand_data = [3, 4, 5, 3, 3, 4, 4, 4, 5, 7, 7, 12, 14 , 5, 6, 12]
        # self.temp_line, = plot.plot(rand_data, linewidth=0.4, color='g')
        # self.temp_plot.set_alpha(0.5)
        # self.temp_plot_figure.tight_layout()
        # self.temp_plot.yaxis.set_major_formatter(FuncFormatter(lambda x, y: "{}°C".format(x)))
        # self.temp_plot.tick_params(axis="y", pad = 1)
        # self.temp_plot.tick_params(axis="x", bottom=False, labelbottom=False)

        # # Add plot to canvas which can be shown in parent widget
        # self.plot_canvas = FigureCanvas(self.temp_plot_figure)
        # self.plot_canvas.setParent(self.stack_plot)
        # self.plot_canvas.setGeometry(QtCore.QRect(0, 40, 320, 200))
        # self.plot_canvas.setStyleSheet("background-color:transparent;")

        self.temp_plot = TempPlot(self.stack_plot, rand_data)

        # Add 3 buttons to update time period over which plot is displayed [3h, 12h, 24h]
        self.plot_button3 = QtWidgets.QPushButton(self.stack_plot)
        self.plot_button12 = QtWidgets.QPushButton(self.stack_plot)
        self.plot_button24 = QtWidgets.QPushButton(self.stack_plot)
        self.plot_button3.setText("3h")
        self.plot_button12.setText("12h")
        self.plot_button24.setText("24h")
        self.plot_button3.setGeometry(QtCore.QRect(80, 200, 60, 30))
        self.plot_button12.setGeometry(QtCore.QRect(150, 200, 60, 30))
        self.plot_button24.setGeometry(QtCore.QRect(220, 200, 60, 30))
        self.plot_buttons = [self.plot_button3, self.plot_button12, self.plot_button24]

        for idx in range(len(self.plot_buttons)):
            self.plot_buttons[idx].clicked.connect(partial(self.rescaleTempPlot, idx))


    def rescaleTempPlot(self, idx):
        print("Trying to rescale plot")
        rand_data = [[3, 4, 5, 7, 8 ], [1,1,2], [5,6,3, 4, 3, 3,3 ,3 ,3 ]]
        self.temp_plot.redraw(rand_data[idx])


    def toolbarAnimation(self):
        
        self.toolbar_show_animation = QtCore.QPropertyAnimation(self.toolbarwidget, b"geometry")
        self.toolbar_show_animation.setDuration(600)
        self.toolbar_show_animation.setStartValue(QtCore.QRect(0, -40, 320, 40))
        self.toolbar_show_animation.setEndValue(QtCore.QRect(0,0, 320, 40))

        self.toolbar_hide_animation = QtCore.QPropertyAnimation(self.toolbarwidget, b"geometry")
        self.toolbar_hide_animation.setDuration(600)
        self.toolbar_hide_animation.setStartValue(QtCore.QRect(0, 0, 320, 40))
        self.toolbar_hide_animation.setEndValue(QtCore.QRect(0, -40, 320, 40))


    def showToolbar(self):
        self.toolbarwidget.setGeometry(QtCore.QRect(0,0,320,40))

    def config_toolbar(self):
        # Add 5 buttons
        self.toolbarwidget.setGeometry(QtCore.QRect(0, -40, 320, 40))
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

    def autohideToolbar(self):
        if not self.toolbarToggle:
            self.toolbar_show_animation.start()
            QtCore.QTimer.singleShot(5000, self.hideToolbar)
            self.toolbarToggle = not self.toolbarToggle
            
    def hideToolbar(self):
        self.toolbar_hide_animation.start()
        self.toolbarToggle = not self.toolbarToggle

    def changeStack(self, index):
        
        # If current index before request to change is plot or calendar then trigger hide
        if self.stack.currentIndex() in [3, 5]:
            print("index was 3 or 5")
            self.toolbar_hide_animation.start()

        # Update current stack to be shown
        self.stack.setCurrentIndex(index)

        # Make sure toolbar remains shown if plot or calendar stack is selected
        if index == 5 or index == 3:
            self.showToolbar()
            # self.toolbarToggle = not self.toolbarToggle

        # If weather stack is selected, then trigger API call to get current data
        if index == 2:
            getWeather()

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
        self.room_temp = QLabel_White(self.stack_temp)
        self.room_temp.setGeometry(QtCore.QRect(100, 70, 100, 120))
        self.room_temp.setAlignment(QtCore.Qt.AlignCenter)
        self.room_temp.setStyleSheet("background-color: green;")

        # Add button to show plot stack page
        self.plot_show = QtWidgets.QPushButton(self.stack_temp)
        self.plot_show.setGeometry(QtCore.QRect(10, 200, 30, 30))
        self.plot_show.clicked.connect(partial(self.changeStack, 5))

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
        self.weather_desc = QLabel_White(self.stack_weather)
        self.curr_temp.setGeometry(QtCore.QRect(160, 80, 150, 50))
        self.max_temp.setGeometry(QtCore.QRect(200, 140, 120, 25))
        self.min_temp.setGeometry(QtCore.QRect(200, 165, 120, 25))
        self.weather_desc.setGeometry(QtCore.QRect(50,180, 200, 25))
        self.curr_temp.setText("12°C")
        # Override class stylesheet for CurrTemp [maybe can have it's own sub-class?]
        self.curr_temp.setStyleSheet("color: white; font-size: 48pt")
        self.max_temp.setText("Max: 14°C")
        self.min_temp.setText("Min: 5°C")

        # Refresh button to force weather request and update
        self.weather_refresh = QtWidgets.QPushButton(self.stack_weather)
        self.weather_refresh.setGeometry(QtCore.QRect(200, 200, 40, 40))
        self.weather_refresh.clicked.connect(getWeather)

    # Signal function for Temp Button UP
    def temp_up(self):
        _translate = QtCore.QCoreApplication.translate
        self.room_temp_val += 1
        self.room_temp.setText(_translate("MainWindow", "{}°C".format(self.room_temp_val)))
        temp_change(self.room_temp_val)

    # Signal function for Temp Button UP
    def temp_down(self):
        _translate = QtCore.QCoreApplication.translate
        self.room_temp_val -= 1
        self.room_temp.setText(_translate("MainWindow", "{}°C".format(self.room_temp_val)))
        temp_change(self.room_temp_val)

    # Update time label
    def update_time(self, time_str):
        _translate = QtCore.QCoreApplication.translate
        self.timeLabel.setText(_translate("MainWindow", time_str))

    def update_weather(self, temp, temp_min, temp_max, weather_desc):
        self.weather_icon.setPixmap(QtGui.QPixmap(os.getcwd() + "/curr_weather_icon.png"))
        self.curr_temp.setText("{:-.1f}°C".format(temp))
        self.min_temp.setText("Min: {:-.1f}°C".format(temp_min))
        self.max_temp.setText("Max: {:-.1f}°C".format(temp_max))
        self.weather_desc.setText("{}".format(weather_desc))
        
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

    # Over length of list, retreieve min and max temp, average these. and output
    avg_min = 0
    avg_max = 0

    # Get average over 15hrs [5x 3hr increments as determined by cnt param in request]
    # for timepoint in range(len(forecast_data)):

    #     temp_min = float(forecast_data[timepoint].get("main").get("temp_min"))
    #     temp_max = float(forecast_data[timepoint].get("main").get("temp_max"))

    #     avg_min = ( avg_min + temp_min ) / (timepoint+1)
    #     avg_max = ( avg_max + temp_max ) / (timepoint+1)

    avg_min = float(forecast_data[0].get("main").get("temp_min"))
    avg_max = float(forecast_data[0].get("main").get("temp_max"))

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

    ui.update_weather(temp_curr, avg_min, avg_max, weather_desc)

def temp_change(curr_temp):
    print(curr_temp)

# Function to be called by scheduler. Measure temp from sensor and activate heating circuit if below target temp
# 
def data_update():
    # Get current temperature from sensor
    return    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # MainWindow.showFullScreen()
    ui = DigiStat_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

