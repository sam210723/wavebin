from typing import NamedTuple

class FileHeader(NamedTuple):
    """
    File header struct
    """

    sig_a:          str     # File signature byte 1 (A)
    sig_g:          str     # File signature byte 2 (G)
    v_maj:          str     # File version byte 1 (major)
    v_min:          str     # File version byte 2 (minor)
    size:           int     # File size (bytes)
    waveforms:      int     # Number of waveforms


class WaveHeader(NamedTuple):
    """
    Waveform header struct
    """

    size:           int     # Header size
    wave_type:      int     # Waveform type (see enums.WaveType)
    buffers:        int     # Number of waveform buffers
    points:         int     # Number of waveform points
    count:          int     # Averaging count (normally 0)
    x_d_range:      float   # Display range (duration)
    x_d_origin:     float   # Display origin (left edge)
    x_increment:    float   # Time between waveform points
    x_origin:       float   # X value of first waveform point
    x_units:        int     # X axis measurement units (see enums.Units)
    y_units:        int     # Y axis measurement units (see enums.Units)
    data:           str     # Acquisition date (zero on InfiniiVision scopes)
    time:           str     # Acquisition timestamp (zero on InfiniiVision scopes)
    label:          str     # Waveform label
    time_tags:      float   # Time since first trigger (seconds, requires segmented memory)
    segment:        int     # Segment number (requires segmented memory)
