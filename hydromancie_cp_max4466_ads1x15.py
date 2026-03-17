# ADS1x15 ADC 
import time
import board
import wave
import numpy as np
# import adafruit_mcp3xxx.mcp3008 as MCP
# from adafruit_mcp3xxx.analog_in import AnalogIn
import busio
import digitalio
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

# Configuration
SAMPLE_RATE = 44100 # Samples per second (Hz)
RECORD_SECONDS = 10  # Recording duration in seconds
WAVE_OUTPUT_FILENAME = "1_recorded_audio.wav"
NUM_CHANNELS = 1    # Mono recording
SAMPLE_WIDTH = 2    # 2 bytes for 16-bit audio (numpy 'int16')

# Create the I2C bus and the ADC - ADS1x15 ADC
i2c = board.I2C()
ads = ADS1115(i2c)

# Initialize SPI bus and the ADC - MCP3008 ADC 
#spi = busio.SPI(clock=digitalio.Pin.board.SCK, MISO=digitalio.Pin.board.MISO, MOSI=digitalio.Pin.board.MOSI)
#cs = digitalio.Pin.board.D8  # Chip select pin (GPIO 8)
#mcp = MCP.MCP3008(spi, cs)
#chan = AnalogIn(mcp, MCP.P0) # Read from channel 0

# Note that setting gain will affect the raw ADC value but not the voltage.
ads.gain = 1 # {2/3, 1, 2, 4, 8, 16}
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
# chan_1 = AnalogIn(ads, ads1x15.Pin.A1) # MAX9814
chan = AnalogIn(ads, ads1x15.Pin.A2) # MAX4466

# Create differential input between channel 0 and 1
# diff_chan_1_2 = AnalogIn(ads, ads1x15.Pin.A0, ads1x15.Pin.A1)

# print("{:>5}\t{:>5}".format("raw", "v"))

print(f"Recording for {RECORD_SECONDS} seconds at {SAMPLE_RATE} Hz...")

frames = []
start_time = time.time()

while (time.time() - start_time) < RECORD_SECONDS:
    # Read the raw 10-bit value (0-1023) and convert to a 16-bit integer for better WAV quality
    # The MCP3008 is 10-bit, so this conversion might need adjustment based on your specific ADC
    raw_value = chan.value
    print(chan.value)
    # Convert 10-bit (0-1023) to 16-bit (0-65535)
    # audio_value = int(raw_value * 64) 
    # Append the sample data as bytes
    frames.append(raw_value) #(audio_value) 

print("Recording stopped.")

# Convert the list of samples to a numpy array of int16 type
# The wave module expects data in a specific format
audio_data = np.array(frames, dtype=np.int16)

# Save the recorded data as a WAV file
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(NUM_CHANNELS)
    wf.setsampwidth(SAMPLE_WIDTH)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(audio_data.tobytes())

print(f"File '{WAVE_OUTPUT_FILENAME}' created successfully.")

#while True:
#    print(f"MAX9814 {chan_1.value:>5}\t{chan_1.voltage:>5.3f}")
#    print(f"MAX4466 {chan_2.value:>5}\t{chan_2.voltage:>5.3f}")
#    time.sleep(0.005)
