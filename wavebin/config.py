from dataclasses import dataclass
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
    verbose: bool = False               # Output extra log messages
    update: bool = False                # Update available on GitHub


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


    def save(self, path: Path | str):
        """
        Save configuration to file
        """

        # Convert string path to pathlib Path
        if isinstance(path, str): path = Path(path)


config = Configuration(App(), UI())
