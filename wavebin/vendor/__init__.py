"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for oscilloscopes.
"""

from pathlib import Path

class Vendor:
    """
    Base class for vendor-specific capture file parsers
    """

    def __init__(self, name: str, site: str, docs: str, devices: list, exts: list):
        self.vendor_name: str = name     # Plain-text vendor name
        self.vendor_site: str = site     # Vendor website URL
        self.vendor_docs: str = docs     # File format documentation URL
        self.devices: list = devices     # List of vendor devices tested with wavebin
        self.extensions: list = exts     # List of supported file extensions

        self.data = None    # Capture file byte array


    def info(self):
        """
        Print vendor information
        """

        print(f"{self.vendor_name} ({self.vendor_site})")
        print(f"  {', '.join(self.devices)}")
        print(f"  {', '.join(self.extensions)}\n")


    def open(self, file_path: str) -> bool:
        """
        Open waveform capture file

        Args:
            file_path (str): Path to waveform capture file
        """

        # Check file exists
        p = Path(file_path)
        if not p.is_file(): return False

        # Read contents into byte array
        with open(p, "rb") as fh:
            self.data = fh.read()
        return True
