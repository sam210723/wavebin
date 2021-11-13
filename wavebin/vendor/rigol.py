"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for oscilloscopes.
"""

from wavebin.vendor import Vendor


class RigolWaveform(Vendor):
    """
    Capture file parser for Rigol oscilloscopes
    """

    def __init__(self):
        super(RigolWaveform, self).__init__(
            "Rigol",
            "https://www.rigolna.com",
            "https://rigol.eu/Public/Uploads/uploadfile/files/ftp/%E6%96%B0%E8%B5%84%E6%96%99%E5%BA%93-%E5%90%AB%E6%89%8B%E5%86%8C%E5%9B%BA%E4%BB%B6%E8%BD%AF%E4%BB%B6/%E5%AE%98%E7%BD%91%E8%B5%84%E6%96%99/DS/%E6%89%8B%E5%86%8C/MSO8000/EN/MSO8000_UserGuide_EN.pdf#page=277",
            ["MSO5074"],
            ["*.bin"]   #TODO: Add Rigol *.wfm support
        )
