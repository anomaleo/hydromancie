import os
import time
import wave
import numpy as np
# from scipy.io.wavfile import write
# import struct
import mcp3008
# import wavio
# import multiprocessing as mp 
import threading
from pydub import AudioSegment
import audioop

# Initialize SPI bus and the ADC - MCP3008 ADC 
adc = mcp3008.MCP3008()
# adc.read([mcp3008.CH0/6/7])


# DEFINE WAVFILE PARAMETERS
NUM_CHANNELS = 1
SAMPLE_WIDTH = 2
SAMPLE_RATE = int(44100)
DURATION = 5
FRAMES = int(SAMPLE_RATE * DURATION)
MAX_AMPLITUDE = (2**15 - 1)

# FILE OUTPUT 
FILE_NAME = "#C2W_" + str(SAMPLE_RATE) + "_FRAMETEST_perf__scipy_mcp_audio"
WAVE_OUTPUT_FILENAME = FILE_NAME + ".wav"
MP3_OUTPUT_FILENAME = FILE_NAME + ".mp3"

# MCP3008 ADC DATA
frames = []


def do_the_right_thing(): #(seconds=DURATION, interval=(1/SAMPLE_RATE)):
    seconds = DURATION
    interval = (1 / SAMPLE_RATE)
    start_time = time.perf_counter()

    for i in range(int(seconds / interval )):
    #for i in range(FRAMES):
        next_tick = start_time + (i +1) * interval
        # do_the_right_thing
        raw_value = adc.read([mcp3008.CH7])
        frames.append((raw_value[0] / 1023) * MAX_AMPLITUDE)
#        time.sleep(1/SAMPLE_RATE)
        # Sleep until the next tick
        sleep_time = next_tick - time.perf_counter()
        if sleep_time > 0:
            time.sleep(sleep_time)
    print(f"Number of Samples (Frames): {len(frames)}")


def do_it(t, inter):
    start_time = time.time()
    while(time.time() - start_time) < t: 
        raw_value = adc.read([mcp3008.CH7])
        frames.append((raw_value[0] / 1023) * MAX_AMPLITUDE)
        time.sleep(inter)


def done_the_right_thing():
    # Convert the list of samples to a numpy array of int16 type
    # The wave module expects data in a specific format
    # audio_data = np.array(np.clip(frames, -32768, 32767),dtype=np.int16)
    audio_data = np.array(frames, dtype=np.int16)

    # SCIPY WAVE FILE WRITER
    # write(WAVE_OUTPUT_FILENAME, SAMPLE_RATE, audio_data)

    # Save the recorded data as a WAV file
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(NUM_CHANNELS)
        wf.setsampwidth(SAMPLE_WIDTH)
        wf.setframerate(SAMPLE_RATE)
        wf.setnframes(FRAMES)
        wf.writeframes(b''.join(audio_data)) # (frames.tobytes())
        wf.close()

    print(f"AUDIO-FILE '{WAVE_OUTPUT_FILENAME}' CREATED SUCCESSFULLY!")


# HYDROMANIC MAIN ENTRY 
if __name__ == "__main__":

    print(f"INIT AUDIO SAMPLING THREAD: {DURATION} Seconds @ {SAMPLE_RATE} Hz.")
    sample = threading.Thread(target=do_the_right_thing)
    sample.start()

    # try:
    print(f"MAIN THREAD YIELDS FOR {DURATION} Seconds")
    busy_wait = time.time()
    sample.join()

    print(f"MAIN THREAD WAIT: {time.time() - busy_wait} Seconds")
    print("SAMPLING COMPLETE: AUDIO THREAD JOIN")
    save = threading.Thread(target=done_the_right_thing)
    save.start()

    print(f"MAIN THREAD YIELDS FOR AUDIO-FILE CREATION")
    busy_wait = time.time()
    save.join()

    print(f"MAIN THREAD WAIT: {time.time() - busy_wait} Seconds")

    if 22050 < SAMPLE_RATE >= 16000:
        print(f"AUDIO_FILE FRAMERATE CORRECTION FOR {SAMPLE_RATE} RECORDINGS")
        sound = AudioSegment.from_file(WAVE_OUTPUT_FILENAME)
        
        # OVERRIDE AUDIO-FILE FRAMERATE
        csound = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * 0.8) # factor
        })

        csound = csound.set_frame_rate(SAMPLE_RATE)
        csound.export("cs"+WAVE_OUTPUT_FILENAME, format="wav")
    
    elif 44100 < SAMPLE_RATE >= 22050:
        print(f"AUDIO_FILE FRAMERATE CORRECTION FOR {SAMPLE_RATE} RECORDINGS")
        sound = AudioSegment.from_file(WAVE_OUTPUT_FILENAME)
        
        # OVERRIDE AUDIO-FILE FRAMERATE
        csound = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * 0.4) # factor
        })

        csound = csound.set_frame_rate(SAMPLE_RATE)
        csound.export("cs"+WAVE_OUTPUT_FILENAME, format="wav")

    else:
        print("EXIT")
        exit()
