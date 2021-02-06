"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

import zipfile


class PulseView():
    def __init__(self, verbose, path, waveforms):
        self.verbose = verbose
        self.path = path
        self.waveforms = waveforms

        self.log(f"Exporting PulseView session to {self.path}")

        # Create ZIP file
        self.zipf = zipfile.ZipFile(self.path, 'w', zipfile.ZIP_DEFLATED)

        # Create version file
        self.zipf.writestr('version', '2'.encode('utf-8'))

        # Close completed ZIP file
        self.zipf.close()


    def log(self, msg):
        if self.verbose: print(msg)
