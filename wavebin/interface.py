"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for oscilloscopes.
"""

from pathlib import Path
from PyQt5 import QtWidgets as qt
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import webbrowser
from wavebin.export import PulseView, WaveFile


class QtApp(qt.QApplication):
    def __init__(self, config):
        super(QtApp, self).__init__([])
        self.config = config
        self.name = f"wavebin v{self.config['version']}"

        # Setup main Qt application
        self.log("Initialising Qt application")
        self.setApplicationDisplayName(self.name)
        self.setApplicationVersion(str(self.config['version']))

        # Create main Qt window
        self.log("Creating main Qt window")
        self.window = qt.QMainWindow()
        self.setup_window()

        # Create main widget
        self.log("Creating main Qt widget")
        self.widget = qt.QWidget()
        self.widget.setStyleSheet("background-color: black;")
        self.window.setCentralWidget(self.widget)
        self.window.setFocus()

        # Create widget layout
        self.log("Creating widget layout")
        self.layout = qt.QGridLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(15)
        self.widget.setLayout(self.layout)

        # Create sidebar widget
        self.sidebar = QtSidebar()
        self.layout.addWidget(self.sidebar, 0, 0)

        # Create file dialogs
        self.ofd = qt.QFileDialog()
        self.sfd = qt.QFileDialog()


    def run(self):
        self.log("Starting Qt application")
        self.window.show()
        self.exec_()


    def update(self):
        self.log("Updating UI")
        self.window.setWindowTitle(f"\"{self.config['file'].name}\"")
        
        # Limit number of points for large captures
        points = len(self.config['wave'].waveforms[0]['data'])
        if points > self.config['limit']:
            subsampling = self.config['limit']
        else:
            subsampling = points

        # Reset sidebar widgets
        self.sidebar.update(
            None,
            None,
            subsampling
        )

        # Enable export options
        self.menu_actions['file_export_pv'].setEnabled(True)
        self.menu_actions['file_export_wav'].setEnabled(True)
        self.menu_actions['view_wave_info'].setEnabled(True)


    def setup_window(self):
        # Styling and icon
        self.window.setWindowIcon(qtg.QIcon("icon.ico"))
        self.window.resize(self.config['width'], self.config['height'])
        self.window.setMinimumSize(800, 200)

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
            "file_open":       qt.QAction("&Open...", self.window),
            "file_export_pv":  qt.QAction("Export to &PulseView...", self.window),
            "file_export_wav": qt.QAction("Export to &WAV file...", self.window),
            "file_----":       None,
            "file_exit":       qt.QAction("E&xit", self.window),
            "view_sidebar":    qt.QAction("&Sidebar", self.window),
            "view_wave_info":  qt.QAction("Waveform &Info", self.window),
            "help_docs":       qt.QAction("&Documentation", self.window),
            "help_shortcuts":  qt.QAction("&Keyboard Shortcuts", self.window),
            "help_----":       None,
            "help_about":      qt.QAction("&About", self.window)
        }

        # Customise menu actions
        self.menu_actions['file_export_pv'].setEnabled(False)
        self.menu_actions['file_export_wav'].setEnabled(False)
        self.menu_actions['view_sidebar'].setCheckable(True)
        self.menu_actions['view_sidebar'].setChecked(True)
        self.menu_actions['view_wave_info'].setEnabled(False)

        # Add actions to menu items
        for a in self.menu_actions:
            if a.split("_")[1] == "----":
                self.menus[a.split("_")[0]].addSeparator()
                continue
            self.menu_actions[a].triggered.connect(eval(f"self.menu_{a}"))
            self.menus[a.split("_")[0]].addAction(self.menu_actions[a])
        
        # Attach keyboard event handler
        self.window.keyPressEvent = self.keyPressEvent


    def instances(self, wave, plot):
        self.config['wave'] = wave
        self.config['plot'] = plot
        self.sidebar.config['wave'] = wave
        self.sidebar.config['plot'] = plot


    def keyPressEvent(self, event):
        key = event.key()

        try:
            char = chr(key)
        except ValueError:
            char = None
        
        if char == 'B':
            self.menu_actions['view_sidebar'].toggle()
            self.sidebar.toggle()


    def menu_file_open(self):
        # Get initial path
        if "file" in self.config:
            initial_path = str(self.config['file'].parents[0])
        else:
            initial_path = "."

        # Show open file dialog
        file_path = self.ofd.getOpenFileName(
            self.window,
            "Open waveform capture",
            initial_path,
            "Waveform files (*.bin);;All files (*.*)"
        )[0]

        # Handle cancelled dialog
        if file_path == "":
            self.log("Open file dialog cancelled")
            return
        
        # Reset sidebar controls
        self.sidebar.update(0, False, -1)

        # Parse waveform capture
        if not self.config['wave'].parse(file_path):
            msgbox = qt.QMessageBox()
            msgbox.setWindowTitle("Error")
            msgbox.setIcon(qt.QMessageBox.Critical)
            msgbox.setStandardButtons(qt.QMessageBox.Ok)
            msgbox.setText(
                f"Error opening \"{Path(file_path).name}\": Unknown file format"
            )
            msgbox.exec_()


    def menu_file_export_pv(self):
        # Show save file dialog
        file_path = self.sfd.getSaveFileName(
            self.window,
            "Export to PulseView",
            f"./{self.config['file'].name.split('.')[0]}.sr",
            "sigrok Sessions (*.sr)"
        )[0]

        # Handle cancelled dialog
        if file_path == "":
            self.log("Save file dialog cancelled")
            return

        # Create PulseView session file
        PulseView(
            self.config['verbose'],
            file_path,
            self.config['plot'].processed_waveforms,
            self.sidebar.config['parts'][1]['widget'].isChecked()
        )
    

    def menu_file_export_wav(self):
        # Check waveform has been clipped
        if not self.sidebar.config['parts'][1]['widget'].isChecked():
            msgbox = qt.QMessageBox()
            msgbox.setWindowTitle("Error")
            msgbox.setIcon(qt.QMessageBox.Critical)
            msgbox.setStandardButtons(qt.QMessageBox.Ok)
            msgbox.setText("Enable waveform clipping before exporting to WAV file")
            msgbox.exec_()
            return

        # Show save file dialog
        file_path = self.sfd.getSaveFileName(
            self.window,
            "Export to WAV file",
            f"./{self.config['file'].name.split('.')[0]}.wav",
            "WAV file (*.wav)"
        )[0]

        # Handle cancelled dialog
        if file_path == "":
            self.log("Save file dialog cancelled")
            return

        # Create WAVE file
        WaveFile(
            self.config['verbose'],
            file_path,
            self.config['plot'].processed_waveforms
        )


    def menu_file_exit(self):
        self.exit()


    def menu_view_sidebar(self):
        self.sidebar.toggle()


    def menu_view_wave_info(self):
        info = ""

        for i, w in enumerate(self.waveforms):
            header = w['header']

            label = header.label.decode().rstrip('\0')
            info += f"Waveform {label}:\n"
            info += f"  - Wave Buffers:\t\t{header.buffers}\n"
            info += f"  - Sample Points:\t\t{header.points}\n"
            info += f"  - Average Count:\t{header.average}\n"

            wave_types = [
                "UNKNOWN",
                "Normal",
                "Peak",
                "Average",
                "",
                "",
                "Logic"
            ]
            info += f"  - Wave Type:\t\t{wave_types[header.wave_type]}\n"

            units = [
                "UNKNOWN",
                "Volts",
                "Seconds",
                "Constant",
                "Amps",
                "Decibels",
                "Hertz"
            ]
            info += f"  - X Units:\t\t{units[header.x_units]}\n"
            info += f"  - Y Units:\t\t{units[header.y_units]}\n"

            rng = round(header.x_d_range * float(10**6), 3)
            info += f"  - X Display Range:\t{rng} μs\n"

            dorigin = round(header.x_d_origin * float(10**6), 3)
            info += f"  - X Display Origin:\t{dorigin} μs\n"

            increment = round(header.x_increment * float(10**9), 3)
            info += f"  - X Increment:\t\t{increment} ns\n"
            
            origin = round(header.x_origin * float(10**6), 3)
            info += f"  - X Origin:\t\t{origin} μs\n"

            frame = header.frame.decode().split(":")
            info += f"  - Frame Type:\t\t{frame[0]}\n"
            info += f"  - Frame Serial:\t\t{frame[1]}\n"
            info += f"  - Date:\t\t\t{header.date.decode()}\n"
            info += f"  - Time:\t\t\t{header.time.decode()}\n"
            
            info += f"  - Waveform Label:\t{header.label.decode()}\n"
            info += f"  - Time Tags:\t\t{header.time_tags}\n"
            info += f"  - Segment Number:\t{header.segment}\n"

            info += "\n"

        # Show messagebox
        msgbox = qt.QMessageBox()
        msgbox.setWindowTitle("Waveform Info")
        msgbox.setIcon(qt.QMessageBox.Information)
        msgbox.setStandardButtons(qt.QMessageBox.Ok)
        msgbox.setText(info)
        self.log("Waveform info dialog launched")
        msgbox.exec_()


    def menu_help_docs(self):
        self.log("Opening docs in default browser")
        webbrowser.open("https://vksdr.com/wavebin", new=2)


    def menu_help_shortcuts(self):
        msgbox = qt.QMessageBox()
        msgbox.setWindowTitle("Keyboard Shortcuts")
        msgbox.setIcon(qt.QMessageBox.Information)
        msgbox.setStandardButtons(qt.QMessageBox.Ok)
        msgbox.setText(
            "B - Toggle sidebar visibility\n"\
            ""
        )
        self.log("Keyboard shortcut dialog launched")
        msgbox.exec_()


    def menu_help_about(self):
        msgbox = qt.QMessageBox()
        msgbox.setWindowTitle("About")
        msgbox.setIcon(qt.QMessageBox.Information)
        msgbox.setStandardButtons(qt.QMessageBox.Ok)
        msgbox.setText(
            "Waveform capture viewer for Agilent, Keysight and Rigol oscilloscopes.\n\n"\
            "Update wavebin by running \"pip install wavebin --upgrade\""
        )
        self.log("About dialog launched")
        msgbox.exec_()


    def add_plot(self, plot):
        self.log("Adding plot widget to layout")
        self.layout.addWidget(plot, 0, 1)


    def log(self, msg):
        if self.config['verbose']: print(msg)


class QtSidebar(qt.QTableWidget):
    def __init__(self):
        super(QtSidebar, self).__init__()

        self.setFixedWidth(300)
        self.setColumnCount(2)
        self.setRowCount(0)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(qt.QHeaderView.Stretch)
        self.setEditTriggers(qt.QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(qtc.Qt.NoFocus)
        self.setSelectionMode(qt.QAbstractItemView.NoSelection)
        self.setStyleSheet(
            "border: none;"\
            "border-right: 1px solid #333;"\
            "background-color: black;"\
            "gridline-color: black;"\
            "color: white;"\
            "font-weight: normal;"\
            "font-size: 17px;"
        )

        self.config = {}
        self.config['parts'] = []
        self.build()
    

    def build(self):
        self.config['parts'].append({"name": "Filter Type", "widget": qt.QComboBox()})
        self.config['parts'].append({"name": "Clipping", "widget": qt.QPushButton("OFF")})
        self.config['parts'].append({"name": "Subsampling", "widget": qt.QSpinBox()})

        # Add filter dropdown options
        self.config['parts'][0]['widget'].addItem("None")
        self.config['parts'][0]['widget'].addItem("Savitzky-Golay")
        self.config['parts'][0]['widget'].currentIndexChanged.connect(self.filter_changed)

        # Set filter window slider properties
        self.config['parts'][1]['widget'].setCheckable(True)
        self.config['parts'][1]['widget'].setStyleSheet("background: red; color: white;")
        self.config['parts'][1]['widget'].clicked.connect(self.clipping_changed)

        # Set subsampling numeric box properties
        self.config['parts'][2]['widget'].setMinimum(2)
        self.config['parts'][2]['widget'].valueChanged.connect(self.subsampling_changed)

        for i, p in enumerate(self.config['parts']):
            # Add new table row
            self.setRowCount(self.rowCount() + 1)

            # Set row name
            self.setItem(i, 0, qt.QTableWidgetItem(p['name']))
            self.setCellWidget(i, 1, p['widget'])
        
        # Bold left column
        f = qtg.QFont()
        f.setBold(True)
        for i, p in enumerate(self.config['parts']):
            self.item(i, 0).setFont(f)
        
        # Remove focus from sidebar widgets
        self.config['parts'][0]['widget'].clearFocus()
        self.config['parts'][1]['widget'].clearFocus()
        self.config['parts'][2]['widget'].clearFocus()


    def update(self, f, c, p):
        if f != None:
            self.config['parts'][0]['widget'].setCurrentIndex(f)
            self.filter_changed(f)
        
        if c != None:
            self.config['parts'][1]['widget'].setChecked(c)
            self.clipping_changed(c)
        
        if p != None:
            # Set subsampling spin box min/max
            self.config['parts'][2]['widget'].setMinimum(2)
            self.config['parts'][2]['widget'].setMaximum(p)
            self.config['parts'][2]['widget'].setValue(p)
            self.subsampling_changed(p)


    def filter_changed(self, value):
        self.config['plot'].config['filter_type'] = value
        self.config['parts'][0]['widget'].clearFocus()

        try:
            self.config['plot'].update()
        except AttributeError:
            return


    def clipping_changed(self, value):
        btn = self.config['parts'][1]['widget']

        if btn.isChecked():
            btn.setText("ON")
            btn.setStyleSheet("background: green; color: white;")
        else:
            btn.setStyleSheet("background: red; color: white;")
            btn.setText("OFF")
        
        self.config['plot'].config['clipping'] = btn.isChecked()
        btn.clearFocus()

        try:
            self.config['plot'].update()
        except AttributeError:
            return


    def subsampling_changed(self, value):
        self.config['plot'].config['subsampling'] = value
        
        try:
            self.config['plot'].update()
        except AttributeError:
            return


    def toggle(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()
