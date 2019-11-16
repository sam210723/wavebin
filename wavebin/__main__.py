from argparse import ArgumentParser

def init():
    args = parse_args()
    print(args)


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
