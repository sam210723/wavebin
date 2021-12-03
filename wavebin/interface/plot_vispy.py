"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from vispy import scene
import numpy as np

from wavebin.vendor import Vendor

# https://vispy.org/gallery/scene/axes_plot.html


class WaveformPlot(scene.SceneCanvas):
    """
    Waveform plotting widget using vispy backend
    """

    def __init__(self, config: dict, waveform: Vendor):
        """
        Initialise waveform plot

        Args:
            config (dict): Configuration options
            waveform (Vendor): Waveform data in Vendor-based class
        """

        # Initialise parent class
        super(WaveformPlot, self).__init__(keys="interactive")

        # Set globals
        self.unfreeze()
        self.config = config
        self.waveform = waveform
        self.colours = [
            (0.95, 0.95, 0.0),
            (0.39, 0.58, 0.93),
            (1.0, 0.0, 0.0),
            (1.0, 0.65, 0.0)
        ]

        # Setup grid
        self.grid = self.central_widget.add_grid()
        self.grid.spacing = 0
        self.grid.margin = 0

        # Loop through waveform channels
        self.views = []
        for i, c in enumerate(self.waveform.channels):
            self.views.append(self.grid.add_view(
                row=i,
                col=0,
                border_color='#000'
            ))

            scene.Line(
                np.swapaxes(c.trace, 0, 1),
                parent=self.views[i].scene,
                color=self.colours[i]
            )

            self.views[i].camera = 'panzoom'
            self.views[i].camera.set_range(
                x=(c.trace[0].min(), c.trace[0].max()),
                y=(c.trace[1].min(), c.trace[1].max())
            )
            scene.visuals.GridLines(parent=self.views[i].scene)
            
            # Link cameras (except 0 to itself)
            if i != 0: self.views[i].camera.link(self.views[0].camera, axis="x")

            # 
            if i == len(self.waveform.channels) - 1:
                xaxis = scene.AxisWidget(
                    orientation='bottom',
                    #axis_label='X Axis',
                    axis_font_size=16,
                    #axis_label_margin=5,
                    tick_label_margin=10
                )
                xaxis.height_max = 20
                self.grid.add_widget(xaxis, row=i+1, col=0)
