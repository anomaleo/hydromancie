# https://gist.github.com/jhauret/8a6e42bc4f03f9d95b604478796d96ba
import os
import sys
import time
import queue
import threading
import numpy  # Make sure NumPy is loaded before it is used in the callback
import soundfile as sf
import sounddevice as sd
import argparse
# sd.default.samplerate = 16000
sd.default.channels = 1
sd.default.dtype = 'int16'
print(sd.default.dtype)
# print(sd.default.samplerate) 
# print(sd.default.channels)
assert numpy  # avoid "imported but unused" message (W0611)

# ARG-PARSER: IDENTITY RECORDING LOCATION  
parser = argparse.ArgumentParser(description="Hydromancie audio recording")
parser.add_argument("location", help="python hydromancie_usb_recorder.py _identified_location_")
args = parser.parse_args()
LOCATION = args.location
print(f"Example Filename: usb-recorder-{LOCATION}0.wav")


# FOR ALL RECORDERS: MAIN USB-C AUDIO INTERFACE THREAD
class Recorder:
    """
    Non-blocking and Multi-channel compatible audio recorder
    
    inspired from :
    https://github.com/spatialaudio/python-sounddevice/blob/0.4.5/examples/rec_unlimited.py
    """

    def __init__(self, samplerate, channels, device):

        # audio parameters
        self.samplerate = samplerate
        self.channels = channels
        self.device = device

        # private attributes
        self._queue = queue.Queue()
        self._recording = False
        self._thread = None


    def start_stream(self, filename):
        """Start recording audio stream in 'filename'.wav"""
        filename = f'{filename}.wav'

        if os.path.exists(filename):
            os.remove(filename)

        def record_stream():
            # record from the default input audio
            with sf.SoundFile(filename, mode='x', samplerate=self.samplerate, channels=self.channels, subtype=None) as file:
                with sd.InputStream(samplerate=self.samplerate, device=self.device, channels=self.channels, callback=self._fill_queue):
                    while self._recording:
                        file.write(self._queue.get())

        self._recording = True
        self._thread = threading.Thread(target=record_stream, daemon=False)
        self._thread.start()


    def _fill_queue(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self._queue.put(indata.copy())


    def stop_stream(self):
        """Stop recording audio stream"""
        self._recording = False
        if self._thread is not None:
            self._thread.join()


# FOR ALL RECORDERS: MAIN ENTRY POINT FOR USB-C RECORDERS
if __name__ == '__main__':
    # QUERY FOR ALL AUDIO DEVICES {AUDIO-IN, AUDIO-OUT}
    devices = sd.query_devices()
    print(devices)
    print(len(devices))

    # FOR ALL RECORDERS: IDENTIFY ALL USB-C AUDIO INTERFACES 
    recorders = []
    for d in devices:
        if "USB Audio Device".lower() in d["name"].lower():
            recorders.append(Recorder(samplerate=44100, channels=1, device=d["index"]))
    print(recorders)            

    # FOR ALL RECORDERS: LOCATION IDENTIFICATION, UNIQUE FILENAMES
    cnt = 0
    for r in recorders:
        fname = "usb-recorder-" + LOCATION + str(cnt)
        r.start_stream(fname)
        cnt += 1

    # FOR ALL RECORDERS: GLOBAL RECORDING PERIOD
    time.sleep(15.0) 

    # FOR ALL RECORDERS: STOP STREAMS AND SAVE FILES
    for r in recorders:
        r.stop_stream()
