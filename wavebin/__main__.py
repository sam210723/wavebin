"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

import argparse

__version__ = 2.0


def init():
    print(f"wavebin v{__version__}\n")

    args = parse_args()

    safe_exit()


def parse_args():
    argp = argparse.ArgumentParser(description="Waveform capture viewer for Keysight oscilloscopes.")
    argp.prog = "wavebin"

    argp.add_argument("-o", action="store", help="Path to Keysight waveform capture file (.bin)", default=None)
    argp.add_argument("-v", action="store_true", help="Enable verbose logging mode", default=None)

    return argp.parse_args()


def safe_exit(msg=True, code=0):
    if msg: print("Exiting...")
    exit(code)

try:
    init()
except KeyboardInterrupt:
    safe_exit()
