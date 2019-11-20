from enum import Enum

class WaveType(Enum):
    """
    Waveform types
    """

    UNKNOWN     = 0
    Normal      = 1
    Peak        = 2
    Average     = 3
    Logic       = 6


class Units(Enum):
    """
    Unit types
    """

    UNKNOWN     = 0
    Volts       = 1
    Seconds     = 2
    Constant    = 3
    Amps        = 4
    Decibels    = 5
    Hertz       = 6


class DataType(Enum):
    """
    Data types
    """

    UNKNOWN     = 0
    float32     = 1
    floatMax    = 2
    floatMin    = 3
    uchar8      = 6
