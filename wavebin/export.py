"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

import wave
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

        # Write waveform data
        self.write_data()

        # Close completed ZIP file
        self.zipf.close()
        self.log("Finished exporting")


    def metadata(self):
        meta =   "[global]\r\n"
        meta +=  "sigrok version=0.5.2\r\n"
        meta +=  "\r\n"

        meta +=  "[device 1]\r\n"
        meta +=  "capturefile=logic-1\r\n"
        meta += f"total probes={len(self.waveforms)}\r\n"
        meta += f"samplerate={self.get_sample_rate() / 1e6} MHz\r\n"
        meta +=  "total analog=0\r\n"       #TODO: Use 'clipped' flag to export analog waveforms
        
        for i in range(len(self.waveforms)):
            meta +=  f"probe{i + 1}=D{i}\r\n"

        meta +=  "unitsize=1"
        meta +=  "\r\n"

        return meta


    def write_data(self):
        for i, w in enumerate(self.waveforms):
            arr = bytearray(b'')
            
            for p in w['data']:
                if p == 1:
                    arr.append(0xFF)
                elif p == -1:
                    arr.append(0xFE)

            self.zipf.writestr(f"logic-1-{i + 1}", bytes(arr))


    def get_sample_rate(self):
        # Check if waveform is subsampled
        if self.waveforms[0]['header'].points != len(self.waveforms[0]['data']):
            # Calculate new sample increment value
            dur = self.waveforms[0]['header'].x_increment * self.waveforms[0]['header'].points
            inc = dur / len(self.waveforms[0]['data'])
            sr = 1 / inc
        else:
            # Use increment value from waveform header
            sr  = 1 / self.waveforms[0]['header'].x_increment
        
        return sr


    def log(self, msg):
        if self.verbose: print(msg)


class WaveFile():
    def __init__(self, verbose, path, waveforms):
        self.verbose = verbose
        self.path = path
        self.waveforms = waveforms

        self.log(f"Exporting WAVE file to \"{self.path}\"")

        # Create WAV file
        self.wavf = wave.open(path, mode='wb')
        self.wavf.setnchannels(len(self.waveforms))             # Number of channels
        self.wavf.setsampwidth(2)                               # Bytes per sample
        self.wavf.setframerate(self.get_sample_rate())          # Sample rate
        self.wavf.setnframes(len(self.waveforms[0]['data']))    # Number of samples

        # Write samples to WAV
        for i, w in enumerate(self.waveforms):
            # Write samples to WAV file
            self.wavf.writeframesraw(
                w['data'].astype(numpy.float16)
            )

        # Close WAV file
        self.wavf.close()
        self.log("Finished exporting")
    
    
    def get_sample_rate(self):
        # Check if waveform is subsampled
        if self.waveforms[0]['header'].points != len(self.waveforms[0]['data']):
            # Calculate new sample increment value
            dur = self.waveforms[0]['header'].x_increment * self.waveforms[0]['header'].points
            inc = dur / len(self.waveforms[0]['data'])
            sr = 1 / inc
        else:
            # Use increment value from waveform header
            sr  = 1 / self.waveforms[0]['header'].x_increment
        
        return sr


    def log(self, msg):
        if self.verbose: print(msg)
