"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

class PulseView():
    def __init__(self, config, waveforms):
        self.config = config
        self.waveforms = waveforms


    def log(self, msg):
        if self.config['verbose']: print(msg)
