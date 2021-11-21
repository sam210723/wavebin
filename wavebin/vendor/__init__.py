"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from pathlib import Path


class Vendor:
    """
    Base class for vendor-specific capture file parsers
    """

    def __init__(self, name: str, site: str, docs: str, devices: list, exts: list, data: bytes):
        self.vendor_name: str = name    # Plain-text vendor name
        self.vendor_site: str = site    # Vendor website URL
        self.vendor_docs: str = docs    # File format documentation URL
        self.devices: list = devices    # List of vendor devices tested with wavebin
        self.extensions: list = exts    # List of supported file extensions
        print(f"Detected {self.vendor_name} waveform file")

        self.data = data                # Capture file byte array
        self.offset = 0                 # Current byte offset in data array
        self.parsed = False             # Flag set when parsing finished
        self.count = 0                  # Number of waveform channels
        self.sample_rate = 0            # Capture sample rate
        self.duration = 0               # Capture duration
        self.channels = []              # Capture channel list


    def info(self):
        """
        Print vendor information
        """

        print(f"{self.vendor_name} ({self.vendor_site})")
        print(f"  {', '.join(self.devices)}")
        print(f"  {', '.join(self.extensions)}\n")


    def open(self, path: Path) -> bool:
        """
        Open waveform capture file

        Args:
            path (pathlib.Path): Path to waveform capture file
        """

        # Check file exists
        if not path.is_file(): return False

        # Read contents into byte array
        with open(path, "rb") as fh:
            self.data = fh.read()
        return True


    def human_format(self, num: int | float, binary: bool = False, sep=' ', unit: str = "") -> str:
        """
        Format numbers as human-readable strings

        Args:
            num (int | float): Number to format
            binary (bool, optional): Divide by 1024 instead of 1000. Defaults to False.
            sep (str, optional): Number and unit separating character
            unit (str, optional): Unit to append to formatted string

        Returns:
            str: Formatted number string
        """

        magnitude = 0                               # Number of magnitudes away from original number
        divmul = 1024.0 if binary else 1000.0       # Divisor/Multiplier between magnitudes
        num = float(f"{num:.3g}")                   # Number as three digit float
        
        if num > 1:
            # Larger SI prefixes
            while abs(num) >= divmul:
                magnitude += 1
                num /= divmul
            prefix = ['', 'k', 'M', 'G', 'T', 'P'][magnitude]

        elif num < 1:
            # Smaller SI prefixes
            while abs(num) <= divmul:
                magnitude += 1
                num *= divmul
            prefix = ['', 'm', 'μ', 'n', 'p', 'f'][magnitude]
        else:
            # Number is 1
            prefix = ""

        # Append prefix and units
        digits = f"{round(num, 2)}".rstrip('0').rstrip('.')
        return f"{digits}{sep}{prefix}{unit}"


def vendor_detect(path: Path) -> Vendor:
    """
    Detect vendor of waveform capture

    Args:
        path (Path): Path to waveform file as pathlib Path object

    Returns:
        Vendor: Instance of KeysightWaveform, RigolWaveform or SiglentWaveform
    """

    # Read file contents in binary mode
    with open(path, "rb") as fh: data = fh.read()

    # Detect waveform capture vendor
    if data[0:2] == b'AG':
        # Keysight/Agilent
        from wavebin.vendor.keysight import KeysightWaveform
        return KeysightWaveform(data)
    elif data[0:2] == b'RG':
        # Rigol
        from wavebin.vendor.rigol import RigolWaveform
        return RigolWaveform(data)
    elif data[0:4] == b'\x02\x00\x00\x00':  #TODO: This is probably wrong
        # Siglent
        from wavebin.vendor.siglent import SiglentWaveform
        return SiglentWaveform(data)
    else:
        return None
