"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

from pathlib import Path

class WaveParser():
    def __init__(self, config):
        self.config = config


    def parse(self, path):
        self.path = path

        # Open capture file
        print(f"Opening \"{self.path.name}\"")
        self.log(f"Full path \"{self.path}\"")
        self.file = open(self.path, mode="rb")

        # Parse capture header
        file_header = self.file.read(0x0C)
        self.parse_file_header(file_header)
    

    def parse_file_header(self, data):
        self.log("Capture Header:")
        print(data)


    def log(self, msg):
        if self.config['verbose']: print(msg)
