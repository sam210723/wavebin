"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QWidget, QGridLayout, QFileDialog, QTextEdit, QMessageBox
from PyQt6.QtCore import Qt, QEvent, QRect
from PyQt6.QtGui import QFontDatabase, QIcon, QKeyEvent, QResizeEvent
import qtawesome as qta
import webbrowser

from wavebin.config import config
from wavebin.interface.toolbar import MainToolBar
from wavebin.interface.menubar import MainMenuBar
from wavebin.interface.plot import WaveformPlot


class MainWindow(QApplication):
    """
    Main application window
    """

    def __init__(self) -> None:
        """
        Initialise main application window
        """

        # Initialise parent class
        super(MainWindow, self).__init__([])

        # Setup main Qt application
        logging.debug("Initialising Qt application")
        self.setApplicationName(config.app.name)
        self.setApplicationDisplayName(f"{config.app.name} v{config.app.version}")
        self.setApplicationVersion(config.app.version)

        # Create main Qt window
        logging.debug("Creating main Qt window")
        self.window = QMainWindow()
        self.window.setFocus()
        self.window.raise_()
        self.window.activateWindow()

        # Attach event handlers
        self.window.resizeEvent = self.event_resize         # type: ignore
        self.window.changeEvent = self.event_change         # type: ignore
        self.window.keyPressEvent = self.event_keypress     # type: ignore

        # Add Inter font
        font_dir = Path(__file__).parent / "assets" / "Inter"
        QFontDatabase.addApplicationFont(str( font_dir / "Inter-Regular.ttf"))
        QFontDatabase.addApplicationFont(str( font_dir / "Inter-Bold.ttf"))

        # Window styling and state
        logging.debug("Updating window style")
        self.icon_path = Path(__file__).parent / "assets" / "icon.ico"
        self.icon_path_multi = Path(__file__).parent / "assets" / "icon-multi.ico"
        self.icon = QIcon(str(self.icon_path_multi))
        self.setWindowIcon(self.icon)
        self.window.setMinimumSize(800, 500)

        # Styling for Windows platforms
        try:
            import pywinstyles
            pywinstyles.apply_style(self.window, "dark")
        except ImportError: pass

        # Add tool bar to main window
        logging.debug("Building tool bar")
        self.tool_bar = MainToolBar(self)
        self.window.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tool_bar)

        # Add menu bar to main window
        logging.debug("Building menu bar")
        self.menu_bar = MainMenuBar(self.tool_bar)
        self.window.setMenuBar(self.menu_bar)

        # Create main widget
        logging.debug("Creating main widget")
        self.widget = QWidget()
        self.window.setCentralWidget(self.widget)
        self.widget.setStyleSheet("background-color: #000;")
        self.widget.setContentsMargins(0, 0, 0, 0)

        # Create main layout
        logging.debug("Creating main grid layout")
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.widget.setLayout(self.layout)

        # Create open/save file dialogs
        logging.debug("Creating file dialogs")
        self.open_dialog = QFileDialog()
        self.save_dialog = QFileDialog()

        # If file already loaded from CLI args
        if config.file:
            # Prepare to render waveform
            self.update()
        else:
            # Initial welcome screen
            self.welcome()


    def run(self) -> int:
        """
        Launch main application window
        """

        logging.debug("Starting Qt application")

        # Get center of primary screen
        screen: QRect = self.primaryScreen().geometry()
        offset: tuple[int, int] = (
            int(screen.width() / 2 - (config.ui.width / 2)),
            int(screen.height() / 2 - (config.ui.height / 2))
        )

        # Update window size and position
        self.window.setGeometry(
            *offset,
            config.ui.width,
            config.ui.height
        )

        # Maximise main window
        if config.ui.maximised:
            self.window.setWindowState(Qt.WindowState.WindowMaximized)

        self.window.show()
        return self.exec()


    def welcome(self) -> None:
        """
        Builds welcome screen when no waveforms are loaded
        """

        logging.debug("Building welcome screen")

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
                }

                span {
                    color: #FFF;
                    font-family: Inter;
                    font-size: 60px;
                    font-weight: bold;
                }

                p {
                    margin-top: 90px;
                    color: #BBB;
                    font-family: Inter;
                    font-size: 12pt;
                }
            </style>

            <div id='container'>
            """ +
          f"    <img src='{self.icon_path}'><span>&nbsp;&nbsp;wavebin</span>" +
            """
                <p>
                    Get started by opening a waveform file or capturing a new waveform
                </p>
            </div>
            """
        )
        self.layout.addWidget(banner, 0, 0, 1, 9, Qt.AlignmentFlag.AlignBottom)

        # Button style
        style = """
            QPushButton {
                margin: 10px;
                padding: 10px 15px 10px 15px;

                color: #FFF;
                background: #222;

                font-family: Inter;
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

        # Open waveform button
        button_open = QPushButton()
        button_open.setText(" Open waveform")
        button_open.setToolTip("Open a waveform capture file from a supported oscilloscope vendor")
        button_open.setStyleSheet(style)
        button_open.setIcon(qta.icon("fa5s.folder-open", color="#FFF"))
        button_open.clicked.connect(self.button_open)
        self.layout.addWidget(button_open, 1, 3, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        # Capture waveform button
        button_capture = QPushButton()
        button_capture.setText(" Capture waveform")
        button_capture.setToolTip("Capture a new waveform from an oscilloscope using USB-TMC")
        button_capture.setStyleSheet(style)
        button_capture.setIcon(qta.icon("fa5s.wave-square", color="#FFF"))
        button_capture.clicked.connect(self.button_capture)
        self.layout.addWidget(button_capture, 1, 4, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        # Documentation button
        button_docs = QPushButton()
        button_docs.setText(" Documentation")
        button_docs.setToolTip("Open wavebin documentation in the default web browser")
        button_docs.setStyleSheet(style)
        button_docs.setIcon(qta.icon("fa5s.bookmark", color="#FFF"))
        button_docs.clicked.connect(self.button_docs)
        self.layout.addWidget(button_docs, 1, 5, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)


    def update(self) -> None:
        """
        Update UI for new waveform capture
        """

        # Clear grid layout
        logging.debug("Resetting main grid layout")
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Set file name in window title
        self.window.setWindowTitle(config.file.name)

        # Add plot widget to grid layout
        self.plot = WaveformPlot(config.waveform)
        self.layout.addWidget(
            self.plot,
            0, 0,
            len(config.waveform.channels), 8
        )

        # Add channel controls to grid layout
        for i, c in enumerate(config.waveform.channels):
            label = QLabel(f"WAVE{i} CONTROLS")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(
                """
                QLabel {
                    color: #FFF;
                    background: #111;
                    border-top: 1px solid #555;
                    border-left: 1px solid #555;
                }
                """
            )
            self.layout.addWidget(label, i, 8, 1, 2)

        # Show waveform info in toolbar
        self.tool_bar.set_info(
            config.waveform.channels[0].sample_rate_pretty,
            config.waveform.channels[0].duration_pretty
        )
        self.tool_bar.set_props(config.waveform)

        # Enable export and properties toolbar buttons
        self.tool_bar.items['export'].setEnabled(True)
        self.tool_bar.items['props'].setEnabled(True)
        
        # Enable export and properties menu actions
        self.menu_bar.menu_actions['file']['export'].setEnabled(True)
        self.menu_bar.menu_actions['view']['props'].setEnabled(True)


    def button_open(self) -> bool:
        """
        Launch open file dialog
        """

        # Get initial path
        if config.file:
            initial = config.file.parent
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
            logging.debug("Open file dialog cancelled")
            return False
        else:
            file_path = Path(file_path)

        # Open waveform file
        config.waveform = file_path
        if config.waveform:
            # Prepare to render waveform
            config.file = file_path
            self.update()
            return True
        else:
            # Show error message
            msgbox = QMessageBox()
            msgbox.setText(f"Error opening \"{file_path.name}\"\n\nUnknown file format.")
            msgbox.setWindowIcon(QIcon("icon.ico"))
            msgbox.setIcon(QMessageBox.Icon.Critical)
            msgbox.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgbox.setDefaultButton(QMessageBox.StandardButton.Ok)
            msgbox.exec()
            return False


    def button_capture(self) -> None:
        """
        Trigger waveform capture via USB-TMC / PyVISA
        """
        #TODO: Waveform capture via PyVISA
        print("CAPTURE")


    def button_docs(self) -> bool:
        """
        Open documentation in browser
        """

        logging.debug("Opening documentation in default web browser")
        return webbrowser.open("https://wavebin.vksdr.com")


    def event_resize(self, event: QResizeEvent) -> None:
        """
        Handle window resize event
        """

        QMainWindow.resizeEvent(self.window, event)

        # Update window size and state in configuration
        if self.window.width() != self.primaryScreen().size().width():
            config.ui.width = self.window.width()
            config.ui.height = self.window.height()


    def event_change(self, event: QEvent) -> None:
        """
        Handle window state change event
        """

        QMainWindow.changeEvent(self.window, event)

        if event.type() == QEvent.WindowStateChange:
            config.ui.maximised = self.window.isMaximized()


    def event_keypress(self, event: QKeyEvent) -> None:
        """
        Handle keyboard hotkey events
        """

        # Ignore key repeats
        if event.isAutoRepeat(): return

        key = event.key()
        mod = event.modifiers()
        mod = None if mod == Qt.KeyboardModifier.NoModifier else mod

        if mod == Qt.KeyboardModifier.AltModifier and key == Qt.Key.Key_Alt:
            # Toggle top menu bar visibility
            self.menu_bar.setHidden(not self.menu_bar.isHidden())

            # Update menu bar focus
            if self.menu_bar.isHidden():
                self.menu_bar.clearFocus()
            else:
                self.menu_bar.setFocus()

        elif mod == None and key == Qt.Key.Key_F1:
            # Show wavebin About dialog
            self.menu_bar.menu_help_about()

        elif mod == None and key == Qt.Key.Key_F:
            # Toggle filled area under waveform traces 
            if config.file: self.plot.toggle_trace_fill()
        
        elif mod == None and key == Qt.Key.Key_I:
            # Show waveform properties dialog
            if config.file: self.menu_bar.menu_view_props()
