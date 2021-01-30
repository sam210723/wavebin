"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

from PyQt5 import QtWidgets as qt
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class QtApp():
    def __init__(self, config):
        self.config = config
        self.app = qt.QApplication([])
        
        # Set application attributes
        name = f"wavebin v{self.config['version']}"
        self.app.setApplicationDisplayName(name)
        self.app.setApplicationVersion(str(self.config['version']))
