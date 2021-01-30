"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

__version__ = 2.0


def init():
    print(f"wavebin v{__version__}\n")

    safe_exit()


def safe_exit(msg=True, code=0):
    if msg: print("Exiting...")
    exit(code)

try:
    init()
except KeyboardInterrupt:
    safe_exit()
