from . import enums, tuples

import argparse
import struct
from magnitude import mg
from PyQt5 import QtWidgets as qt
import numpy as np
import pyqtgraph as pg

### Globals ###
args = None
file_header = None
wave_headers = []
data_header = None
waveforms = []


def init():
    global args
    global file_header
    global wave_headers
    global data_header

    # Parse CLI arguments
    args = parse_args()

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

    # Render plots
    render()


### Render Functions ###
def render():
    """
    Renders waveform data using PyQtGraph
    """
    
    print(f"Rendering {len(waveforms)} waveform", end="")
    if len(waveforms) > 1: print("s", end="")
    print("...")

    # Loop through waveforms
    for i, w in enumerate(waveforms):
        header = wave_headers[i]

        # Generate X points
        start = header.x_d_origin
        stop = header.x_d_origin + header.x_d_range
        num = header.x_d_range / header.x_increment
        x = np.linspace(start, stop, num)

        pg.plot(x, w)


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

    rng = mg(header.x_d_range, unit="s", ounit="us")
    print(f"  - X Display Range:\t{rng}")

    dorigin = mg(header.x_d_origin, unit="s", ounit="us")
    print(f"  - X Display Origin:\t{dorigin}")

    increment = mg(header.x_increment, unit="s", ounit="ns")
    print(f"  - X Increment:\t{increment}")
    
    origin = mg(header.x_origin, unit="s", ounit="us")
    print(f"  - X Origin:\t\t{origin}")
    
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
    print(f"[DATA] Type: {data_type}    Depth: {header.bpp * 8} bits    Length: {header.length} bytes")


def parse_args():
    """
    Parses command line arguments
    """

    argp = argparse.ArgumentParser()
    argp.prog = "wavebin"
    argp.description = "Keysight/Agilent oscilloscope waveform file viewer and converter."
    argp.add_argument("-v", action="store_true", help="Enable verbose output")
    argp.add_argument("BIN", action="store", help="Path to waveform file (.bin)")

    return argp.parse_args()


try:
    init()
except KeyboardInterrupt:
    print("Exiting...\n")
    exit()
