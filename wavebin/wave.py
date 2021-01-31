"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

from pathlib import Path
import struct
from collections import namedtuple

class WaveParser():
    def __init__(self, config):
        self.config = config


    def parse(self, path):
        self.config['file'] = Path(path)

        # Open capture file
        print(f"Opening \"{self.config['file'].name}\"")
        self.log(f"Full path \"{self.config['file']}\"\n")
        self.file = open(self.config['file'], mode="rb")

        # Parse file header
        file_header = self.file.read(0x0C)
        if not self.parse_file_header(file_header):
            return False
        
        # Update UI elements
        self.config['app'].update()
        self.config['plot'].update()


    def parse_file_header(self, data):
        # Unpack file header
        file_header_tuple = namedtuple('FileHeader', 'magic version size waveforms')
        fields = struct.unpack("2s2s2i", data)
        self.file_header = file_header_tuple(*fields)

        # Check file magic
        if self.file_header.magic != b'AG':
            print("Unknown file format")
            return False

        # Print file header info
        self.log("File Header:")
        self.log(f"  - Waveforms: {self.file_header.waveforms}")
        self.log(f"  - File Size: {self.file_header.size} bytes\n")

        return True


    def ui(self, app, plot):
        self.config['app'] = app
        self.config['plot'] = plot


    def log(self, msg):
        if self.config['verbose']: print(msg)
