# RPI-ZERO-2W 
import time
import board
import digitalio
# ACCESS FILE SYSTEM
import os
print(os.getcwd())

# PREFIX_FILE
PREFIX_FILE = "hydromancie_prefix.txt"

led = digitalio.DigitalInOut(board.D18)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

#while True:
#    led.value = not button.value # light when button is pressed!

def get_file_prefix():
    _data = None
    try:
        if os.path.isfile(PREFIX_FILE):
            with open(PREFIX_FILE, "r", encoding="utf-8") as f:
                _data = int(f.read())
#                f.close()
    except FileNotFoundError:
        print(f"The file {PREFIX_FILE} was not found")
    finally:
        return _data


def set_file_prefix(pre):

    try:
        if os.path.isfile(PREFIX_FILE):
            # os.remove(PREFIX_FILE)
            # time.sleep(1)
            #_p = open(PREFIX_FILE,"w", encoding="utf-8")
            #pre += 1
            #print("pre", pre)
            #_p.write(f"{pre}")
            with open(PREFIX_FILE,"w", encoding="utf-8") as f:
                print("file open for writing")
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

    #if set_file_prefix(_prefix) != _prefix:
     #   print("File Prefix Update")
