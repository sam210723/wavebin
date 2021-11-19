"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from PyQt5.QtWidgets import QApplication, QMenuBar, QMenu


class MainMenuBar(QMenuBar):
    """
    Main window menu bar
    """

    def __init__(self, app: QApplication):
        # Initialise base class
        super(MainMenuBar, self).__init__()

        # Hide menubar by default
        self.setHidden(True)

        # Parent application instance
        self.app = app
        
        # Root menu bar items
        self.menus = {
            "file": QMenu("&File"),
            "view": QMenu("&View"),
            "help": QMenu("&Help")
        }

        # Add root items to menu bar
        for m in self.menus: self.addMenu(self.menus[m])


    def log(self, msg: str):
        """
        Print message to console if verbose mode enabled

        Args:
            msg (str): Message to print to console
        """

        if self.app.config['verbose']: print(msg)
