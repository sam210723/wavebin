from argparse import ArgumentParser

def init():
    args = parse_args()

    # Read BIN file
    print("Opening \"{}\"...\n".format(args.BIN))
    bin_bytes = open(args.BIN, mode="rb").read()
    parse_bin(bin_bytes)


def parse_bin(data):
    """
    Parse BIN file
    """

    # File Header
    


def parse_args():
    """
    Parses command line arguments
    """

    argp = ArgumentParser()
    argp.prog = "wavebin"
    argp.description = "Keysight/Agilent oscilloscope waveform file converter"
    argp.add_argument("BIN", action="store", help="Path to waveform file (.bin)")

    return argp.parse_args()


try:
    init()
except KeyboardInterrupt:
    print("Exiting...")
