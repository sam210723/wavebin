"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon


class MainWindow(QApplication):
    """
    Main application window
    """

    def __init__(self, config: dict):
        """
        Initialise main application window

        Args:
            config (dict): Configuration options
        """

        # Initialise parent class
        super(MainWindow, self).__init__([])

        # Set globals
        self.config = config
        self.name = f"wavebin v{self.config['version']}"

        # Setup main Qt application
        self.log("Initialising Qt application")
        self.setApplicationDisplayName(self.name)
        self.setApplicationVersion(str(self.config['version']))

        # Create main Qt window
        self.log("Creating main Qt window")
        self.window = QMainWindow()
        self.setup_window()


    def setup_window(self):
        """
        Setup main application window
        """

        # Styling and icon
        self.window.setWindowIcon(QIcon("icon.ico"))
        self.window.resize(self.config['width'], self.config['height'])
        self.window.setMinimumSize(800, 400)
        self.window.setStyleSheet("background-color: black;")


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
