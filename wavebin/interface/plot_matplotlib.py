"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np

from wavebin.vendor import Channel

# https://matplotlib.org/2.0.2/examples/user_interfaces/embedding_in_qt5.html
# https://www.pythonguis.com/tutorials/plotting-matplotlib/
# https://www.geeksforgeeks.org/how-to-embed-matplotlib-graph-in-pyqt5/


class WaveformPlot(FigureCanvasQTAgg):
    """
    Waveform plotting widget using matplotlib backend
    """

    def __init__(self, config: dict, waveform: Channel, colour: tuple):
        """
        Initialise waveform plot

        Args:
            config (dict): Configuration options
            waveform (Channel): Waveform data contained in Channel object
            colour (tuple): Waveform trace colour
        """

        # Initialise parent class
        fig = Figure(figsize=(5, 4), dpi=100, facecolor="black")
        self.axes = fig.add_subplot(111)
        super(WaveformPlot, self).__init__(fig)

        # Set globals
        self.config = config
        self.waveform = waveform
        self.colour = colour

        fig.tight_layout()
        self.axes.set_facecolor((0, 0, 0))
        self.axes.xaxis.set_ticklabels([])
        self.axes.tick_params(axis='y', colors='white')
        self.axes.grid(color="#333")
        self.axes.spines['bottom'].set_color('white')
        self.axes.spines['top'].set_color('white') 
        self.axes.spines['right'].set_color('white')
        self.axes.spines['left'].set_color('white')
        self.axes.plot(self.waveform.trace[0], self.waveform.trace[1])
