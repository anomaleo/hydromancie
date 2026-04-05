# RPI-ZERO-2W 
import time
import board
import digitalio
# ACCESS FILE SYSTEM
import os
# print(os.getcwd())

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
        print("bleeped")


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

    # ATTENDING GLOBAL ACTIVATION SIGNAL - EXTERNAL BUTTON SIGNAL
    if not we_are_go.value:
        time.sleep(0.375)
        if not activate:
            activate = 1
        else:
            print(f"We are go to go: access prefix_file, update filename and initiate record session")
            debug_status(g, 4, 0.127) # GREEN LED ON = RECORDING OFF
            activate = 0


    if activate:

        # FIRST: RETRIEVE LATEST PREFIX
        _prefix = get_file_prefix()
        if _prefix is None:
            print(f"ERROR: CHECK PREFIX_FILE!")
            while True:
                debug_status(b, 7, 0.067)
        else:
            print(f"We are go to go: access prefix_file, update filename and initiate record session")

        # START, SETUP CAMERA RECORDING SESSION...

        time.sleep(5)
        debug_status(r, 4, 0.127) # RED LED ON = RECORDING ON

        # CLEAN-UP CAMERA RECORDING SESSION...


        # NEXT: SAVE RECORDING, UPDATE PREFIX_FILE & REINIT RECORDING (activate = 1)
        _status = set_file_prefix(_prefix)
        if _status is None:
            print(f"ERROR: CHECK PREFIX_FILE!")
            while True:
                debug_status(b, 7, 0.067)
        else:
            print(f"We are go to go: access prefix_file, update filename and initiate record session")

        # 
        #if set_file_prefix(_prefix):
        #   print("File Prefix Update")

        #while True:
        #    led.value = not button.value # light when button is pressed!
