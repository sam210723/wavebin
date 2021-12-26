"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from collections import namedtuple
import struct
import numpy as np

from wavebin.vendor import Vendor, Channel, Unit


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
            "https://wavebin.app/cloud/manuals/Agilent%20MSO-X%20User%20Manual.pdf#page=342",
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
            header = self.parse_waveform_header()
            data = self.parse_waveform_data()

            # Set waveform capture device model and serial from first waveform
            if i == 0: self.model, self.serial = header.frame.decode().split(':')

            # Create channel object
            self.channels.append(Channel(
                trace = data,
                points = header.points,
                sample_rate = 1/header.x_increment,
                duration = header.x_d_range,
                x_unit = Unit(header.x_units),
                y_unit = Unit(header.y_units),
                digital = data.dtype == np.uint8
            ))

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
            f" in {self.human_format(self._file_header.size, binary=True, unit='B')}"
        )

        return True


    def parse_waveform_header(self) -> namedtuple:
        """
        Parse waveform header

        Returns:
            namedtuple: Parsed waveform header as namedtuple
        """

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

        return header


    def parse_waveform_data(self) -> np.array:
        """
        Parse waveform data and data header

        Returns:
            np.array: NumPy array containing waveform data
        """

        # Unpack waveform data header
        length = self.data[self.offset]
        waveform_data_header_tuple = namedtuple(
            "WaveformDataHeader",
            "size data_type bpp length"
        )
        fields = struct.unpack("i2hi", self.data[self.offset : self.offset + length])
        self.offset += length
        header = waveform_data_header_tuple(*fields)

        # Parse waveform data
        dtype = [
            None,           # Unknown data
            np.float32,     # Normal float data
            np.float32,     # Maximum float data
            np.float32,     # Minimum float data
            None,           # Not used
            None,           # Not used
            np.uint8        # Digital unsigned char
        ]
        buf = np.frombuffer(
            self.data[self.offset : self.offset + header.length],
            dtype=dtype[header.data_type]
        )
        self.offset += header.length

        return buf
