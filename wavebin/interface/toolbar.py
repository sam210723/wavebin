"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from pathlib import Path
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
                background-color: #222;
                border: none;
                padding-left: 4px;
            }

            QToolBar::separator {
                background: #444;
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
            "open":    ["Open file", "folder-open"],
            "export":  ["Export waveform", "file-export"],
            "sep0":    None,
            "props":   ["Waveform properties", "list"],
            "capture": ["Capture waveform", "wave-square"],
            "sep1":    None,
            "bug":     ["Report a bug", "bug"],
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
        self.items['export'].setEnabled(False)
        self.items['props'].setEnabled(False)
        if not self.app.config['update']: self.removeAction(self.items['update'])


    def button_open(self):
        """
        Launch open file dialog
        """

        # Get initial path
        if self.app.config['file']:
            initial = self.app.config['file'].parent
        else:
            initial = Path.home()

        # Show open file dialog
        file_path = self.app.open_dialog.getOpenFileName(
            self,
            "Open waveform capture",
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
        self.app.config['file'] = file_path


    def button_export(self):
        """
        Launch export file dialog
        """

        # Get initial path
        initial = self.app.config['file']

        # Show export file dialog
        file_path = self.app.save_dialog.getSaveFileName(
            self,
            "Export waveform",
            str(initial.with_suffix(".sr").absolute()),
            "PulseView session (*.sr);;WAV file (*.wav)"
        )[0]

        # Handle cancelled dialog
        if file_path == "":
            self.log("Export file dialog cancelled")
            return
        else:
            file_path = Path(file_path)
        
        #TODO: Call export class


    def button_props(self):
        """
        Show current waveform properties
        """
        
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Waveform Properties")
        msgbox.setWindowIcon(QIcon("icon.ico"))
        msgbox.setIcon(QMessageBox.Icon.NoIcon)
        msgbox.setTextFormat(Qt.TextFormat.RichText)
        msgbox.setText(
            "PLACEHOLDER TEXT<br>" +    #TODO
            "Body to be filled by waveform parser class"
        )
        msgbox.setStandardButtons(QMessageBox.Close)
        msgbox.setDefaultButton(QMessageBox.Close)
        msgbox.exec()


    def button_capture(self):
        """
        Trigger waveform capture via USB-TMC / PyVISA
        """
        pass


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
        msgbox.setWindowIcon(QIcon("icon.ico"))
        msgbox.setTextFormat(Qt.TextFormat.RichText)
        msgbox.setText(
            "An update is available for wavebin via the Python Package Index (PyPI)<br>" +
            "<a href=\"https://github.com/sam210723/wavebin/blob/master/CHANGELOG.md\">View changelog on GitHub</a><br><br>"
            "Are you sure you want to update wavebin?"
        )
        msgbox.setIcon(QMessageBox.Icon.Question)
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
