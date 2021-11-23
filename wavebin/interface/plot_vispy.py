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
        views = []
        for i, c in enumerate(self.waveform.channels):
            views.append(self.grid.add_view(row=i, col=0, border_color='#333'))
            scene.Line(np.swapaxes(c.trace, 0, 1), parent=views[i].scene, color=self.colours[i])
            #scene.visuals.GridLines(parent=views[i].scene)
            views[i].camera = 'panzoom'
            views[i].camera.reset()
            views[i].camera.set_range()
            
            if i != 0: views[i].camera.link(views[0].camera, axis="x")

        # Camera linking https://github.com/vispy/vispy/blob/main/vispy/scene/cameras/base_camera.py#L383
