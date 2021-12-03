"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg

from wavebin.vendor import Vendor


class WaveformPlot(GraphicsLayoutWidget):
    """
    Waveform plotting widget using PyQtGraph backend
    """

    def __init__(self, config: dict, waveform: Vendor) -> None:
        """
        Initialise waveform plot

        Args:
            config (dict): Configuration options
            waveform (Vendor): Waveform data in Vendor-based class
        """

        # Initialise parent class
        super(WaveformPlot, self).__init__()

        # Set globals
        self.config = config
        self.waveform = waveform
        self.colours = [
            (242, 242, 0),
            (100, 149, 237),
            (255, 0, 0),
            (255, 165, 0)
        ]
