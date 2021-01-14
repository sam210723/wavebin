from . import enums, tuples, filters

import argparse
import struct
from PyQt5 import QtWidgets as qt
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import pyqtgraph as pg
import ntpath
import numpy as np

### Globals ###
args = None
file_header = None
wave_headers = []
waveforms = []
wave_colours = [(242, 242, 0), (100, 149, 237), (255, 0, 0), (255, 165, 0)]
x_limit = 50000
version = "1.3"
width = 1500
height = 600
bg = "black"
detail_items = [
    "Sample Points",
    "Averaging",
    "Display Range",
    "Device",
    "Date",
    "Time",
    "Filtering"
]

def init():
    global args
    global file_header
    global wave_headers

    # Parse CLI arguments
    args = parse_args()

    # Print version
    print(f"wavebin v{version}\n")

    # Open bin file
    print(f"Loading \"{args.BIN}\"...")
    bin_file = open(args.BIN, mode="rb")
    
    # Read and parse File Header
    file_header = parse_file_header( bin_file.read(0x0C) )
    if args.v: print_file_header(file_header)

    # Read and parse Waveform Headers
    for i in range(file_header.waveforms):
        data = bin_file.read(0x8C)
        wave_header = parse_wave_header(data)
        wave_headers.append(wave_header)
        if args.v: print_wave_header(wave_header)

        # Read and parse Data Header
        data_header = parse_data_header( bin_file.read(0x0C) )
        if args.v: print_data_header(data_header)

        # Parse Waveform Data
        parse_data(data_header, bin_file.read(data_header.length))

    # Close bin file
    bin_file.close()

    # Show number of waveforms
    print(f"Rendering {len(waveforms)} waveform", end="")
    if len(waveforms) > 1: print("s", end="")
    print("...")

    # Render plots
    render()


### Render Functions ###
def render():
    """
    Renders waveform data using PyQtGraph
    """

    # Create Qt app
    app = qt.QApplication([])
    
    # Create Qt widgets
    window = qt.QWidget()
    layout = qt.QHBoxLayout()
    pgplot = pg.PlotWidget()
    detail = qt.QTableWidget()

    # Setup window
    window.setWindowTitle(f"{ntpath.basename(args.BIN)} - wavebin v{version}")
    window.resize(width, height)
    window.setLayout(layout)
    window.setStyleSheet(f"background-color: {bg};")
    window.setWindowIcon(qtg.QIcon('icon.ico'))

    # Setup layout
    layout.addWidget(pgplot)
    layout.addWidget(detail)
    layout.setContentsMargins(10, 0, 0, 10)
    layout.setSpacing(30)
    detail.setFixedWidth(300)

    # Setup detail table
    detail.setStyleSheet("border: 1px solid black; background-color: black; gridline-color: #555;"\
                         "color: white; font-weight: normal; font-size: 17px;")
    detail.setRowCount(len(detail_items))
    detail.setColumnCount(2)
    detail.verticalHeader().setVisible(False)
    detail.horizontalHeader().setVisible(False)
    detail.horizontalHeader().setSectionResizeMode(qt.QHeaderView.Stretch)
    detail.setEditTriggers(qt.QAbstractItemView.NoEditTriggers)
    detail.setFocusPolicy(qtc.Qt.NoFocus)
    detail.setSelectionMode(qt.QAbstractItemView.NoSelection)


    # Set detail names
    for i, s in enumerate(detail_items):
        detail.setItem(i, 0, qt.QTableWidgetItem(f" {s}"))

    # Set detail values
    header = wave_headers[0]
    detail.setItem(0, 1, qt.QTableWidgetItem(f" {header.points}"))
    detail.setItem(1, 1, qt.QTableWidgetItem(" {}".format("None" if header.count == 1 else header.count)))
    detail.setItem(2, 1, qt.QTableWidgetItem(f" {round(header.x_d_range * float(10**6), 3)} μs"))
    detail.setItem(3, 1, qt.QTableWidgetItem(" {}".format(header.frame.decode().split(":")[0])))
    detail.setItem(4, 1, qt.QTableWidgetItem(f" {header.date.decode()}"))
    detail.setItem(5, 1, qt.QTableWidgetItem(f" {header.time.decode()}"))
    detail.setItem(6, 1, qt.QTableWidgetItem(" {}".format("Savitzky-Golay" if args.f else "None")))

    # Bold left column
    f = qtg.QFont()
    f.setBold(True)
    for i in range(len(detail_items)):
        detail.item(i, 0).setFont(f)


    # Loop through waveforms
    for i, w in enumerate(waveforms):
        header = wave_headers[i]

        # Generate X points
        start = header.x_d_origin
        stop = header.x_d_origin + header.x_d_range
        x = np.linspace(start, stop, len(w))

        # Build plot
        pgplot.setLabel('bottom', "Time", units='s')
        pgplot.setLabel('left', enums.Units(header.y_units).name, units=enums.UnitAbbr(header.y_units).name)
        pgplot.showGrid(x=True, y=True, alpha=1.0)
        pgplot.setMouseEnabled(x=True, y=False)

        # Add data to plot
        pgplot.plot(x, w, pen=pg.mkPen(wave_colours[i], width=2))

        # Add waveform specific details
        r = detail.rowCount()
        detail.insertRow(r)
        detail.setItem(r, 0, qt.QTableWidgetItem(f" Waveform {header.label.decode()}"))
        detail.setItem(r, 1, qt.QTableWidgetItem(f" {enums.WaveType(header.wave_type).name}"))
        detail.item(r, 0).setForeground(qtg.QBrush(qtg.QColor(*wave_colours[i])))
        detail.item(r, 0).setFont(f)

    
    # Run Qt app
    window.show()
    app.exec_()


### Parse Functions ###
def parse_file_header(data):
    """
    Parses file header into Named Tuple
    """

    # Unpack header fields
    fields = struct.unpack("2s2s2i", data)
    file_header = tuples.FileHeader(*fields)
    
    # Check file signature
    if (file_header.signature.decode() != "AG"):
        print("UNEXPECTED FILE SIGNATURE\nExiting...\n")
        exit(1)

    return file_header

def parse_wave_header(data):
    """
    Parses waveform header into Named Tuple
    """
    
    # Get header length
    header_len = data[0]

    # Unpack header fields
    fields = struct.unpack("5if3d2i16s16s24s16sdI", data[:header_len])
    wave_header = tuples.WaveHeader(*fields)

    return wave_header

def parse_data_header(data):
    """
    Parses data header into Named Tuple
    """

    # Get header length
    header_len = data[0]

    # Unpack header fields
    fields = struct.unpack("i2hi", data[:header_len])
    data_header = tuples.DataHeader(*fields)

    return data_header

def parse_data(header, data):
    """
    Parse waveform data field
    """

    arr = np.frombuffer(data, dtype=np.float32)

    # Subsample waveform points for large captures
    if (len(arr) > int(args.s)):
        print("Subsampling large waveform capture ({} -> {} points)...".format(len(arr), int(args.s)))
        arr = arr[::int(len(arr) / int(args.s))]
    
    # Waveform filtering
    if args.f:
        print("Applying Savitzky-Golay low-pass filter...")

        # Calculate window length
        window_len = round(len(arr) * 0.025)
        if window_len % 2 == 0: window_len += 1

        # Filter waveform points
        filtered = filters.savitzky_golay(arr, window_len, 2)
        waveforms.append(filtered)
    else:
        waveforms.append(arr)


### Print Functions ###
def print_file_header(header):
    # Print file info
    size = round(header.size / 1024, 2)
    print(f"File Size:\t\t{size} KB")
    print(f"Waveforms:\t\t{header.waveforms}\n")

def print_wave_header(header):
    label = header.label.decode().rstrip('\0')
    print(f"Waveform {label}:")

    t = enums.WaveType(header.wave_type).name
    print(f"  - Wave Type:\t\t{t}")
    print(f"  - Wave Buffers:\t{header.buffers}")
    print(f"  - Sample Points:\t{header.points}")
    print(f"  - Average Count:\t{header.count}")

    rng = round(header.x_d_range * float(10**6), 3)
    print(f"  - X Display Range:\t{rng} μs")

    dorigin = round(header.x_d_origin * float(10**6), 3)
    print(f"  - X Display Origin:\t{dorigin} μs")

    increment = round(header.x_increment * float(10**9), 3)
    print(f"  - X Increment:\t{increment} ns")
    
    origin = round(header.x_origin * float(10**6), 3)
    print(f"  - X Origin:\t\t{origin} μs")
    
    print(f"  - X Units:\t\t{enums.Units(header.x_units).name}")
    print(f"  - Y Units:\t\t{enums.Units(header.y_units).name}")
    print(f"  - Date:\t\t{header.date.decode()}")
    print(f"  - Time:\t\t{header.time.decode()}")
    
    frame = header.frame.decode().split(":")
    print(f"  - Frame Type:\t\t{frame[0]}")
    print(f"  - Frame Serial:\t{frame[1]}")
    
    print(f"  - Waveform Label:\t{header.label.decode()}")
    print(f"  - Time Tags:\t\t{header.time_tags}")
    print(f"  - Segment Number:\t{header.segment}\n")

def print_data_header(header):
    data_type = enums.DataType(header.type).name
    print(f"[DATA] Type: {data_type}    Depth: {header.bpp * 8} bits    Length: {header.length} bytes\n\n")


def parse_args():
    """
    Parses command line arguments
    """

    argp = argparse.ArgumentParser()
    argp.prog = "wavebin"
    argp.description = "Keysight/Agilent oscilloscope waveform file viewer and converter."
    argp.add_argument("-f", action="store_true", help="Apply a filter to each waveform")
    argp.add_argument("-v", action="store_true", help="Enable verbose output")
    argp.add_argument("-s", action="store", help="Waveform subsampling threshold", default=x_limit)
    argp.add_argument("BIN", action="store", help="Path to waveform file (.bin)")

    return argp.parse_args()


try:
    init()
except KeyboardInterrupt:
    print("Exiting...\n")
    exit()
