"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from PyQt5.QtWidgets import QMenuBar, QMenu


class MainMenuBar(QMenuBar):
    """
    Main window menu bar
    """

    def __init__(self):
        super(MainMenuBar, self).__init__()
        
        # Root menu bar items
        self.menus = {
            "file": QMenu("&File"),
            "view": QMenu("&View"),
            "help": QMenu("&Help")
        }

        # Add root items to menu bar
        for m in self.menus: self.addMenu(self.menus[m])
