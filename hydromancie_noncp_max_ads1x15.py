import os
import time
import ADS1x15
import wave
import numpy as np

SAMPLE_RATE = 1024 # Samples per second (Hz)
RECORD_SECONDS = 10  # Recording duration in seconds
WAVE_OUTPUT_FILENAME = "#5_noncp_recorded_audio.wav"
NUM_CHANNELS = 1    # Mono recording
SAMPLE_WIDTH = 2    # 2 bytes for 16-bit audio (numpy 'int16')


#ADS = ADS1x15.ADS1015(1, 0x48)
ADS = ADS1x15.ADS1115(1, 0x48)
print(os.path.basename(__file__))
print("ADS1X15_LIB_VERSION: {}".format(ADS1x15.__version__))

ADS.setGain(ADS.PGA_4_096V)
ADS.setDataRate(ADS.DR_ADS111X_860)
ADS.setMode(ADS.MODE_CONTINUOUS)
ADS.requestADC(3) 

print(f"Recording for {RECORD_SECONDS} seconds at {SAMPLE_RATE} Hz...")

frames = []
start_time = time.time()

while (time.time() - start_time) < RECORD_SECONDS:
    # Read the raw 10-bit value (0-1023) and convert to a 16-bit integer for better WAV quality
    # The MCP3008 is 10-bit, so this conversion might need adjustment based on your specific ADC
    raw_value = ADS.getValue() # chan.value
    # print(chan.value)
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
#while True :
#    raw = ADS.getValue()
#    print("{0:.3f} V".format(raw)) #(ADS.toVoltage(raw)))
#    time.sleep(0.01)
