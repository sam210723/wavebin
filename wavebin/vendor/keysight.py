"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from wavebin.vendor import Vendor


class KeysightWaveform(Vendor):
    """
    Capture file parser for Keysight and Agilent oscilloscopes

    Args:
        data (bytes, optional): Waveform capture file byte array. Defaults to None.
    """

    def __init__(self, data: bytes = None):
        super(KeysightWaveform, self).__init__(
            "Keysight/Agilent",
            "https://www.keysight.com",
            "https://vksdr.com/download/wavebin/manuals/Agilent%20MSO-X%20User%20Manual.pdf#page=342",
            ["DSO-X 1102G", "MSO-X 4154A"],
            ["*.bin", "*.csv"],
            data
        )
