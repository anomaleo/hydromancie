# RPI-ZERO-2W - PICAMERA
import time
import threading
import board
import digitalio
# ACCESS FILE SYSTEM
import os
# print(os.getcwd())

from picamera2 import Picamera2
from libcamera import Transform
from picamera2.encoders import H264Encoder
# from picamera2.encoders import JpegEncoder
# from picamera2.outputs import PyavOutput

picam2 = Picamera2()
video_config = picam2.create_video_configuration({"format": "YUV420", "size": (640, 480)}, transform=Transform(hflip=True, vflip=True))
picam2.configure(video_config)
# encoder = JpegEncoder(q=73)
encoder = H264Encoder(bitrate=25000000) # 1 MBP = 1000000 | 25 MBPS = 25 000 000
picam2.start()

# ARG-PARSER: IDENTITY RECORDING LOCATION  
parser = argparse.ArgumentParser(description="Hydromancie video recording")
parser.add_argument("record_time", help="python hydromancie_zero_time.py _video_time_")
args = parser.parse_args()
VIDEO_TIME = args.record_time
print(f"Example VIDEO-TIME: {VIDEO_TIME}")

# PREFIX_FILE
PREFIX_FILE = "hydromancie_prefix.txt"

# STATUS RGB LED
r = digitalio.DigitalInOut(board.D17)
r.direction = digitalio.Direction.OUTPUT
g = digitalio.DigitalInOut(board.D27)
g.direction = digitalio.Direction.OUTPUT
b = digitalio.DigitalInOut(board.D22)
b.direction = digitalio.Direction.OUTPUT
# RASPI GND PIN 9 | 14
# STATUS LEDS OFF
r.value = g.value = b.value = 0

# SHARED ACTIVATE SIGNAL - ARDUINO RPI
we_are_go = digitalio.DigitalInOut(board.D18)
we_are_go.direction = digitalio.Direction.INPUT
we_are_go.pull = digitalio.Pull.UP

# ACTIVATE CONTROL VARIABLE
activate = 0 # we are a go ...
_prefix = -1 # RECORD FILE PREFIX NUMBER 


def debug_status(led, flash, t):
    for _ in range(flash):
        led.value = not led.value
        time.sleep(t)


def get_file_prefix():
    _data = None
    try:
        if os.path.isfile(PREFIX_FILE):
            with open(PREFIX_FILE, "r", encoding="utf-8") as f:
                _data = int(f.read())
    except FileNotFoundError:
        print(f"The file {PREFIX_FILE} was not found")
    finally:
        return _data


def set_file_prefix(pre):
    try:
        if os.path.isfile(PREFIX_FILE):
            with open(PREFIX_FILE,"w", encoding="utf-8") as f:
                pre += 1
                f.write(f"{pre}")
    except FileNotFoundError:
        print(f"The file {PREFIX_FILE} was not found")
    finally:
        return True
    

if __name__ == '__main__':

    # FIRST: RETRIEVE LATEST PREFIX
    _prefix = get_file_prefix()
    if _prefix is None:
        print(f"ERROR: CHECK PREFIX_FILE!")
        while True:
            debug_status(b, 2, 0.1)

    # START, SETUP CAMERA RECORDING SESSION...
    global _namer
    _namer = f"hydromancie_{_prefix}.h264"
            
    time.sleep(1)
    print("Recording started...")
    debug_status(r, 1, 1.0)
    picam2.start_recording(encoder, _namer)
    # picam2.wait_recording(VIDEO_TIME)
    time.sleep(VIDEO_TIME)
    picam2.stop_recording()
    debug_status(r, 1, 1.0)
    print("Recording stopped.")
    # CLEAN-UP CAMERA RECORDING SESSION...
    time.sleep(1)

    # NEXT: SAVE RECORDING, UPDATE PREFIX_FILE & REINIT RECORDING (activate = 1)
    _status = set_file_prefix(_prefix)
    if _status is None:
        print(f"ERROR: CHECK PREFIX_FILE!")
        while True:
            debug_status(b, 2, 0.1)