"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for oscilloscopes.
"""

from wavebin.vendor import Vendor


class KeysightWaveform(Vendor):
    """
    Binary capture file parser for Keysight and Agilent oscilloscopes
    """

    def __init__(self):
        super(KeysightWaveform, self).__init__(
            "Keysight / Agilent",
            "https://www.keysight.com",
            "https://web.mit.edu/6.115/www/document/agilent_mso-x_manual.pdf#page=342",
            ["DSO-X 1102G", "MSO-X 4154A"]
        )
