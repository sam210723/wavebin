import appdirs
from dataclasses import dataclass
import logging
from pathlib import Path

from wavebin import __main__ as main
from wavebin.vendor import Vendor


@dataclass
class App():
    """
    General application settings
    """

    name: str = "wavebin"               # Application name
    version: str = main.__version__     # Application version
    update: bool = False                # Update available on GitHub

    # Log file path
    log: Path = Path(
        appdirs.user_config_dir(
            appname="wavebin",
            appauthor="",
            roaming=False
        )
    ) / "wavebin.log"


@dataclass
class UI():
    """
    User interface settings
    """

    width: int = 1400                   # Main window width
    height: int = 800                   # Main window height
    maximised: bool = False             # Maximised state


@dataclass
class Configuration():
    app: App                            # General application settings
    ui: UI                              # User interface settings
    file: Path = None                   # Path to waveform capture file
    waveform: Vendor = None             # Parsed waveform object


    def load(self, reset: bool = False):
        """
        Load configuration from file
        """

        # Log current configuration
        logging.debug(str(config).replace("Configuration(", "Configuration ("))

        # Reset configuration if requested
        if reset:
            #TODO: Apply default configuration
            logging.info('Resetting configuration')

            # Log default configuration
            logging.debug(str(config).replace("Configuration(", "Configuration ("))


    def save(self):
        """
        Save configuration to file
        """

        pass


config = Configuration(App(), UI())
