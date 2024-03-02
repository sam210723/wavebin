"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""


import argparse
import logging
from pathlib import Path
import platform
import sys

from wavebin.config import config
from wavebin.interface.window import MainWindow


def main() -> None:
    # Configure file logging
    config.app.log.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=str(config.app.log),
        filemode="w",
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)8s: %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S"
    )

    # Configure console logging
    log_stream = logging.StreamHandler(sys.stdout)
    log_stream.setLevel(logging.INFO)
    logging.getLogger().addHandler(log_stream)

    # Print app header
    logging.info("\n" +
        "                              __    _        \n" +
        "   _      ______ __   _____  / /_  (_)___    \n" +
        "  | | /| / / __ `/ | / / _ \\/ __ \\/ / __ \\\n" +
        "  | |/ |/ / /_/ /| |/ /  __/ /_/ / / / / /   \n" +
       f"  |__/|__/\\__,_/ |___/\\___/_.___/_/_/ /_/  v{config.app.version}\n\n" +
       f"    Oscilloscope waveform capture viewer\n" +
        "         https://wavebin.vksdr.com\n\n"
    )

    # Check Python version
    min_py: tuple = (3, 10)
    if sys.version_info[1] < min_py[1]:
        logging.critical(f"Python {min_py[0]}.{min_py[1]} or newer is required")
        exit(1)

    # Log system info (Python, OS, CPU)
    logging.debug(f"Python {platform.python_version()} on {platform.platform()} {platform.machine()}")

    # Parse args and persistent config
    args = parse_args()
    config.load(args.reset)

    # Check for app updates
    config.app.update = update_check()
    if config.app.update: logging.info("A new version of wavebin is available on GitHub"); print()

    # Load file from argument
    if args.file:
        config.file = Path(args.file)
        config.waveform = config.file
        if not config.waveform: safe_exit(code=1)

    # Launch user interface
    if args.verbose: log_stream.setLevel(logging.DEBUG)
    app = MainWindow()
    app.run()

    # Gracefully exit application
    safe_exit()


def parse_args() -> argparse.Namespace:
    """
    Handle command-line arguments

    Returns:
        argparse.Namespace: Parsed arguments
    """

    argp = argparse.ArgumentParser()
    argp.prog = "wavebin"

    # Configure options
    argp.add_argument("-i", action="store", help="path to waveform capture file", default=None, dest="file")
    argp.add_argument("-v", action="store_true", help="enable verbose logging mode", dest="verbose")
    argp.add_argument("-r", action="store_true", help="reset configuration to defaults", dest="reset")

    args = argp.parse_args()
    logging.debug(f'Arguments {vars(args)}')

    return args


def update_check() -> bool:
    """
    Check for update on GitHub

    Returns:
        bool: True if update available
    """

    import json
    from packaging.version import Version
    import urllib.request
    import urllib.error

    # Build update check request
    url = "https://api.github.com/repos/sam210723/wavebin/releases/latest"
    headers = { 'User-Agent': 'sam210723/wavebin update_check' }
    req = urllib.request.Request(url, None, headers)
    
    # Send update check request and parse response
    try:
        res = urllib.request.urlopen(req, timeout=2)
        latest = json.loads(res.read())['tag_name'][1:]
        update = Version(config.app.version) < Version(latest)
        ahead = Version(config.app.version) > Version(latest)

        logging.debug(
            f"Current release version on GitHub is v{latest}" +
            f", instance {'can be updated' if update else 'is ahead of release' if ahead else 'is up to date'}"
        )
        return (update and not ahead)

    except Exception as e:
        logging.warning(f"Failed to check for updates on GitHub ({e})")
        return False


def safe_exit(code: int = 0) -> None:
    """
    Save configuration and exit the application

    Args:
        code (int, optional): Exit code, defaults to 0
    """

    config.save()
    logging.info("Exiting...")
    sys.exit(code)


try:
    if __name__ == "__main__":
        # Fix for Windows taskbar icon
        from os import name as os_name
        if os_name == "nt":
            import ctypes
            appid = f"com.vksdr.wavebin.{config.app.version}"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

        main()
except KeyboardInterrupt:
    safe_exit()
