"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

import appdirs
import argparse
import configparser
from pathlib import Path
import sys

from wavebin.interface.window import MainWindow
from wavebin.interface.plot import QtPlot
from wavebin.wave import WaveParser

__version__ = "2.2"
description = "Oscilloscope waveform capture viewer"


def main():
    print( "                              __    _        ")
    print( "   _      ______ __   _____  / /_  (_)___    ")
    print( "  | | /| / / __ `/ | / / _ \\/ __ \\/ / __ \\")
    print( "  | |/ |/ / /_/ /| |/ /  __/ /_/ / / / / /   ")
    print(f"  |__/|__/\\__,_/ |___/\\___/_.___/_/_/ /_/  v{__version__}\n")
    print(f"    {description}")
    print( "             vksdr.com/wavebin\n\n")

    # Parse CLI arguments
    args = parse_args()

    # Load configuration from file
    config = load_config(args.v, args.r)

    # Create Qt application
    app = MainWindow(config)

    # Create Qt waveform plot
    """
    plot = QtPlot({
        "verbose":     args.v,
        "opengl":      not args.no_opengl,
        "subsampling": limit,
        "filter_type": 0,
        "clipping":    False,
        "colours": [
            (242, 242, 0),
            (100, 149, 237),
            (255, 0, 0),
            (255, 165, 0)
        ]
    })
    """

    # Set class instances
    #wave.instances(app, plot)
    #app.instances(wave, plot)

    # Add plot to main window
    #app.add_plot(plot)

    # Parse file if path specified in argument
    #if args.file and not wave.parse(args.file): safe_exit(code=1)

    # Run application
    app.run()

    # Gracefully exit application
    safe_exit(config)


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments

    Returns:
        argparse.Namespace: List of arguments
    """

    argp = argparse.ArgumentParser(description=description)
    argp.prog = "wavebin"

    argp.add_argument("-i", action="store", help="Path to waveform capture file", default=None, dest="file")
    argp.add_argument("-v", action="store_true", help="Enable verbose logging mode")
    argp.add_argument("-r", action="store_true", help="Reset configuration to defaults")

    return argp.parse_args()


def load_config(verbose: bool, reset: bool = False) -> dict:
    """
    Load configuration options from file

    Args:
        verbose (bool): Verbose console output flag
        reset (bool): Reset configuration to default. Defaults to False.

    Returns:
        dict: Configuration options
    """

    # Check for existing configuration file
    config_path = Path(appdirs.user_config_dir("wavebin", "")) / "wavebin.ini"
    if config_path.is_file() and not reset:
        if verbose: print(f"Found configuration file at \"{config_path}\"")

        # Load configuration from file
        cfgp = configparser.ConfigParser()
        cfgp.read(config_path)

        # Create configuration object
        config_dict = {
            "width":       cfgp.getint("wavebin", "width"),
            "height":      cfgp.getint("wavebin", "height"),
            "maximised":   cfgp.getboolean("wavebin", "maximised")
        }   
    else:
        # Create default configuration object
        config_dict = {
            "width":       1400,
            "height":      700,
            "maximised":   False
        }
        if reset: print("Configuration reset to defaults") 

        # Save default configuration to file
        save_config(config_dict)
    
    # Add non-persistent options
    config_dict['version'] = __version__
    config_dict['verbose'] = verbose
    config_dict['description'] = description

    return config_dict


def save_config(config: dict) -> bool:
    """
    Save configuration to file

    Args:
        config (dict): Configuration options

    Returns:
        bool: Success flag
    """

    # Create folders for configuration file
    config_path = Path(appdirs.user_config_dir("wavebin", "")) / "wavebin.ini"
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Remove non-persistent options
    rmkeys = ["verbose", "description"]
    for _, key in enumerate(rmkeys):
        if key in config: del config[key]

    # Prepare configuration object
    cfgp = configparser.ConfigParser()
    cfgp._sections['wavebin'] = config

    # Write configuration to file
    with open(config_path, "w") as fh:
        cfgp.write(fh)
    return True


def safe_exit(config: dict = None, code=0) -> None:
    """
    Gracefully exit the application

    Args:
        config (dict): Configuration options. Defaults to None.
        code (int, optional): Code to exit with. Defaults to 0.
    """

    # Save configuration to file
    if config:
        verbose = config['verbose']
        if verbose: print("Saving configuration...")
        save_config(config)

    if verbose: print("Exiting...")
    sys.exit(code)


try:
    if __name__ == "__main__": main()
except KeyboardInterrupt:
    safe_exit()
