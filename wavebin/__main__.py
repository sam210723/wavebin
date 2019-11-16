from . import enums, tuples

import argparse
import struct

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
    header = data[:header_len]

    fields = struct.unpack("5if3d2i16s16s24s16sdI", data[:header_len])
    wave_header = tuples.WaveHeader(*fields)
    print(wave_header)

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
    print("File Size:       {} KB".format(size))
    print("Waveforms:       {}\n".format(file_header.waveforms))

    return file_header


def parse_args():
    """
    Parses command line arguments
    """

    argp = argparse.ArgumentParser()
    argp.prog = "wavebin"
    argp.description = "Keysight/Agilent oscilloscope waveform file converter"
    argp.add_argument("BIN", action="store", help="Path to waveform file (.bin)")

    return argp.parse_args()


try:
    init()
except KeyboardInterrupt:
    print("Exiting...\n")
    exit()
