"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for oscilloscopes.
"""

from wavebin.vendor import Vendor


class KeysightWaveform(Vendor):
    """
    Capture file parser for Keysight and Agilent oscilloscopes
    """

    def __init__(self):
        super(KeysightWaveform, self).__init__(
            "Keysight / Agilent",
            "https://www.keysight.com",
            "https://vksdr.com/download/wavebin/Agilent%20MSO-X%20User%20Manual.pdf",
            ["DSO-X 1102G", "MSO-X 4154A"],
            ["*.bin", "*.csv"]
        )
