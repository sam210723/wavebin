"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

from enum import Enum
import numpy as np
from pyqtgraph import PlotWidget
import pyqtgraph as pg


class QtPlot(PlotWidget):
    def __init__(self, config):
        self.config = config

        self.log("Initialising plot widget")
        super().__init__()

        # Enable/Disable OpenGL
        if self.config['opengl']:
            pg.setConfigOptions(useOpenGL=True)
            self.config['line_width'] = 2
        else:
            pg.setConfigOptions(useOpenGL=False)
            self.config['line_width'] = 1    # See https://github.com/pyqtgraph/pyqtgraph/issues/533

        # Set plot properties
        self.view = self.getViewBox()
        self.setAntialiasing(True)
        self.setLabel('bottom', "Time", units='s')
        self.showGrid(x=True, y=True, alpha=1.0)
        self.setMouseEnabled(x=True, y=False)


    def update(self):
        self.log("Updating plot")

        # Remove old traces
        self.clear()

        # Loop through waveforms and render traces
        for i, w in enumerate(self.waveforms):
            # Subsampling
            if self.config['subsampling'] == -1 or self.config['subsampling'] == len(w['data']):
                y = w['data']
            else:
                self.log(f"Subsampling waveform ({len(w['data'])} -> {self.config['subsampling']} points)")
                y = w['data'][:: int( len(w['data']) / self.config['subsampling'] )]

            # Generate X points
            start = w['header'].x_d_origin
            stop = w['header'].x_d_origin + w['header'].x_d_range
            x = np.linspace(start, stop, len(y))

            # Filtering
            if self.config['filter_type'] == 1:
                self.log(f"Filtering waveform {i + 1} (Savitzky-Golay)")
                
                # Calculate window length
                window = round(len(y) * 0.025)
                if window % 2 == 0: window += 1

                # Catch filter exceptions
                try:
                    # Applt filter
                    y = Filters().savitzky_golay(y, window, 3)
                except TypeError as e:
                    if str(e) == "window_size is too small for the polynomials order":
                        self.log("Not enough points to apply filter")
            
            
            # Clipping
            if self.config['clipping']:
                self.log(f"Clipping waveform {i + 1}")

                # Find waveform median
                med = (np.amax(y) - abs(np.amin(y))) / 2   # Waveform median

                # Shift waveform to be centered around zero
                y = (y - med) + 0

                # Apply threshold to waveform values
                y[y > 0] = 1
                y[y < 0] = -1
            

            # Render data on plot
            self.plot(
                x,
                y,
                pen=pg.mkPen(
                    self.config['colours'][i],
                    width=self.config['line_width']
                )
            )
        
        # Set left Y axis label
        self.setLabel(
            'left',
            Units(self.waveforms[0]['header'].y_units).name,
            units=UnitAbbr(self.waveforms[0]['header'].y_units).name
        )


    def log(self, msg):
        if self.config['verbose']: print(msg)


class Filters():
    def savitzky_golay(self, y, window_size, order, deriv=0, rate=1):
        """
        Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
        The Savitzky-Golay filter removes high frequency noise from data.
        It has the advantage of preserving the original shape and
        features of the signal better than other types of filtering
        approaches, such as moving averages techniques.
        Parameters
        ----------
        y : array_like, shape (N,)
            the values of the time history of the signal.
        window_size : int
            the length of the window. Must be an odd integer number.
        order : int
            the order of the polynomial used in the filtering.
            Must be less then `window_size` - 1.
        deriv: int
            the order of the derivative to compute (default = 0 means only smoothing)
        Returns
        -------
        ys : ndarray, shape (N)
            the smoothed signal (or it's n-th derivative).
        Notes
        -----
        The Savitzky-Golay is a type of low-pass filter, particularly
        suited for smoothing noisy data. The main idea behind this
        approach is to make for each point a least-square fit with a
        polynomial of high order over a odd-sized window centered at
        the point.
        Examples
        --------
        t = np.linspace(-4, 4, 500)
        y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
        ysg = savitzky_golay(y, window_size=31, order=4)
        import matplotlib.pyplot as plt
        plt.plot(t, y, label='Noisy signal')
        plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
        plt.plot(t, ysg, 'r', label='Filtered signal')
        plt.legend()
        plt.show()
        References
        ----------
        .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
        Data by Simplified Least Squares Procedures. Analytical
        Chemistry, 1964, 36 (8), pp 1627-1639.
        .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
        W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
        Cambridge University Press ISBN-13: 9780521880688
        """
        
        import numpy as np
        from math import factorial

        try:
            window_size = np.abs(np.int(window_size))
            order = np.abs(np.int(order))
        except ValueError:
            raise ValueError("window_size and order have to be of type int")

        if window_size % 2 != 1 or window_size < 1:
            raise TypeError("window_size size must be a positive odd number")

        if window_size < order + 2:
            raise TypeError("window_size is too small for the polynomials order")

        order_range = range(order+1)
        half_window = (window_size -1) // 2

        # Precompute coefficients
        b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
        m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
        
        # Pad the signal at the extremes with values taken from the signal itself
        firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
        lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
        
        y = np.concatenate((firstvals, y, lastvals))

        return np.convolve( m[::-1], y, mode='valid')


class Units(Enum):
    """
    Waveform units
    """

    UNKNOWN     = 0
    Volts       = 1
    Seconds     = 2
    Constant    = 3
    Amps        = 4
    Decibels    = 5
    Hertz       = 6


class UnitAbbr(Enum):
    """
    Waveform unit abbreviations
    """

    UNKNOWN     = 0
    V           = 1
    s           = 2
    C           = 3
    A           = 4
    dB          = 5
    Hz          = 6
