"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for oscilloscopes.
"""

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

    def info(self):
        """
        Print vendor information
        """

        print(f"{self.vendor_name} ({self.vendor_site})")
        print(f"  {', '.join(self.devices)}")
        print(f"  {', '.join(self.extensions)}\n")
