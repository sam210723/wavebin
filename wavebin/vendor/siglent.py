"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from wavebin.vendor import Vendor


class SiglentWaveform(Vendor):
    """
    Capture file parser for Siglent oscilloscopes
    """

    def __init__(self):
        super(SiglentWaveform, self).__init__(
            "Siglent",
            "https://siglentna.com",
            "https://vksdr.com/download/wavebin/manuals/Siglent%20Oscilloscope%20Binary%20Data%20Format.pdf#page=3",
            ["SDS2000X Plus"],
            ["*.bin"]
        )
