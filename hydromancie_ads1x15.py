# ADS1x15 ADC 
import time
import board
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

# Create the I2C bus
i2c = board.I2C()
ads = ADS1115(i2c)

# Note that setting gain will affect the raw ADC value but not the voltage.
ads.gain = 2 # {2/3, 1, 2, 4, 8, 16}
ads.mode = ads1x15.Mode.CONTINUOUS # Mode.SINGLE
# >>> ads.gain
# 1
# >>> chan.value, chan.voltage
# (84, 0.168082)
# >>> ads.gain = 16
# >>> ads.gain
# 16
# >>> chan.value, chan.voltage
# (1335, 0.167081)
# >>> 


# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
chan_1 = AnalogIn(ads, ads1x15.Pin.A2) # MAX9814
chan_2 = AnalogIn(ads, ads1x15.Pin.A3) # MAX4466

# Create differential input between channel 0 and 1
# diff_chan_1_2 = AnalogIn(ads, ads1x15.Pin.A0, ads1x15.Pin.A1)

print("{:>5}\t{:>5}".format("raw", "v"))

while True:
    print(f"MAX9814 {chan_1.value:>5}\t{chan_1.voltage:>5.3f}")
    print(f"MAX4466 {chan_2.value:>5}\t{chan_2.voltage:>5.3f}")
    time.sleep(0.005)
