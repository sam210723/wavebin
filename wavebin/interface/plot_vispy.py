"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from vispy import scene
import numpy as np

from wavebin.vendor import Channel

# https://vispy.org/gallery/scene/axes_plot.html


class WaveformPlot(scene.SceneCanvas):
    """
    Waveform plotting widget using vispy backend
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
        super(WaveformPlot, self).__init__(keys="interactive")

        # Set globals
        self.unfreeze()
        self.config = config
        self.waveform = waveform
        self.colour = colour

        grid = self.central_widget.add_grid(margin=10)
        grid.spacing = 0

        view = grid.add_view(row=1, col=1, border_color='white')
        self.waveform._trace = np.swapaxes(self.waveform.trace, 0, 1)
        line = scene.Line(self.waveform.trace, parent=view.scene)

        view.camera = 'panzoom'
        view.camera.set_range()
