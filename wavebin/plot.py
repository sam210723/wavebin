"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

from pyqtgraph import PlotWidget
import pyqtgraph as qtp

class QtPlot(PlotWidget):
    def __init__(self, config):
        self.config = config

        self.log("Initialising plot widget")
        super().__init__()

        # Enable/Disable OpenGL
        if self.config['opengl']:
            qtp.setConfigOptions(useOpenGL=True)
            self.line_width = 2
        else:
            qtp.setConfigOptions(useOpenGL=False)
            self.line_width = 1    # See https://github.com/pyqtgraph/pyqtgraph/issues/533

        self.setAntialiasing(True)
        self.setLabel('bottom', "Time", units='s')
        self.showGrid(x=True, y=True, alpha=1.0)
        self.setMouseEnabled(x=True, y=False)


    def update(self):
        self.log("Updating plot")


    def log(self, msg):
        if self.config['verbose']: print(msg)
