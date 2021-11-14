"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStyle, QMenu, QToolBar, QToolButton
from PyQt5.QtCore import Qt, QEvent
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

        # Setup window menu bar and tool bar
        self.setup_menubar()
        self.setup_toolbar()


    def setup_window(self):
        """
        Setup main application window
        """

        # Styling and icon
        self.window.setWindowIcon(QIcon("icon.ico"))
        self.window.resize(self.config['width'], self.config['height'])
        if self.config['maximised']: self.window.showMaximized()
        self.window.setMinimumSize(800, 400)

        # Create main widget
        self.log("Creating main Qt widget")
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color: #000;")
        self.window.setCentralWidget(self.widget)
        self.window.setFocus()
        self.window.resizeEvent = self.resizeEvent
        self.window.changeEvent = self.changeEvent


    def setup_menubar(self):
        """
        Setup main window menu bar
        """

        # Initialise menu bar
        self.log("Building menu bar")
        self.menu_bar = self.window.menuBar()
        self.window.setMenuBar(self.menu_bar)

        # Root items
        self.menus = {
            "file": QMenu("&File", self.window),
            "view": QMenu("&View", self.window),
            "help": QMenu("&Help", self.window)
        }

        # Add root items to menu bar
        for m in self.menus: self.menu_bar.addMenu(self.menus[m])


    def setup_toolbar(self):
        """
        Setup main window tool bar
        """

        # Initialise tool bar
        self.log("Building tool bar")
        self.tool_bar = QToolBar()
        self.window.addToolBar(Qt.TopToolBarArea, self.tool_bar)

        # Set tool bar properties
        self.tool_bar.setMovable(False)
        self.tool_bar.setFloatable(False)
        self.tool_bar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.tool_bar.setStyleSheet(
            """
            QToolBar {
                background-color: #333;
            }

            QToolBar::separator {
                background: #666;
                width: 1px;
                margin: 5px 17px 5px 10px;
            }
            """
        )

        # Tool bar items
        self.tools = {
            "open":   ["Open File", "DirIcon"],
            "export": ["Export Waveform", "DriveFDIcon"],
            "sep0":   None,
            "info":   ["Waveform Info", "MessageBoxInformation"],
            "sep1":   None,
            "bug":    ["Report Bug", "MessageBoxWarning"]
        }

        # Build tool bar
        for t in self.tools:
            if self.tools[t] == None:
                self.tool_bar.insertSeparator(None)
                continue

            # Get built-in Qt icon
            icon = QIcon(
                self.style().standardIcon(
                    getattr(QStyle, f"SP_{self.tools[t][1]}")
                )
            )

            # Build button
            button = QToolButton()
            button.setIcon(icon)
            button.setText(f"  {self.tools[t][0]}")
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

            # Set button appreance
            button.setStyleSheet(
                """
                QToolButton {
                    color: #FFF;
                    padding: 5px 0 5px 0;
                }

                QToolButton:hover {
                    background: #444;
                }

                QToolButton:pressed {
                    color: #000;
                    background: #FFF;
                }
                """
            )

            # Add button to toolbar
            self.tool_bar.addWidget(button)

            # Replace list in dict with QToolButton instance
            self.tools[t] = button
        
        # Set default button states
        self.tools['info'].setEnabled(False)


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
