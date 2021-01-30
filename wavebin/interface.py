"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

from PyQt5 import QtWidgets as qt
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import webbrowser

class QtApp():
    def __init__(self, config):
        self.config = config
        self.name = f"wavebin v{self.config['version']}"
        
        # Create main Qt application
        self.log("Initialising Qt application")
        self.app = qt.QApplication([])
        self.app.setApplicationDisplayName(self.name)
        self.app.setApplicationVersion(str(self.config['version']))

        # Create main Qt window
        self.log("Creating main Qt window")
        self.window = qt.QMainWindow()
        self.setup_window()

        # Run Qt app
        self.log("Starting Qt application")
        self.window.show()
        self.app.exec_()


    def setup_window(self):
        # Styling and icon
        self.window.setWindowIcon(qtg.QIcon("icon.ico"))
        self.window.resize(self.config['width'], self.config['height'])

        # Title (prepended to application display name by Qt)
        if self.config['file']: self.window.setWindowTitle(f"\"{self.config['file'].name}\"")

        # Menu bar
        self.log("Building menus")
        self.menu_bar = self.window.menuBar()
        self.window.setMenuBar(self.menu_bar)

        # Menu items
        self.menus = {
            "file": qt.QMenu("&File", self.window),
            "view": qt.QMenu("&View", self.window),
            "help": qt.QMenu("&Help", self.window)
        }

        # Add items to menu bar
        for m in self.menus: self.menu_bar.addMenu(self.menus[m])

        # Menu actions
        self.menu_actions = {
            "file_open":    qt.QAction("&Open...", self.window),
            "file_exit":    qt.QAction("&Exit", self.window),
            "view_sidebar": qt.QAction("&Sidebar", self.window),
            "help_github":  qt.QAction("&GitHub repository...", self.window),
        }

        # Customise menu actions
        self.menu_actions['view_sidebar'].setCheckable(True)
        self.menu_actions['view_sidebar'].setChecked(True)

        # Add actions to menu items
        for a in self.menu_actions:
            self.menu_actions[a].triggered.connect(eval(f"self.menu_{a}"))
            self.menus[a.split("_")[0]].addAction(self.menu_actions[a])


    def menu_file_open(self):
        return


    def menu_file_exit(self):
        self.app.exit()


    def menu_view_sidebar(self):
        return


    def menu_help_github(self):
        webbrowser.open("https://github.com/sam210723/wavebin", new=2)


    def log(self, msg):
        if self.config['verbose']: print(msg)
