"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

import zipfile


class PulseView():
    def __init__(self, verbose, path, waveforms, clipped):
        self.verbose = verbose
        self.path = path
        self.waveforms = waveforms
        self.clipped = clipped

        self.log(f"Exporting PulseView session to \"{self.path}\"")

        # Create ZIP file
        self.zipf = zipfile.ZipFile(self.path, 'w', zipfile.ZIP_DEFLATED)

        # Create version file
        self.zipf.writestr('version', '2'.encode('utf-8'))

        # Create metadata file
        meta = self.metadata()
        self.zipf.writestr('metadata', meta.encode('utf-8'))

        # Close completed ZIP file
        self.zipf.close()


    def metadata(self):
        num = len(self.waveforms)
        sr  = int(round(1 / self.waveforms[0]['header'].x_increment) / 1e6)

        meta =   "[global]\r\n"
        meta +=  "sigrok version=0.5.2\r\n"
        meta +=  "\r\n"

        meta +=  "[device 1]"
        meta +=  "capturefile=logic-1\r\n"
        meta += f"total probes={num}\r\n"
        meta += f"samplerate={sr} MHz\r\n"
        meta +=  "total analog=0\r\n"       #TODO: Use 'clipped' flag to export analog waveforms
        
        for i in range(num):
            meta +=  f"probe{i + 1}=D{i}\r\n"

        meta +=  "unitsize=1"
        meta +=  "\r\n"

        return meta


    def log(self, msg):
        if self.verbose: print(msg)
