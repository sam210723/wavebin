"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

from argparse import ArgumentParser
from pathlib import Path

__version__ = 2.0


def init():
    # Banner
    print("                              __    _        ")
    print("   _      ______ __   _____  / /_  (_)___    ")
    print("  | | /| / / __ `/ | / / _ \\/ __ \\/ / __ \\")
    print("  | |/ |/ / /_/ /| |/ /  __/ /_/ / / / / /   ")
    print(f"  |__/|__/\\__,_/ |___/\\___/_.___/_/_/ /_/  v{__version__}\n")
    print("             vksdr.com/wavebin\n\n")

    # Parse CLI arguments
    args = parse_args()
    if args.o: args.o = Path(args.o)
    
    # Print startup info
    print_info(args)

    # Gracefully exit application
    safe_exit(False)


def parse_args():
    argp = ArgumentParser(description="Waveform capture viewer for Keysight oscilloscopes.")
    argp.prog = "wavebin"

    argp.add_argument("-o", action="store", help="Path to Keysight waveform capture file (.bin)", default=None)
    argp.add_argument("-v", action="store_true", help="Enable verbose logging mode", default=None)

    return argp.parse_args()


def print_info(args):
    if args.o: print(f"Opening \"{args.o.name}\"...")
    print()


def safe_exit(msg=True, code=0):
    if msg: print("Exiting...")
    exit(code)

try:
    init()
except KeyboardInterrupt:
    safe_exit()
