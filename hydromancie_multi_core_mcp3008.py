import os
import time
import wave
import numpy as np
from scipy.io.wavfile import write
import struct
import mcp3008
import multiprocessing as mp 
# import threading


# Initialize SPI bus and the ADC - MCP3008 ADC 
adc = mcp3008.MCP3008()
# adc.read([mcp3008.CH0/6/7])


# DEFINE WAVFILE PARAMETERS
NUM_CHANNELS = 1
SAMPLE_WIDTH_BYTES = 2
SAMPLE_RATE = 11025
DURATION = 5
FRAMES = int(SAMPLE_RATE * DURATION)
MAX_AMPLITUDE = (2**15 - 1)

# FILE OUTPUT 
FILE_NAME = "#C2W_" + str(SAMPLE_RATE) + "_FRAMETEST_perf__scipy_mcp_audio"
WAVE_OUTPUT_FILENAME = FILE_NAME + ".wav"
MP3_OUTPUT_FILENAME = FILE_NAME + ".mp3"

# MCP3008 ADC DATA
frames = []


def do_the_right_thing(seconds, interval=1.0):
    start_time = time.perf_counter()
    #interval = 1 / SAMPLE_RATE
    #for i in range(int(seconds / interval)):
    for i in range(FRAMES):
        next_tick = start_time + (i +1) * interval
        # do_the_right_thing
        raw_value = adc.read([mcp3008.CH7])
        frames.append((raw_value[0] / 1023) * MAX_AMPLITUDE)
        # Sleep until the next tick
        sleep_time = next_tick - time.perf_counter()
        if sleep_time > 0:
            time.sleep(sleep_time)


# HYDROMANIC MAIN ENTRY 
if __name__ == "__main__":

    print(f"Recording for {DURATION} seconds at {SAMPLE_RATE} Hz...")

    print(mp.cpu_count())
    #with mp.Pool(processes=4) as pool:
        #pool.map(do_the_right_thing, (1 // SAMPLE_RATE))
    # with ProcessPoolExecutor(max_workers=mp.cpu_count) as executor:
        # executor.map(do_the_right_thing, (1 / SAMPLE_RATE))
    #for _ in range(mp.cpu_count()):
        #mp.Process(target=do_the_right_thing, args=(DURATION,1/SAMPLE_RATE,)).start()

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

