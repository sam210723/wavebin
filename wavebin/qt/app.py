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
        self.name = f"wavebin v{self.config['version']}"
        
        # Create main Qt application
        self.app = qt.QApplication([])
        self.app.setApplicationDisplayName(self.name)
        self.app.setApplicationVersion(str(self.config['version']))

        # Create main Qt window
        self.window = qt.QMainWindow()
        self.window.setWindowIcon(qtg.QIcon("icon.ico"))
        self.window.setStyleSheet(f"background-color: black;")
        if self.config['file']: self.window.setWindowTitle(f"\"{self.config['file'].name}\"")

        # Run Qt app
        self.window.show()
        self.app.exec_()
