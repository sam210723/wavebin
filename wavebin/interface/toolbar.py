"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from PyQt5.QtWidgets import QApplication, QToolBar, QToolButton, QStyle
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


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
            }

            QToolBar::separator {
                background: #666;
                width: 1px;
                margin: 5px 15px 5px 10px;
            }
            """
        )

        # Tool bar items
        self.items = {
            "open":   ["Open File", "DirIcon"],
            "export": ["Export Waveform", "DriveFDIcon"],
            "sep0":   None,
            "info":   ["Waveform Info", "MessageBoxInformation"],
            "sep1":   None,
            "bug":    ["Report Bug", "MessageBoxWarning"]
        }

        # Build tool bar
        for t in self.items:
            if self.items[t] == None:
                self.insertSeparator(None)
                continue

            # Get built-in Qt icon
            icon = QIcon(
                self.style().standardIcon(
                    getattr(QStyle, f"SP_{self.items[t][1]}")
                )
            )

            # Build button
            button = QToolButton()
            button.setIcon(icon)
            button.setText(f"  {self.items[t][0]}")
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
            self.addWidget(button)

            # Replace list in dict with QToolButton instance
            self.items[t] = button
        
        # Set default button states
        self.items['info'].setEnabled(False)
