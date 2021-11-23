"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from wavebin.vendor import Channel


class WaveformPlot():
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
        super(WaveformPlot, self).__init__()

        # Set globals
        self.config = config
        self.waveform = waveform
        self.colour = colour
