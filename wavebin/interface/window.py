"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QFileDialog
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon

from wavebin.interface.toolbar import MainToolBar
from wavebin.interface.menubar import MainMenuBar


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

        # Window styling and state
        self.window.setWindowIcon(QIcon("icon.ico"))
        self.window.resize(self.config['width'], self.config['height'])
        self.window.setMinimumSize(800, 400)
        if self.config['maximised']: self.window.showMaximized()

        # Add menu bar to main window
        self.log("Building menu bar")
        self.menu_bar = MainMenuBar()
        self.window.setMenuBar(self.menu_bar)

        # Add tool bar to main window
        self.log("Building tool bar")
        self.tool_bar = MainToolBar()
        self.window.addToolBar(Qt.TopToolBarArea, self.tool_bar)

        # Create main widget
        self.log("Creating main Qt widget")
        self.widget = QWidget()
        self.window.setCentralWidget(self.widget)
        self.widget.setStyleSheet("background-color: #000;")
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.window.resizeEvent = self.resizeEvent
        self.window.changeEvent = self.changeEvent
        self.window.setFocus()

        # Create main layout
        self.log("Creating main grid layout")
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.widget.setLayout(self.layout)

        # Create open/save file dialogs
        self.open_dialog = QFileDialog()
        self.save_dialog = QFileDialog()


    def run(self):
        """
        Launch main application window
        """

        self.log("Starting Qt application")
        self.window.show()
        self.exec()


    def resizeEvent(self, event):
        """
        Handle window resize event
        """

        QMainWindow.resizeEvent(self.window, event)

        # Update window size and state in configuration
        self.config['width'] = self.window.width()
        self.config['height'] = self.window.height()
    

    def changeEvent(self, event):
        """
        Handle window state change
        """

        if event.type() == QEvent.WindowStateChange:
            self.config['maximised'] = self.window.isMaximized()


    def log(self, msg: str):
        """
        Print message to console if verbose mode enabled

        Args:
            msg (str): Message to print to console
        """

        if self.config['verbose']: print(msg)
