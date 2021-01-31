"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

class WaveParser():
    def __init__(self, config):
        self.config = config


    def parse(self, path):
        self.path = path


    def log(self, msg):
        if self.config['verbose']: print(msg)
