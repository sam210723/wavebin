"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

from enum import Enum
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

            if self.config['filter'] == 0:
                y = w['data']
            elif self.config['filter'] == 1:
                #TODO: Filter waveform
                y = w['data']
            else:
                self.log(f"Invalid filter selection: {self.config['filter']}")
                y = w['data']

            self.plot(
                x,
                y,
                pen=pg.mkPen(
                    self.config['colours'][i],
                    width=self.config['line_width']
                )
            )
        
        # Set left Y axis label
        self.setLabel(
            'left',
            Units(self.waveforms[0]['header'].y_units).name,
            units=UnitAbbr(self.waveforms[0]['header'].y_units).name
        )
    

    def savitzky_golay(self, points):
        #TODO: Implement filter
        return


    def log(self, msg):
        if self.config['verbose']: print(msg)


class Units(Enum):
    """
    Waveform units
    """

    UNKNOWN     = 0
    Volts       = 1
    Seconds     = 2
    Constant    = 3
    Amps        = 4
    Decibels    = 5
    Hertz       = 6


class UnitAbbr(Enum):
    """
    Waveform unit abbreviations
    """

    UNKNOWN     = 0
    V           = 1
    s           = 2
    C           = 3
    A           = 4
    dB          = 5
    Hz          = 6
