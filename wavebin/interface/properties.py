"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from pathlib import Path
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from threading import Thread
import requests


class WaveformProperties(QDialog):
    """
    Dialog box containing waveform properties
    """

    def __init__(self, app: QApplication) -> None:
        super(WaveformProperties, self).__init__(parent=None, flags=Qt.WindowCloseButtonHint)
        self.app = app

        # Set dialog properties
        self.setWindowTitle("Waveform Properties")
        self.setWindowIcon(app.icon)
        self.setSizeGripEnabled(False)
        self.setAcceptDrops(False)
        self.setFixedWidth(600)
        self.setFixedHeight(400)
        self.setContentsMargins(15, 5, 10, 10)
        self.setStyleSheet("background: #111;")

        # Setup dialog layout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.setLayout(self.grid_layout)


    def update(self, vendor: str, model: str, serial: str) -> None:
        """
        Update waveform properties

        Args:
            vendor (str): Device vendor name
            model (str): Device model
            serial (str): Device serial
        """

        # Remove widgets in grid layout
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        # Standardise vendor and model strings
        vendor_clean = vendor.lower()
        vendor_clean = vendor_clean.replace('/agilent', '')     #FIXME
        model_clean = model.replace('-', '')
        model_clean = model_clean.replace(' ', '')

        # Download device image
        self.download_thread = Thread(
            target=self.download_device_image,
            args=(
                f"https://wavebin.app/cloud/devices/{vendor_clean}/{model_clean}.png",
            )
        )
        self.download_thread.start()

        # Add device image widget to dialog
        self.device_image_pixmap = QPixmap()
        self.device_image_label = QLabel()
        self.grid_layout.addWidget(self.device_image_label, 0, 0, 2, 2, Qt.AlignTop)

        # Add vendor logo to dialog
        self.vendor_image_pixmap = QPixmap()
        self.vendor_image_path = str(Path(__file__).parent / "assets" / f"{vendor_clean}.png")
        self.vendor_image_pixmap.load(self.vendor_image_path)
        self.vendor_image_label = QLabel()
        self.vendor_image_label.setPixmap(self.vendor_image_pixmap)
        self.grid_layout.addWidget(self.vendor_image_label, 0, 2, 1, 2, Qt.AlignCenter)

        # Add device info to dialog
        self.device_info_label = QLabel()
        self.device_info_label.setTextFormat(Qt.TextFormat.RichText)
        self.device_info_label.setStyleSheet("font-family: Roboto; font-size: 15px; color: #FFF;")
        self.device_info_label.setText(
            f"""
            <div align='center'>
                <h1>{model}</h1>
                <p>{serial}</p>
            </div>
            """
        )
        self.grid_layout.addWidget(self.device_info_label, 1, 2, 1, 2, Qt.AlignTop | Qt.AlignCenter)

        # Add waveform info table
        self.waveform_props_widget = QLabel()
        self.waveform_props_widget.setText("PLACEHOLDER")
        self.waveform_props_widget.setStyleSheet("color: #FFF;")
        self.grid_layout.addWidget(self.waveform_props_widget, 2, 0, 2, 4, Qt.AlignCenter)


    def download_device_image(self, url: str) -> bool:
        """
        Download device image file from the web in new thread

        Args:
            url (str): URL to download

        Returns:
            bool: True on success
        """

        try:
            r = requests.get(
                url,
                headers = {
                    "User-Agent": "sam210723/wavebin download_device_image"
                }
            )

            if r.status_code == 200:
                self.device_image_pixmap.loadFromData(r.content)
                self.device_image_label.setPixmap(self.device_image_pixmap)
                self.log(f"Downloaded properties dialog device image")
                return True
            else:
                # Reposition top row of widgets so vendor logo and device model are centered
                if r.status_code == 403:
                    self.grid_layout.removeItem(self.grid_layout.itemAt(0))
                    self.grid_layout.removeItem(self.grid_layout.itemAt(1))
                    self.grid_layout.removeItem(self.grid_layout.itemAt(2))

                    self.grid_layout.addWidget(self.vendor_image_label, 0, 0, 1, 4, Qt.AlignCenter)
                    self.grid_layout.addWidget(self.device_info_label, 1, 0, 1, 4, Qt.AlignTop | Qt.AlignCenter)

                self.log(f"Failed to download device image (HTTP {r.status_code})")
                return False
        except Exception as e:
            self.log(f"Failed to download device image ({e})")
            return False


    def log(self, msg: str):
        """
        Print message to console if verbose mode enabled

        Args:
            msg (str): Message to print to console
        """

        if self.app.config['verbose']: print(msg)
