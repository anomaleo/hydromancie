# https://gist.github.com/jhauret/8a6e42bc4f03f9d95b604478796d96ba
import os
import sys
import time
import queue
import threading
import numpy  # Make sure NumPy is loaded before it is used in the callback
import soundfile as sf
import sounddevice as sd
sd.default.samplerate = 16000
sd.default.channels = 1
sd.default.dtype = 'int16'
print(sd.default.dtype)
print(sd.default.samplerate) 
print(sd.default.channels)
assert numpy  # avoid "imported but unused" message (W0611)


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

if __name__ == '__main__':
    devices = sd.query_devices()
    print(devices)
    print(len(devices))

    recorders = []
    for d in devices:
        if "USB Audio Device".lower() in d["name"].lower():
            #recorders.append(d["index"])
#            print(d.check_input_settings(d["index"]))
            recorders.append(Recorder(samplerate=44100, channels=1, device=d["index"]))
            # recorder.start_stream('usb-recorder'+d["index"])
    print(recorders)            
    cnt = 0
    for r in recorders:
        fname = "usb-recorder" + str(cnt)
        r.start_stream(fname)
        cnt += 1
    # recorder.start_stream('usb-recorder'+d["index"])
    # recorder = Recorder(samplerate=48_000, channels=1, device=1)
    #recorder.start_stream('demo-1')
    time.sleep(30.0) 
    for r in recorders:
        r.stop_stream()
    #recorder.stop_stream()
