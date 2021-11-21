"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

import struct
from collections import namedtuple

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

        # Parse data when class initialised
        if data: self.parse()
    

    def parse(self) -> bool:
        """
        Parse waveform data

        Returns:
            bool: True if waveform parsed 
        """

        # Parse file header
        if not self.parse_file_header(): return False

        self.parsed = True
        return True


    def parse_file_header(self) -> bool:
        """
        Parse waveform file header

        Returns:
            bool: True if waveform file header parsed ok
        """

        # Unpack file header
        file_header_tuple = namedtuple(
            "FileHeader",
            "magic version size waveforms"
        )
        fields = struct.unpack("2s2s2i", self.data[:0x0C])
        self._file_header = file_header_tuple(*fields)
        self.count = self._file_header.waveforms

        # Check file magic
        if self._file_header.magic != b'AG':
            print("Unknown file format")
            return False

        # Print file header info
        print("File Header:")
        print(f"  - Waveforms: {self.count}")
        print(f"  - File Size: {self.human_format(self._file_header.size, binary=True)}B\n")

        return True
