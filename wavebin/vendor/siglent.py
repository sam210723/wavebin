"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for oscilloscopes.
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
            "https://siglentna.com/operating-tip/oscilloscope-binary-data-format",
            ["SDS2000X Plus"],
            ["*.bin"]
        )
