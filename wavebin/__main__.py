from . import enums, tuples

import argparse
import struct
from magnitude import mg

args = None
file_header = None
wave_header = None
data_header = None

def init():
    global args
    global file_header
    global wave_header
    global data_header

    # Parse CLI arguments
    args = parse_args()

    # Read bin file
    print("Opening \"{}\"\n".format(args.BIN))
    bin_bytes = open(args.BIN, mode="rb").read()
    
    # Parse File Header
    file_header = parse_file_header(bin_bytes[:12])
    print_file_header(file_header)

    # Parse Waveform Header
    wave_header = parse_wave_header(bin_bytes[12:])
    print_wave_header(wave_header)

    # Parse Data Header
    data_header = parse_data_header(bin_bytes[152:])
    print_data_header(data_header)


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


def print_file_header(header):
    # Print file info
    size = round(header.size / 1024, 2)
    print("File Size:           {} KB".format(size))
    print("Waveforms:           {}\n".format(header.waveforms))

def print_wave_header(header):
    print("Waveform {}:".format(header.label.decode().rstrip('\0')))
    print("  - Wave Type:           {}".format(enums.WaveType(header.wave_type).name))
    print("  - Wave Buffers:        {}".format(header.buffers))
    print("  - Sample Points:       {}".format(header.points))
    print("  - Average Count:       {}".format(header.count))
    rng = mg(header.x_d_range, unit="s", ounit="us")
    print("  - X Display Range:     {}".format(rng))
    dorigin = mg(header.x_d_origin, unit="s", ounit="us")
    print("  - X Display Origin:    {}".format(dorigin))
    increment = mg(header.x_increment, unit="s", ounit="ns")
    print("  - X Increment:         {}".format(increment))
    origin = mg(header.x_origin, unit="s", ounit="us")
    print("  - X Origin:            {}".format(origin))
    print("  - X Units:             {}".format(enums.Units(header.x_units).name))
    print("  - Y Units:             {}".format(enums.Units(header.y_units).name))
    print("  - Date:                {}".format(header.date.decode()))
    print("  - Time:                {}".format(header.time.decode()))
    frame = header.frame.decode().split(":")
    print("  - Frame Type:          {}".format(frame[0]))
    print("  - Frame Serial:        {}".format(frame[1]))
    print("  - Waveform Label:      {}".format(header.label.decode()))
    print("  - Time Tags:           {}".format(header.time_tags))
    print("  - Segment Number:      {}\n".format(header.segment))

def print_data_header(header):
    data_type = enums.DataType(header.type).name
    print("[DATA] Type: {}    Depth: {} bits    Length: {} bits".format(data_type, header.bpp*8, header.length))


def parse_args():
    """
    Parses command line arguments
    """

    argp = argparse.ArgumentParser()
    argp.prog = "wavebin"
    argp.description = "Keysight/Agilent oscilloscope waveform file viewer and converter."
    argp.add_argument("BIN", action="store", help="Path to waveform file (.bin)")

    return argp.parse_args()


try:
    init()
except KeyboardInterrupt:
    print("Exiting...\n")
    exit()
