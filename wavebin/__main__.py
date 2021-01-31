"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

from argparse import ArgumentParser
from pathlib import Path
import sys

from wavebin.interface import QtApp
from wavebin.plot import QtPlot
from wavebin.wave import WaveParser

__version__ = 2.0


def init():
    print( "                              __    _        ")
    print( "   _      ______ __   _____  / /_  (_)___    ")
    print( "  | | /| / / __ `/ | / / _ \\/ __ \\/ / __ \\")
    print( "  | |/ |/ / /_/ /| |/ /  __/ /_/ / / / / /   ")
    print(f"  |__/|__/\\__,_/ |___/\\___/_.___/_/_/ /_/  v{__version__}\n")
    print( "             vksdr.com/wavebin\n\n")

    # Parse CLI arguments
    args = parse_args()
    if args.file: args.file = Path(args.file)
    
    # Print startup info
    print_info(args)

    # Setup waveform capture parser
    wave = WaveParser({
        "verbose":     args.v,
        "file":        args.file,
        "app_update":  app.update,
        "plot_update": plot.update
    })
    #TODO: Update UI callback when parse complete

    # Create Qt application
    app = QtApp({
        "verbose":    args.v,
        "version":    __version__,
        "file":       args.file,
        "width":      1500,
        "height":     700,
        "opengl":     not args.no_opengl,
        "wave_parse": wave.parse
    })

    # Create Qt waveform plot
    plot = QtPlot({
        "verbose": args.v,
        "opengl":  not args.no_opengl
    })

    # Add plot to main window
    app.add_plot(plot)

    # Run application
    app.run()

    # Gracefully exit application
    safe_exit()


def parse_args():
    argp = ArgumentParser(description="Waveform capture viewer for Keysight oscilloscopes.")
    argp.prog = "wavebin"

    argp.add_argument("-i", action="store", help="path to Keysight waveform capturefile (.bin)", default=None, dest="file")
    argp.add_argument("-v", action="store_true", help="enable verbose logging mode")
    argp.add_argument("--no-opengl", action="store_true", help="disable hardware accelerated rendering with OpenGL")

    return argp.parse_args()


def print_info(args):
    if args.no_opengl and args.v: print("OpenGL disabled")


def safe_exit(msg=True, code=0):
    if msg: print("Exiting...")
    sys.exit(code)


try:
    init()
except KeyboardInterrupt:
    safe_exit()
