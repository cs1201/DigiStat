import matplotlib.pyplot as plot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as PlotCanvas

tempdata = [3, 4, 5, 3, 3, 4, 4, 4, 5, 7, 7, 12, 14 , 5, 6, 12]

plot.plot(tempdata, '-')

plot.show()