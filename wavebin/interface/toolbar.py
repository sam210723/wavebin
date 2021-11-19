"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from PyQt5.QtWidgets import QAction, QApplication, QMessageBox, QToolBar, QStyle
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import qtawesome as qta
import sys
import webbrowser

class MainToolBar(QToolBar):
    """
    Main window tool bar
    """

    def __init__(self, app: QApplication):
        # Initialise base class
        super(MainToolBar, self).__init__()

        # Parent application instance
        self.app = app

        # Set tool bar properties
        self.setMovable(False)
        self.setFloatable(False)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setStyleSheet(
            """
            QToolBar {
                background-color: #333;
                border: none;
                padding-left: 4px;
            }

            QToolBar::separator {
                background: #000;
                width: 1px;
                margin: 5px 5px 5px 5px;
            }

            QToolButton {
                color: #FFF;
                padding: 7px;
            }
            """
        )

        # Tool bar items
        self.items = {
            "open":    ["Open File", "folder-open"],
            "export":  ["Export Waveform", "file-export"],
            "sep0":    None,
            "info":    ["Waveform Info", "list"],
            "capture": ["Capture Waveform", "wave-square"],
            "sep1":    None,
            "bug":     ["Report Bug", "bug"],
            "update":  ["Update wavebin", "sync-alt"]
        }

        # Build tool bar
        for t in self.items:
            # Insert toolbar separators
            if self.items[t] == None:
                self.insertSeparator(None)
                continue

            icon = qta.icon(
                f"fa5s.{self.items[t][1]}",
                color="#FFF",
                color_active="#AAA"
            )

            # Build action object
            action = QAction(self)
            action.setIcon(icon)
            action.setText(self.items[t][0])
            action.triggered.connect(eval(f"self.button_{t}"))
            self.addAction(action)

            # Replace list in dict with QAction instance
            self.items[t] = action
        
        # Set default button states
        self.items['info'].setEnabled(False)
        if not self.app.config['update']: self.removeAction(self.items['update'])


    def button_open(self):    print("button_open")
    def button_export(self):  print("button_export")
    def button_capture(self): print("button_capture")
    def button_info(self):    print("button_info")


    def button_bug(self):
        """
        Open issue form on GitHub
        """

        self.log("Opening GitHub issue form in default web browser")
        webbrowser.open(
            "https://github.com/sam210723/wavebin/issues/new" +
            "?template=bug.md" +
            "&labels=bug,from+app" +
            "&assignees=sam210723" +
           f"&title=[v{self.app.config['version']} on {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}] *Brief description of issue*"
        )


    def button_update(self):
        """
        Update wavebin via PyPI
        """

        # Confirm update with user
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Update available")
        msgbox.setTextFormat(Qt.TextFormat.RichText)
        msgbox.setText(
            "An update is available for wavebin via the Python Package Index (PyPI)<br>" +
            "<a href=\"https://github.com/sam210723/wavebin/blob/master/CHANGELOG.md\">View changelog on GitHub</a><br><br>"
            "Are you sure you want to update wavebin?"
        )
        msgbox.setIcon(QMessageBox.Icon.Question)
        msgbox.setWindowIcon(QIcon("icon.ico"))
        msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgbox.setDefaultButton(QMessageBox.No)
        msgbox.exec()
        if msgbox.result() == QMessageBox.No: return

        # Launch separate process to update
        import subprocess
        subprocess.Popen("python3 -m pip install --no-input --upgrade wavebin && wavebin", shell=True)
        #TODO: Fix new wavebin process exiting

        # Exit current instance
        self.app.safe_exit(self.app.config)


    def log(self, msg: str):
        """
        Print message to console if verbose mode enabled

        Args:
            msg (str): Message to print to console
        """

        if self.app.config['verbose']: print(msg)
