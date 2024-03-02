"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from collections import namedtuple
import logging
import numpy as np
import struct

from wavebin.vendor import Vendor


class SiglentWaveform(Vendor):
    """
    Capture file parser for Siglent oscilloscopes

    Args:
        data (bytes, optional): Waveform capture file byte array. Defaults to None.
    """

    def __init__(self, data: bytes = None):
        super(SiglentWaveform, self).__init__(
            "Siglent",
            "https://siglentna.com",
            "https://wavebin.app/cloud/manuals/Siglent%20Oscilloscope%20Binary%20Data%20Format.pdf#page=3",
            ["SDS2000X Plus"],
            ["*.bin"],
            data
        )
