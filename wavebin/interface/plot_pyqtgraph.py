"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

import numpy as np
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget, PlotItem, ViewBox, AxisItem

from wavebin.vendor import Vendor

# https://pyqtgraph.readthedocs.io/en/latest/plotting.html#organization-of-plotting-classes


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
        pg.setConfigOptions(
            antialias=True,
            useOpenGL=True,
            enableExperimental=True
        )

        # Set globals
        self.config = config
        self.waveform = waveform
        self.colours = [
            (242, 242, 0),
            (100, 149, 237),
            (255, 0, 0),
            (255, 165, 0)
        ]

        # Loop through waveform channels
        for i, c in enumerate(self.waveform.channels):
            # Create plot object
            c.plot = PlotItem()
            view = c.plot.getViewBox()

            # Setup plot styling
            view.setBorder(None)
            view.setMouseMode(ViewBox.PanMode)
            view.setBorder("#969696")
            c.plot.setMenuEnabled(enableMenu=False)
            c.plot.setMouseEnabled(x=True, y=False)
            c.plot.hideButtons()

            # Setup plot limits and axes
            c.plot.setYRange(np.min(c.trace[1]), np.max(c.trace[1]), padding=0.1)
            c.plot.setLimits(
                xMin=np.min(c.trace[0]),
                xMax=np.max(c.trace[0]),
                yMin=np.min(c.trace[1]),
                yMax=np.max(c.trace[1])
            )
            c.plot.showAxes((False, True, True, False))
            c.plot.getAxis('right').setWidth(w=40)
            c.plot.getAxis('right').setLabel(text="Volts", units='V')
            c.plot.getAxis('right').setPen(pg.mkPen(color="#969696", width=1))
            #TODO: Set y axis units

            #FIXME: showGrid() causes zoom to center on X origin rather than mouse location
            #FIXME: See pyqtgraph/pyqtgraph #1937, #1975, #2034 and #2057
            #FIXME: This is fixed in the dev version of pyqtgraph, not yet released
            #FIXME: setuptools can not install deps from GitHub when package is being installed from PyPI
            c.plot.showGrid(x=True, y=True, alpha=0.5)

            # Subsample large waveform captures
            limit = 250000
            if c.points > limit:
                c.plot.setDownsampling(
                    ds=int(c.points/limit),
                    auto=False,
                    mode="subsample"
                )

            # Plot data
            c.plot.plot(
                c.trace[0],
                c.trace[1],
                clear=True,
                #skipFiniteCheck=True,
                pen=pg.mkPen(
                    self.colours[i],
                    width=2     # See pyqtgraph/pyqtgraph #533
                )
            )

            # Link x-axis of all views
            if i != 0: c.plot.setXLink(self.waveform.channels[0].plot.getViewBox())

            # Add plot to layout
            self.addItem(c.plot, row=i+1, col=0, rowspan=1, colspan=1)
        
        # Create time-axis (x)
        self.xaxis = AxisItem(orientation="top")
        self.xaxis.linkToView(self.waveform.channels[0].plot.getViewBox())
        self.xaxis.setLabel(text="Time", units='s')
        self.xaxis.enableAutoSIPrefix(True)
        self.addItem(self.xaxis, row=0, col=0)
