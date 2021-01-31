"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

import numpy as np
from pyqtgraph import PlotWidget
import pyqtgraph as pg

class QtPlot(PlotWidget):
    def __init__(self, config):
        self.config = config

        self.log("Initialising plot widget")
        super().__init__()

        # Enable/Disable OpenGL
        if self.config['opengl']:
            pg.setConfigOptions(useOpenGL=True)
            self.config['line_width'] = 2
        else:
            pg.setConfigOptions(useOpenGL=False)
            self.config['line_width'] = 1    # See https://github.com/pyqtgraph/pyqtgraph/issues/533

        # Set plot properties
        self.view = self.getViewBox()
        self.setAntialiasing(True)
        self.setLabel('bottom', "Time", units='s')
        self.showGrid(x=True, y=True, alpha=1.0)
        self.setMouseEnabled(x=True, y=False)


    def update(self):
        self.log("Updating plot")

        # Remove old traces
        self.clear()

        # Loop through waveforms and render traces
        for i, w in enumerate(self.waveforms): 
            # Generate X points
            start = w['header'].x_d_origin
            stop = w['header'].x_d_origin + w['header'].x_d_range
            x = np.linspace(start, stop, w['header'].points)

            self.plot(
                x,
                w['data'],
                pen=pg.mkPen(
                    self.config['colours'][i],
                    width=self.config['line_width']
                )
            )


    def log(self, msg):
        if self.config['verbose']: print(msg)
