"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

import numpy as np
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget, PlotItem, ViewBox, AxisItem

from wavebin.vendor import Vendor, Unit, UnitAbbr

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
        self.axis_pen = pg.mkPen(color="#969696", width=1)

        # Loop through waveform channels
        for i, c in enumerate(self.waveform.channels):
            last = i == len(self.waveform.channels) - 1
            # Create plot object
            c.plot = PlotItem()
            view = c.plot.getViewBox()

            # Setup plot styling
            view.setBorder(None)
            view.setMouseMode(ViewBox.PanMode)
            view.setBorder("#969696")
            c.plot.setMenuEnabled(False)
            c.plot.setMouseEnabled(x=True, y=False)
            c.plot.hideButtons()

            # Setup plot limits
            c.plot.setYRange(np.min(c.trace[1]), np.max(c.trace[1]), padding=0.1)
            c.plot.setLimits(
                xMin=np.min(c.trace[0]),
                xMax=np.max(c.trace[0]),
                yMin=np.min(c.trace[1]),
                yMax=np.max(c.trace[1])
            )

            # Setup plot axes
            c.plot.showAxes((True, False, False, True))
            c.plot.getAxis('bottom').setHeight(40)
            c.plot.getAxis('bottom').setLabel(text=c.x_unit.name, units=UnitAbbr(c.x_unit.value).name)
            c.plot.getAxis('bottom').setPen(self.axis_pen)
            c.plot.getAxis('left').setWidth(40)
            c.plot.getAxis('left').setLabel(text=c.y_unit.name, units=UnitAbbr(c.y_unit.value).name)
            c.plot.getAxis('left').setPen(self.axis_pen)

            #FIXME: showGrid() causes zoom to center on X origin rather than mouse location
            #FIXME: See pyqtgraph/pyqtgraph #1937, #1975, #2034 and #2057
            #FIXME: This is fixed in the dev version of pyqtgraph, not yet released
            #FIXME: setuptools can not install deps from GitHub when package is being installed from PyPI
            c.plot.showGrid(x=True, y=True, alpha=0.75)

            # Subsample large waveform captures
            limit = 250000
            if c.points > limit:
                print(f"Subsampling channel with more than {limit/1000:.0f}k points")
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
                skipFiniteCheck=True,
                pen=pg.mkPen(
                    self.colours[i],
                    width=2     # See pyqtgraph/pyqtgraph #533
                )
            )

            # Link views and add to layout
            if i != 0: c.plot.setXLink(self.waveform.channels[0].plot.getViewBox())
            self.addItem(c.plot, row=i, col=0, rowspan=1, colspan=1)
