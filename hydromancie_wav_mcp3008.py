import time
import wave
import numpy as np
import struct
import mcp3008
#import spidev
#hydromancie = spidev.SpiDev()
#hydromancie.open(0,0)
#print(hydromancie.max_speed_hz)
#hydromancie.max_speed_hz = 1350000
#from pydub import AudioSegment


# DEFINE WAVFILE PARAMETERS
NUM_CHANNELS = 1
SAMPLE_WIDTH_BYTES = 2
SAMPLE_RATE = 8192
DURATION = 5
FILE_NAME = "#8192_mcp_audio"
WAVE_OUTPUT_FILENAME = FILE_NAME + ".wav"
MP3_OUTPUT_FILENAME = FILE_NAME + ".mp3"


# Initialize SPI bus and the ADC - MCP3008 ADC 
adc = mcp3008.MCP3008()
# adc.read([mcp3008.CH0/6/7])

print(f"Recording for {DURATION} seconds at {SAMPLE_RATE} Hz...")
FRAMES = int(SAMPLE_RATE * DURATION)*2
max_amplitude = 32767

frames = []
for f in range(int(SAMPLE_RATE * DURATION)):
    raw_value = adc.read([mcp3008.CH7])
    # print(raw_value[0])
    frames.append(raw_value[0])

#start_time = time.time()
#while (time.time() - start_time) < DURATION:
    # Read the raw 10-bit value (0-1023) and convert to a 16-bit integer for better WAV quality
    # The MCP3008 is 10-bit, so this conversion might need adjustment based on your specific ADC
    #raw_value = adc.read([mcp3008.CH7]) # chan.value
    # print(raw_value[0])
    # Convert 10-bit (0-1023) to 16-bit (0-65535)
    #audio_value = int(raw_value[0] * 32) 
    # print(audio_value)
    # Append the sample data as bytes
    #frames.append(audio_value) #(audio_value) 

print("Recording stopped. Frame len(", len(frames))

# Convert the list of samples to a numpy array of int16 type
# The wave module expects data in a specific format
#audio_data = np.array(np.clip(frames, -32768, 32767),dtype=np.int16)
audio_data = np.array(frames, dtype=np.int16)

# Save the recorded data as a WAV file
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(NUM_CHANNELS)
    wf.setsampwidth(SAMPLE_WIDTH_BYTES)
    wf.setframerate(SAMPLE_RATE)
    wf.setnframes(FRAMES)
    wf.writeframes(b''.join(audio_data)) # (frames.tobytes())
    wf.close()

print(f"File '{WAVE_OUTPUT_FILENAME}' created successfully.")

#audio = AudioSegment.from_file(WAVE_OUTPUT_FILENAME, format="wav")
#audio.export(MP3_OUTPUT_FILENAME, format="mp3")

#while True:
#    print(f"MAX9814 {chan_1.value:>5}\t{chan_1.voltage:>5.3f}")
#    print(f"MAX4466 {chan_2.value:>5}\t{chan_2.voltage:>5.3f}")
#    time.sleep(0.005)
