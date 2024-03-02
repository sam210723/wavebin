"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

import appdirs
import configparser
from dataclasses import dataclass, asdict, field
import logging
from pathlib import Path
from pprint import pformat

from wavebin.vendor import Vendor, vendor_detect


@dataclass
class App():
    """
    General application settings
    """

    name: str = "wavebin"               # Application name
    version: str = "3.0"                # Application version
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

    # Configuration file path
    path: Path = Path(
        appdirs.user_config_dir(
            appname="wavebin",
            appauthor="",
            roaming=False
        )
    ) / "wavebin.ini"

    # Parsed waveform object
    _waveform: Vendor = field(
        repr=False,
        init=False,
        default=None    # type: ignore
    )

    @property
    def waveform(self) -> Vendor: return self._waveform

    @waveform.setter
    def waveform(self, path: Path):
        #TODO: Needs fixing when Vendor class is re-written
        if isinstance(path, Path):
            try:
                w: Vendor = vendor_detect(path)
                if w.parsed: self._waveform = w
            except RuntimeError as e:
                logging.error(e)


    def load(self, reset: bool = False) -> bool:
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
        logging.debug('Loading configuration')
        parser = configparser.ConfigParser()
        parser.read(str(self.path.absolute()))

        # Update dataclass values
        self.ui.width = parser.getint('ui', 'width')
        self.ui.height = parser.getint('ui', 'height')
        self.ui.maximised = parser.getboolean('ui', 'maximised')

        # Log current configuration
        logging.debug(f"Configuration loaded from \"{self.path.absolute()}\"")
        for l in self.print(): logging.debug(l)

        return True


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

            logging.debug(f"Configuration saved to \"{self.path.absolute()}\"")
            return True

        except OSError as e:
            logging.error(f"Failed to save configuration file\n{e}")
            return False


    def print(self) -> list[str]:
        """
        Pretty print configuration options
        """

        return pformat(
            config,
            width=1,
            sort_dicts=False
        ).split('\n')


config = Configuration(App(), UI())
