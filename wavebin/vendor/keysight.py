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

        # Loop through waveforms
        for i in range(self.count):
            print(f"Waveform {i + 1}:")

            # Parse waveform header
            header = self.parse_waveform_header()
            self.channels.append({
                "header": header,
                "data": None
            })

        self.parsed = True
        return True


    def parse_file_header(self) -> bool:
        """
        Parse waveform file header

        Returns:
            bool: True if waveform file header parsed
        """

        # Unpack file header
        file_header_tuple = namedtuple(
            "FileHeader",
            "magic version size waveforms"
        )
        fields = struct.unpack("2s2s2i", self.data[:0x0C])
        self.offset = 0x0C
        self._file_header = file_header_tuple(*fields)
        self.count = self._file_header.waveforms

        # Check file magic
        if self._file_header.magic != b'AG':
            print("Unknown file format")
            return False

        # Print file header info
        print(
            f"Found {self.count} waveform{'s' if self.count > 1 else ''}" +
            f" in {self.human_format(self._file_header.size, binary=True, unit='B')}\n"
        )

        return True


    def parse_waveform_header(self) -> namedtuple:
        """
        Parse waveform header

        Returns:
            namedtuple: Parsed waveform header as namedtuple
        """

        # Unpack waveform header
        length = self.data[self.offset]
        waveform_header_tuple = namedtuple(
            "WaveformHeader",
            "size wave_type buffers points average " +
            "x_d_range x_d_origin x_increment x_origin " +
            "x_units y_units date time frame label " +
            "time_tags segment"
        )
        fields = struct.unpack("5if3d2i16s16s24s16sdI", self.data[self.offset : self.offset + length])
        self.offset += length
        header = waveform_header_tuple(*fields)

        # Format sample rate and duration
        self.sample_rate = self.human_format(1 / header.x_increment, unit="S/s")
        self.duration = self.human_format(header.x_d_range, unit="s")

        print(f"  - Sample Points:  {self.human_format(header.points)}")
        print(f"  - Sample Rate:    {self.sample_rate}")
        print(f"  - Device Model:   {header.frame.decode().split(':')[0]}")
        print(f"  - Device Serial:  {header.frame.decode().split(':')[1]}\n")

        return header
