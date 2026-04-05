# RPI-ZERO-2W 
import time
import board
import digitalio
# ACCESS FILE SYSTEM
import os
print(os.getcwd())

# PREFIX_FILE
PREFIX_FILE = "hydromancie_prefix.txt"

# STATUS RGB LED
r = digitalio.DigitalInOut(board.D18)
r.direction = digitalio.Direction.OUTPUT
g = digitalio.DigitalInOut(board.D18)
g.direction = digitalio.Direction.OUTPUT
b = digitalio.DigitalInOut(board.D18)
b.direction = digitalio.Direction.OUTPUT

# SHARED ACTIVATE SIGNAL - ARDUINO RPI
activate = digitalio.DigitalInOut(board.D4)
activate.direction = digitalio.Direction.INPUT
activate.pull = digitalio.Pull.UP


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
    if _prefix is not None:
        print(_prefix)
    time.sleep(5)
    print(set_file_prefix(_prefix))

    #if set_file_prefix(_prefix):
     #   print("File Prefix Update")

    while True:
        led.value = not button.value # light when button is pressed!
