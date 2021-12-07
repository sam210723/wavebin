"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from pathlib import Path
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QToolBar, QDialog, QAction, QLabel, QMessageBox, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
import qtawesome as qta
import sys
import webbrowser
from urllib import request

from wavebin.vendor import Vendor


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
            "open":    ["Open waveform", "folder-open"],
            "capture": ["Capture waveform", "wave-square"],
            "export":  ["Export waveform", "file-export"],
            "props":   ["Waveform properties", "list"],
            "sep0":    None,
            "docs":    ["Open documentation", "bookmark"],
            "bug":     ["Report a bug", "bug"],
            "update":  ["An update is available for wavebin", "sync-alt"]
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
        
        # Create waveform properties dialog
        self.props_dialog = QDialog(None, Qt.WindowCloseButtonHint)
        self.props_dialog.setWindowTitle("Waveform Properties")
        self.props_dialog.setWindowIcon(self.app.icon)
        self.props_dialog.setSizeGripEnabled(False)
        self.props_dialog.setAcceptDrops(False)
        self.props_dialog.setFixedWidth(600)
        self.props_dialog.setFixedHeight(400)
        self.props_dialog.setContentsMargins(15, 5, 10, 10)
        self.props_dialog.setStyleSheet("background: #111;")

        # Add waveform info label
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addWidget(spacer)
        self.info = QLabel()
        self.info.setFixedWidth(150)
        self.info.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.info.setToolTip("Sample rate and capture duration")
        self.info.setStyleSheet(
            """
            QLabel {
                color: #FFF;
                font-size: 11pt;
                padding-right: 10px;
            }
            """
        )
        self.addWidget(self.info)


    def button_open(self):
        """
        Launch open file dialog
        """
        
        self.app.button_open()


    def button_capture(self):
        """
        Trigger waveform capture via USB-TMC / PyVISA
        """

        self.app.button_capture()


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

        self.props_dialog.exec()


    def button_docs(self):
        """
        Open documentation in browser
        """

        self.log("Opening documentation in default web browser")
        webbrowser.open("https://vksdr.com/wavebin")


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
           f"&title=[v{self.app.config['version']} on {sys.version.split(' ')[0]}] *Brief description of issue*"
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


    def set_info(self, sr: str, dur: str):
        """
        Update info widget in toolbar

        Args:
            sr (str): Sample rate as human-readable string
            dur (str): Capture duration as human-readable string
        """

        self.info.setText(f"{sr}\n{dur}")


    def set_props(self, waveform: Vendor):
        """
        Update waveform properties
        """

        self.props_layout = QGridLayout()
        self.props_layout.setContentsMargins(0, 0, 0, 0)
        self.props_layout.setSpacing(0)
        self.props_dialog.setLayout(self.props_layout)

        # Download device image
        vendor = waveform.vendor_name.lower().replace("/agilent", '')
        model = waveform.model.replace('-', '').replace(' ', '')
        url = f"https://vksdr.com/download/wavebin/devices/{vendor}/{model}.png"
        image = request.urlopen(url).read()

        # Add device image to dialog
        pixmap = QPixmap()
        pixmap.loadFromData(image)
        device_image = QLabel()
        device_image.setPixmap(pixmap)
        self.props_layout.addWidget(device_image, 0, 0, 2, 2, Qt.AlignTop)

        # Add vendor logo to dialog
        pixmap = QPixmap(str(Path(__file__).parent / "assets" / f"{vendor}.png"))
        vendor_logo = QLabel()
        vendor_logo.setPixmap(pixmap)
        self.props_layout.addWidget(vendor_logo, 0, 2, 1, 2, Qt.AlignCenter)

        # Add device info to dialog
        device_info = QLabel()
        device_info.setTextFormat(Qt.TextFormat.RichText)
        device_info.setStyleSheet("font-family: Roboto; font-size: 15px; color: #FFF;")
        device_info.setText(
            f"""
            <div align='center'>
                <h1>{waveform.model}</h1>
                {waveform.serial}
            </div>
            """
        )
        self.props_layout.addWidget(device_info, 1, 2, 1, 2, Qt.AlignTop | Qt.AlignCenter)

        # Add waveform info table
        waveform_info = QLabel()
        self.props_layout.addWidget(waveform_info, 2, 0, 2, 4, Qt.AlignCenter)


    def log(self, msg: str):
        """
        Print message to console if verbose mode enabled

        Args:
            msg (str): Message to print to console
        """

        if self.app.config['verbose']: print(msg)
