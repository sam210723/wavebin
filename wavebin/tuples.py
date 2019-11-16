from typing import NamedTuple

class FileHeader(NamedTuple):
    """
    File header struct
    """

    sig_a:       str
    sig_g:       str
    version:     int
    size:        int
    waveforms:   int
