"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QToolBar, QLabel, QMessageBox, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
import qtawesome as qta
import sys
import webbrowser

from wavebin.config import config
from wavebin.interface.properties import WaveformProperties
from wavebin.vendor import Vendor


class MainToolBar(QToolBar):
    """
    Main window tool bar
    """

    def __init__(self, app: QApplication) -> None:
        # Initialise base class
        super(MainToolBar, self).__init__()

        # Parent application instance
        self.app = app

        # Set tool bar properties
        self.setMovable(False)
        self.setFloatable(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
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
            "open":    ["Open waveform", "folder-open"],
            "capture": ["Capture waveform", "wave-square"],
            "export":  ["Export waveform", "file-export"],
            "props":   ["Waveform properties", "list"],
            "sep0":    None,
            "docs":    ["Open documentation", "bookmark"],
            "bug":     ["Report a bug", "bug"],
            "update":  ["An update is available for wavebin", "sync-alt"],
            "about":   ["About wavebin", "question"]
        }

        # Build tool bar
        for t in self.items:
            # Insert toolbar separators
            if self.items[t] == None:
                self.insertSeparator(None)
                continue

            # Get icon from Font Awesome
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
        if not config.app.update: self.removeAction(self.items['update'])

        # Create waveform properties dialog
        self.props_dialog = WaveformProperties(self.app)

        # Add waveform info label
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(spacer)
        self.info = QLabel()
        self.info.setFixedWidth(150)
        self.info.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        self.info.setToolTip("Sample rate and capture duration")
        self.info.setStyleSheet(
            """
            QLabel {
                color: #FFF;
                font-family: Roboto;
                font-size: 15px;
                padding-right: 5px;
            }
            """
        )
        self.addWidget(self.info)


    def button_open(self) -> bool:
        """
        Launch open file dialog
        """
        
        return self.app.button_open()


    def button_capture(self) -> None:
        """
        Trigger waveform capture via USB-TMC / PyVISA
        """

        self.app.button_capture()


    def button_export(self) -> None:
        """
        Launch export file dialog
        """

        # Get initial path
        initial = self.app.config['file']

        # Show export file dialog
        file_path = self.app.save_dialog.getSaveFileName(
            self,
            "Export waveform",
            str(initial.with_suffix("").absolute()),
            "PulseView session (*.sr);;WAV file (*.wav)"
        )[0]

        # Handle cancelled dialog
        if file_path == "":
            logging.debug("Export file dialog cancelled")
            return
        else:
            file_path = Path(file_path)
        
        #TODO: Call export class


    def button_props(self) -> int:
        """
        Show current waveform properties
        """

        return self.props_dialog.exec()


    def button_docs(self) -> bool:
        """
        Open documentation in browser
        """

        return self.app.button_docs()


    def button_bug(self) -> bool:
        """
        Open issue form on GitHub
        """

        logging.debug("Opening GitHub issue form in default web browser")
        return webbrowser.open(
            "https://github.com/sam210723/wavebin/issues/new" +
            "?template=bug.md" +
            "&labels=bug,from+app" +
            "&assignees=sam210723" +
           f"&title=[v{self.app.config['version']} on {sys.version.split(' ')[0]}] *Brief description of issue*"
        )


    def button_update(self) -> bool:
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
            "<a href=\"https://github.com/sam210723/wavebin/blob/master/CHANGELOG.md\">View changelog on GitHub</a><br><br>" +
            "Are you sure you want to update wavebin?"
        )
        msgbox.setIcon(QMessageBox.Icon.Question)
        msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgbox.setDefaultButton(QMessageBox.No)
        msgbox.exec()
        if msgbox.result() == QMessageBox.No: return False

        # Launch separate process to update
        import subprocess
        subprocess.Popen("python3 -m pip install --no-input --upgrade wavebin && wavebin", shell=True)
        #TODO: Fix new wavebin process exiting

        # Exit current instance
        self.app.safe_exit(self.app.config)


    def button_about(self) -> bool:
        """
        Launch wavebin About dialog
        """

        print("ABOUT")


    def set_info(self, sr: str, dur: str) -> None:
        """
        Update info widget in toolbar

        Args:
            sr (str): Sample rate as human-readable string
            dur (str): Capture duration as human-readable string
        """

        self.info.setText(f"{sr}\n{dur}")


    def set_props(self, waveform: Vendor) -> None:
        """
        Update waveform properties
        """

        self.props_dialog.update(
            waveform.vendor_name,
            waveform.model,
            waveform.serial
        )
        #TODO: Pass waveform properties to dialog
