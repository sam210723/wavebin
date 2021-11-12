"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for oscilloscopes.
"""

class Vendor:
    """
    Base class for vendor-specific binary capture file parsers
    """

    def __init__(self, name: str, site: str, docs: str, devices: list):
        self.vendor_name: str = name     # Plain-text vendor name
        self.vendor_site: str = site     # Vendor website URL
        self.vendor_docs: str = docs     # Binary format documentation URL
        self.devices: list = devices     # List of vendor devices tested with wavebin

    def info(self):
        """
        Print vendor information
        """

        print(f"{self.vendor_name} ({self.vendor_site})")
        for d in self.devices: print(f"  - {d}")
        print()
