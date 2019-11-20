from enum import Enum

class WaveType(Enum):
    """
    Waveform types
    """

    UNKNOWN     = 0
    NORMAL      = 1
    PEAK_DETECT = 2
    AVERAGE     = 3
    LOGIC       = 6


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
    FLOAT32     = 1
    FLOATMAX    = 2
    FLOATMIN    = 3
    UCHAR8      = 6
