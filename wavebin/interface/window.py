"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QFileDialog, QTextEdit
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon
import qtawesome as qta
import webbrowser

from wavebin.interface.toolbar import MainToolBar
from wavebin.interface.menubar import MainMenuBar


class MainWindow(QApplication):
    """
    Main application window
    """

    def __init__(self, config: dict, safe_exit):
        """
        Initialise main application window

        Args:
            config (dict): Configuration options
            safe_exit (function): Graceful application exit function
        """

        # Initialise parent class
        super(MainWindow, self).__init__([])

        # Set globals
        self.safe_exit = safe_exit
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
        self.log("Updating window style")
        self.window.setWindowIcon(QIcon("icon.ico"))
        self.window.resize(self.config['width'], self.config['height'])
        self.window.setMinimumSize(800, 400)
        if self.config['maximised']: self.window.showMaximized()

        # Add menu bar to main window
        self.log("Building menu bar")
        self.menu_bar = MainMenuBar(self)
        self.window.setMenuBar(self.menu_bar)

        # Add tool bar to main window
        self.log("Building tool bar")
        self.tool_bar = MainToolBar(self)
        self.window.addToolBar(Qt.TopToolBarArea, self.tool_bar)

        # Create main widget
        self.log("Creating main widget")
        self.widget = QWidget()
        self.window.setCentralWidget(self.widget)
        self.widget.setStyleSheet("background-color: #000;")
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.window.resizeEvent = self.event_resize
        self.window.changeEvent = self.event_change
        self.window.keyPressEvent = self.event_keypress
        self.window.setFocus()

        # Create main layout
        self.log("Creating main grid layout")
        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)

        # Create open/save file dialogs
        self.log("Creating file dialogs")
        self.open_dialog = QFileDialog()
        self.save_dialog = QFileDialog()

        # Initial welcome screen
        self.log("Building welcome screen")
        if not self.config['file']: self.welcome()


    def run(self):
        """
        Launch main application window
        """

        self.log("Starting Qt application")
        self.window.show()
        self.exec()


    def welcome(self):
        """
        Builds welcome screen when no waveforms are loaded
        """

        # Text banner
        banner = QTextEdit()
        banner.setStyleSheet("QTextEdit { border: none; }")
        banner.setReadOnly(True)
        banner.setDisabled(True)
        banner.setHtml(
            """
            <style>
                #container {
                    text-align: center;
                    vertical-align: bottom;
                    margin-top: 150px;
                }

                span {
                    color: #FFF;
                    font-family: Arial;
                    font-size: 60px;
                    font-weight: bold;
                }

                p {
                    margin-top: 30px;
                    color: #AAA;
                    font-family: Roboto;
                    font-size: 12pt;
                }
            </style>

            <br><div id='container'>
                <img src='icon.ico'><span> wavebin</span>
                <p>
                    Get started by opening a waveform file or capturing a new waveform
                </p>
            </div>
            """
        )
        self.layout.addWidget(banner, 0, 0, 1, 9)

        # Open/Capture buttons
        style = """
            QPushButton {
                margin: 10px;
                padding: 10px 15px 10px 15px;

                color: #FFF;
                background: #222;

                font-family: Roboto;
                font-size: 12pt;

                border: 1px solid #444;
                border-radius: 6px;
            }

            QPushButton::hover {
                background: #444;
            }

            QPushButton::pressed {
                background: #999;
            }
        """
        button_open = QPushButton()
        button_open.setText(" Open waveform")
        button_open.setStyleSheet(style)
        button_open.setIcon(qta.icon("fa5s.folder-open", color="#FFF"))
        button_open.clicked.connect(self.button_open)
        self.layout.addWidget(button_open, 1, 3, 1, 1, Qt.AlignRight | Qt.AlignTop)

        button_capture = QPushButton()
        button_capture.setText(" Capture waveform")
        button_capture.setStyleSheet(style)
        button_capture.setIcon(qta.icon("fa5s.wave-square", color="#FFF"))
        button_capture.clicked.connect(self.button_capture)
        self.layout.addWidget(button_capture, 1, 4, 1, 1, Qt.AlignCenter | Qt.AlignTop)

        button_docs = QPushButton()
        button_docs.setText(" Documentation")
        button_docs.setStyleSheet(style)
        button_docs.setIcon(qta.icon("fa5s.bookmark", color="#FFF"))
        button_docs.clicked.connect(self.button_docs)
        self.layout.addWidget(button_docs, 1, 5, 1, 1, Qt.AlignLeft | Qt.AlignTop)


    def button_open(self):
        """
        Launch open file dialog
        """

        # Get initial path
        if self.config['file']:
            initial = self.config['file'].parent
        else:
            initial = Path.home()

        # Show open file dialog
        file_path = self.open_dialog.getOpenFileName(
            self.widget,
            "Open waveform",
            str(initial.absolute()),
            "Waveforms (*.bin *.wfm *.csv);;All files (*.*)"
        )[0]

        # Handle cancelled dialog
        if file_path == "":
            self.log("Open file dialog cancelled")
            return
        else:
            file_path = Path(file_path)
        
        # Update current file in config
        self.config['file'] = file_path


    def button_capture(self):
        """
        Trigger waveform capture via USB-TMC / PyVISA
        """
        #TODO: Waveform capture via PyVISA
        pass


    def button_docs(self):
        """
        Open documentation in browser
        """

        self.log("Opening documentation in default web browser")
        webbrowser.open("https://vksdr.com/wavebin")


    def event_resize(self, event):
        """
        Handle window resize event
        """

        QMainWindow.resizeEvent(self.window, event)

        # Update window size and state in configuration
        self.config['width'] = self.window.width()
        self.config['height'] = self.window.height()
    

    def event_change(self, event):
        """
        Handle window state change
        """

        if event.type() == QEvent.WindowStateChange:
            self.config['maximised'] = self.window.isMaximized()


    def event_keypress(self, event):
        """
        Handle keyboard hotkey events
        """

        # Show/Hide menubar
        if event.key() == Qt.Key.Key_Alt:
            self.menu_bar.setHidden(not self.menu_bar.isHidden())
            self.menu_bar.setFocus(not self.menu_bar.isHidden())


    def log(self, msg: str):
        """
        Print message to console if verbose mode enabled

        Args:
            msg (str): Message to print to console
        """

        if self.config['verbose']: print(msg)
