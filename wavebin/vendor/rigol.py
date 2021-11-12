"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for oscilloscopes.
"""

from wavebin.vendor import Vendor


class RigolWaveform(Vendor):
    """
    Binary capture file parser for Rigol oscilloscopes
    """

    def __init__(self):
        super(RigolWaveform, self).__init__(
            "Rigol",
            "https://www.rigolna.com",
            "https://web.mit.edu/6.115/www/document/agilent_mso-x_manual.pdf#page=342",
            ["MSO5074"]
        )
