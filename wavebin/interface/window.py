"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from PyQt6 import QtWidgets as qt
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg


class MainWindow(qt.QApplication):
    """
    Main application window
    """

    def __init__(self, config):
        """
        Initialise main application window

        Args:
            config (dict): Configuration options
        """

        super(MainWindow, self).__init__([])

        self.config = config
        self.name = f"wavebin v{self.config['version']}"

        # Setup main Qt application
        self.log("Initialising Qt application")
        self.setApplicationDisplayName(self.name)
        self.setApplicationVersion(str(self.config['version']))

        # Create main Qt window
        self.log("Creating main Qt window")
        self.window = qt.QMainWindow()


    def run(self):
        """
        Launch main application window
        """

        self.log("Starting Qt application")
        self.window.show()
        self.exec()


    def log(self, msg):
        """
        Print message to console if verbose mode enabled

        Args:
            msg (str): Message to print to console
        """

        if self.config['verbose']: print(msg)
