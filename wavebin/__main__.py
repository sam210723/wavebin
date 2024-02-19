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

__version__ = "3.0"     # Application version
__min_py__ = (3, 10)    # Minimum Python version

from wavebin.config import config
from wavebin.interface.window import MainWindow
from wavebin.vendor import Vendor, vendor_detect


# Fix for Windows taskbar icon
from os import name as os_name
if os_name == "nt":
    import ctypes
    appid = f'com.vksdr.wavebin.{__version__}'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)


def main() -> None:
    print(
        "                              __    _        \n" +
        "   _      ______ __   _____  / /_  (_)___    \n" +
        "  | | /| / / __ `/ | / / _ \\/ __ \\/ / __ \\\n" +
        "  | |/ |/ / /_/ /| |/ /  __/ /_/ / / / / /   \n" +
       f"  |__/|__/\\__,_/ |___/\\___/_.___/_/_/ /_/  v{__version__}\n\n" +
       f"    {config.app.desc}\n" +
        "         https://wavebin.vksdr.com\n\n"
    )

    # Check minimum Python version requirement
    if sys.version_info[1] < __min_py__[1]:
        print(f"Python {__min_py__[0]}.{__min_py__[1]} or newer is required to run wavebin")
        exit(1)

    # Parse CLI arguments
    args = parse_args()

    # Check for update on GitHub
    config.app.update = update_check()
    if config.app.update:
        print(f"A new version of wavebin is available")
        print("Run \"pip install --upgrade wavebin\" to install it\n")

    # Load configuration from file
    #config = load_config(args, update)

    # Load file from -i argument
    if config.file:
        waveform = open_waveform(config.file)
        if not waveform: safe_exit(code=1)
        config['waveform'] = waveform

    # Create Qt application
    app = MainWindow(safe_exit, open_waveform)

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

    argp = argparse.ArgumentParser()
    argp.prog = "wavebin"

    argp.add_argument("-i", action="store", help="path to waveform capture file", default=None, dest="file")
    argp.add_argument("-v", action="store_true", help="enable verbose logging mode")
    argp.add_argument("-r", action="store_true", help="reset configuration to defaults")

    return argp.parse_args()


def load_config(args: argparse.Namespace, update: bool = False) -> dict:
    """
    Load configuration options from file

    Args:
        args (argparse.Namespace): Parsed command line arguments.
        update (bool): True if update is available on GitHub. Defaults to False.

    Returns:
        dict: Configuration options
    """

    # Check for existing configuration file
    config_path = Path(appdirs.user_config_dir("wavebin", "")) / "wavebin.ini"
    if config_path.is_file() and not args.r:
        if args.v: print(f"Loading configuration \"{config_path}\"")

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
            "height":      800,
            "maximised":   False
        }
        if args.r: print("Configuration reset to defaults") 

        # Save default configuration to file
        save_config(config_dict)

    # Add non-persistent options
    config_dict['version'] = __version__
    config_dict['verbose'] = args.v
    config_dict['config.app.desc'] = config.app.desc
    config_dict['update'] = update
    config_dict['file'] = Path(args.file) if args.file else None

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
    rmkeys = ["verbose", "config.app.desc", "update", "file", "waveform"]
    for _, key in enumerate(rmkeys):
        if key in config: del config[key]

    # Prepare configuration object
    cfgp = configparser.ConfigParser()
    cfgp._sections['wavebin'] = config

    # Write configuration to file
    with open(config_path, "w") as fh:
        cfgp.write(fh)
    return True


def update_check() -> bool:
    """
    Check for update on GitHub

    Returns:
        bool: True if update available
    """

    import json
    import urllib.request
    import urllib.error

    # Build update check request
    url = "https://api.github.com/repos/sam210723/wavebin/releases/latest"
    headers = { "User-Agent": "sam210723/wavebin update_check" }
    req = urllib.request.Request(url, None, headers)
    
    # Send update check request and parse response
    try:
        res = urllib.request.urlopen(req)
        data = json.loads(res.read())
        return f"v{__version__}" != data['tag_name']
        
    except urllib.error.HTTPError as e:
        print(f"Failed to check for updates on GitHub ({e})")
        return False


def open_waveform(path: Path) -> Vendor:
    """
    Open waveform file, parse, then update UI

    Args:
        path (Path): Path to waveform file as pathlib Path object
    
    Returns:
        Vendor or None: None when file format is unknown, otherwise instance of Vendor
    """

    # Detect waveform vendor
    print(f"Opening \"{path.name}\"")
    waveform = vendor_detect(path)

    if waveform:
        # Known file type
        if waveform.parsed:
            return waveform
        else:
            print(f"Unable to parse waveform file \"{path.name}\"")
    else:
        # Unknown file type
        print(f"Unknown file format \"{path.name}\"")
        return None


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
