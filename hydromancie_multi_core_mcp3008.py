import os
import time
import wave
import numpy as np
from scipy.io.wavfile import write
import struct
import mcp3008
import multiprocessing as mp 
import threading

# DEFINE WAVFILE PARAMETERS
NUM_CHANNELS = 1
SAMPLE_WIDTH_BYTES = 2
SAMPLE_RATE = 16000
DURATION = 5
FILE_NAME = "#C2W_16000_FRAMETEST_perf__scipy_mcp_audio"
WAVE_OUTPUT_FILENAME = FILE_NAME + ".wav"
MP3_OUTPUT_FILENAME = FILE_NAME + ".mp3"


# Initialize SPI bus and the ADC - MCP3008 ADC 
adc = mcp3008.MCP3008()
# adc.read([mcp3008.CH0/6/7])

print(f"Recording for {DURATION} seconds at {SAMPLE_RATE} Hz...")
FRAMES = int(SAMPLE_RATE * DURATION)
max_amplitude = (2**15 - 1)
num_samples = int(SAMPLE_RATE * DURATION)
frames = []


def do_the_right_thing(seconds, interval=1.0):
    start_time = time.perf_counter()
    for i in range(int(seconds / interval)):
    # for i in range(num_samples):
        next_tick = start_time + (i +1) * interval
        # do_the_right_thing
        raw_value = adc.read([mcp3008.CH7])
        frames.append((raw_value[0] / 1023) * max_amplitude)
        # Sleep until the next tick
        sleep_time = next_tick - time.perf_counter()
        if sleep_time > 0:
            time.sleep(sleep_time)

# HYDROMANIC MAIN ENTRY 
if __name__ == "__main__":




    print("TIME INTERVAL: ", 1 / SAMPLE_RATE)
    do_the_right_thing(DURATION, (1 / SAMPLE_RATE))

    print("Recording stopped. Frame len(", len(frames))

    # Convert the list of samples to a numpy array of int16 type
    # The wave module expects data in a specific format
    # audio_data = np.array(np.clip(frames, -32768, 32767),dtype=np.int16)
    audio_data = np.array(frames, dtype=np.int16)

    # SCIPY WAVE FILE WRITER
    write(WAVE_OUTPUT_FILENAME, SAMPLE_RATE, audio_data)


# Save the recorded data as a WAV file
#with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
#    wf.setnchannels(NUM_CHANNELS)
#    wf.setsampwidth(SAMPLE_WIDTH_BYTES)
#    wf.setframerate(SAMPLE_RATE)
#    wf.setnframes(FRAMES)
#    wf.writeframes(b''.join(audio_data)) # (frames.tobytes())
#    wf.close()

    print(f"File '{WAVE_OUTPUT_FILENAME}' created successfully.")

