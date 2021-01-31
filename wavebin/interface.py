"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

from pathlib import Path
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

        # Create main widget
        self.log("Creating main Qt widget")
        self.widget = qt.QWidget()
        self.widget.setStyleSheet("background-color: black;")
        self.window.setCentralWidget(self.widget)

        # Create widget layout
        self.log("Creating widget layout")
        self.layout = qt.QGridLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        self.widget.setLayout(self.layout)

        # Create sidebar widget
        self.sidebar = qt.QTableWidget()
        self.sidebar.setFixedWidth(300)
        self.sidebar.setColumnCount(2)
        self.sidebar.setRowCount(0)
        self.sidebar.verticalHeader().setVisible(False)
        self.sidebar.horizontalHeader().setVisible(False)
        self.sidebar.horizontalHeader().setSectionResizeMode(qt.QHeaderView.Stretch)
        self.sidebar.setEditTriggers(qt.QAbstractItemView.NoEditTriggers)
        self.sidebar.setFocusPolicy(qtc.Qt.NoFocus)
        self.sidebar.setSelectionMode(qt.QAbstractItemView.NoSelection)
        self.sidebar.setStyleSheet(
            "border: 1px solid black;"\
            "background-color: black;"\
            "gridline-color: black;"\
            "color: white;"\
            "font-weight: normal;"\
            "font-size: 17px;"
        )
        self.layout.addWidget(self.sidebar, 0, 0)


    def run(self):
        self.log("Starting Qt application")
        self.window.show()
        self.app.exec_()


    def setup_window(self):
        # Styling and icon
        self.window.setWindowIcon(qtg.QIcon("icon.ico"))
        self.window.resize(self.config['width'], self.config['height'])
        self.window.setMinimumSize(800, 400)

        # Title (prepended to application display name by Qt)
        if self.config['file']: self.window.setWindowTitle(f"\"{self.config['file'].name}\"")

        # Menu bar
        self.log("Building menu bar ")
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
            "help_website": qt.QAction("&Website...", self.window),
        }

        # Customise menu actions
        self.menu_actions['view_sidebar'].setCheckable(True)
        self.menu_actions['view_sidebar'].setChecked(True)

        # Add actions to menu items
        for a in self.menu_actions:
            self.menu_actions[a].triggered.connect(eval(f"self.menu_{a}"))
            self.menus[a.split("_")[0]].addAction(self.menu_actions[a])


    def menu_file_open(self):
        self.log("Creating Open File dialog")
        ofd = qt.QFileDialog()
        
        # Show open file dialog
        file_path = ofd.getOpenFileName(
            self.window,
            "Open waveform capture",
            str(Path().home()),
            "Waveform files (*.bin)"
        )[0]

        # Handle cancelled dialog
        if file_path == "":
            self.log("Open file dialog cancelled")
            return
        
        # Parse file path
        file_path = Path(file_path)
        print(f"Opening \"{file_path.name}\"")
        self.log(f"Full path \"{file_path}\"")
        self.window.setWindowTitle(f"\"{file_path.name}\"")


    def menu_file_exit(self):
        self.app.exit()


    def menu_view_sidebar(self):
        if self.sidebar.isHidden():
            self.sidebar.show()
        else:
            self.sidebar.hide()


    def menu_help_website(self):
        self.log("Opening site in default browser")
        webbrowser.open("https://vksdr.com/wavebin", new=2)


    def add_plot(self, plot):
        self.log("Adding plot widget to layout")
        self.layout.addWidget(plot, 0, 1)


    def log(self, msg):
        if self.config['verbose']: print(msg)
