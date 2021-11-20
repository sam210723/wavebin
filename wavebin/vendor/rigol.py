"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from wavebin.vendor import Vendor


class RigolWaveform(Vendor):
    """
    Capture file parser for Rigol oscilloscopes

    Args:
        data (bytes, optional): Waveform capture file byte array. Defaults to None.
    """

    def __init__(self, data: bytes = None):
        super(RigolWaveform, self).__init__(
            "Rigol",
            "https://www.rigolna.com",
            "https://vksdr.com/download/wavebin/manuals/Rigol%20MSO8000%20User%20Manual.pdf#page=277",
            ["MSO5074"],
            ["*.bin", "*.wfm", "*.csv"],
            data
        )
