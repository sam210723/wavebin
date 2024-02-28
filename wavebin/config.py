import appdirs
import configparser
from dataclasses import dataclass, asdict, make_dataclass
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
    file: Path = None                   # Path to waveform capture file     # type: ignore
    waveform: Vendor = None             # Parsed waveform object            # type: ignore

    # Configuration file path
    path: Path = Path(
        appdirs.user_config_dir(
            appname="wavebin",
            appauthor="",
            roaming=False
        )
    ) / "wavebin.ini"


    def load(self, reset: bool = False):
        """
        Load configuration from file
        """

        # Skip if configuration file does not exist
        if not self.path.is_file(): return True

        # Ignore stored configuration reset requested
        if reset:
            logging.info('Resetting configuration')
            return True

        # Prepare configuration object
        logging.info('Loading configuration')
        parser = configparser.ConfigParser()
        parser.read(str(self.path.absolute()))

        # Update dataclass values
        self.ui.width = parser.getint('ui', 'width')
        self.ui.height = parser.getint('ui', 'height')
        self.ui.maximised = parser.getboolean('ui', 'maximised')

        # Log current configuration
        logging.debug(str(config).replace("Configuration(", "Configuration ("))


    def save(self) -> bool:
        """
        Save configuration to file
        """

        # Create folders for configuration file
        self.path.parent.mkdir(parents=True, exist_ok=True)

        # Prepare configuration object
        parser = configparser.ConfigParser()
        parser.add_section('ui')

        # Add configuration options
        parser['ui'] = asdict(self.ui)

        # Write configuration to file
        try:
            with open(str(self.path.absolute()), "w") as fh:
                parser.write(fh)
            return True

        except OSError as e:
            logging.error(e)
            return False


config = Configuration(App(), UI())
