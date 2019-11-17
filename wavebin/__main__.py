from . import enums, tuples

import argparse
import struct
from magnitude import mg

args = None
file_header = None
wave_header = None

def init():
    global args
    global file_header
    global wave_header

    # Parse CLI arguments
    args = parse_args()

    # Read bin file
    print("Opening \"{}\"\n".format(args.BIN))
    bin_bytes = open(args.BIN, mode="rb").read()
    
    # Parse file header
    file_header = parse_file_header(bin_bytes[:12])

    # Parse Waveform Header
    wave_header = parse_wave_header(bin_bytes[12:])


def parse_wave_header(data):
    """
    Parses waveform header into Named Tuple
    """
    
    # Get header length
    header_len = data[0]

    # Unpack header fields
    fields = struct.unpack("5if3d2i16s16s24s16sdI", data[:header_len])
    wave_header = tuples.WaveHeader(*fields)

    # Print waveform info
    print("Waveform {}:".format(wave_header.label.decode().rstrip('\0')))
    print("  - Wave Type:           {}".format(enums.WaveType(wave_header.wave_type).name))
    print("  - Wave Buffers:        {}".format(wave_header.buffers))
    print("  - Sample Points:       {}".format(wave_header.points))
    print("  - Average Count:       {}".format(wave_header.count))
    rng = mg(wave_header.x_d_range, unit="s", ounit="us")
    print("  - X Display Range:     {}".format(rng))
    dorigin = mg(wave_header.x_d_origin, unit="s", ounit="us")
    print("  - X Display Origin:    {}".format(dorigin))
    increment = mg(wave_header.x_increment, unit="s", ounit="ns")
    print("  - X Increment:         {}".format(increment))
    origin = mg(wave_header.x_origin, unit="s", ounit="us")
    print("  - X Origin:            {}".format(origin))
    print("  - X Units:             {}".format(enums.Units(wave_header.x_units).name))
    print("  - Y Units:             {}".format(enums.Units(wave_header.y_units).name))
    print("  - Date:                {}".format(wave_header.date.decode()))
    print("  - Time:                {}".format(wave_header.time.decode()))
    frame = wave_header.frame.decode().split(":")
    print("  - Frame Type:          {}".format(frame[0]))
    print("  - Frame Serial:        {}".format(frame[1]))
    print("  - Waveform Label:      {}".format(wave_header.label.decode()))
    print("  - Time Tags:           {}".format(wave_header.time_tags))
    print("  - Segment Number:      {}".format(wave_header.segment))

    return wave_header


def parse_file_header(data):
    """
    Parses file header into Named Tuple
    """

    # Unpack header fields
    fields = struct.unpack("2s2sii", data)
    file_header = tuples.FileHeader(*fields)
    
    # Check file signature
    if (file_header.signature.decode() != "AG"):
        print("UNEXPECTED FILE SIGNATURE\nExiting...\n")
        exit(1)
    
    # Print file info
    size = round(file_header.size / 1024, 2)
    print("File Size:           {} KB".format(size))
    print("Waveforms:           {}\n".format(file_header.waveforms))

    return file_header


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
