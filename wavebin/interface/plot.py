"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

import logging
import numpy as np
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget, PlotItem, ViewBox, AxisItem

from wavebin.config import config
from wavebin.vendor import Vendor, Unit, UnitAbbr

# https://pyqtgraph.readthedocs.io/en/latest/plotting.html#organization-of-plotting-classes


class WaveformPlot(GraphicsLayoutWidget):
    """
    Waveform plotting widget using PyQtGraph backend
    """

    def __init__(self, waveform: Vendor) -> None:
        """
        Initialise waveform plot

        Args:
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
        self.waveform = waveform
        self.colours = [
            (242, 242, 0),
            (100, 149, 237),
            (255, 0, 0),
            (255, 165, 0)
        ]
        self.axis_pen = pg.mkPen(color="#969696", width=1)
        self.axis_style = {
            'color': '#969696',
            'font-family': 'Roboto',
            'font-size': '14px',
            'font-weight': 'bold'
        }
        self.filled = False

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
            c.plot.showGrid(x=True, y=True, alpha=0.75)
            self.setup_axis(c.plot.getAxis('bottom'), c.x_unit)
            self.setup_axis(c.plot.getAxis('left'), "DIGITAL" if c.is_digital else c.y_unit)

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
                    width=2
                )
            )

            # Link views and add to layout
            if i != 0: c.plot.setXLink(self.waveform.channels[0].plot.getViewBox())
            self.addItem(c.plot, row=i, col=0, rowspan=1, colspan=1)

            # Add infinite crosshair
            c.crosshair = [
                pg.InfiniteLine(angle=90, movable=False),
                pg.InfiniteLine(angle=0, movable=False)
            ]
            for line in c.crosshair:
                line.setPen("#FFFFFF")
                view.addItem(line, ignoreBounds=True)
            self.proxy = pg.SignalProxy(self.sceneObj.sigMouseMoved, rateLimit=60, slot=self.update_crosshair)
            #TODO: Move signal to parent widget (QWidget:wavebin.interface.window.widget)


    def setup_axis(self, axis: AxisItem, unit: Unit) -> None:
        """
        Setup styling and options for plot AxisItems

        Args:
            axis (AxisItem): Axis object to configure
            unit (Unit | str): Axis measurement unit
        """

        if axis.orientation in ["left", "right"]:
            axis.setWidth(50)
        elif axis.orientation in ["top", "bottom"]:
            axis.setHeight(40)

        axis.setPen(self.axis_pen)

        if type(unit) == Unit:
            axis.setLabel(
                text=unit.name,
                units=UnitAbbr(unit.value).name,
                **self.axis_style
            )
        elif type(unit) == str:
            axis.setLabel(
                text=unit,
                units=None,
                **self.axis_style
            )


    def toggle_trace_fill(self):
        """
        Toggle filled area under waveform traces
        """

        for i, c in enumerate(self.waveform.channels):
            c.plot.plot(
                c.trace[0],
                c.trace[1],
                clear=True,
                skipFiniteCheck=True,
                pen=pg.mkPen(
                    self.colours[i],
                    width=2
                ),
                fillLevel=0,
                brush=(*self.colours[i], 32) if not self.filled else None
            )
        self.filled = not self.filled


    def update_crosshair(self, e):
        """
        Update infinite line crosshair position on plots
        """

        for i, c in enumerate(self.waveform.channels):
            if c.plot.sceneBoundingRect().contains(e[0]):
                # Set crosshair position within plot
                mousePoint = c.plot.vb.mapSceneToView(e[0])
                c.crosshair[0].setPos(mousePoint.x())
                c.crosshair[1].setPos(mousePoint.y())
            else:
                # Move lines far off-screen
                c.crosshair[0].setPos(1e9)
                c.crosshair[1].setPos(1e9)
