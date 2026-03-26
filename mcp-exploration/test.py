import wave
import struct
import math

# Audio parameters
sample_rate = 44100.0 # frames per second
duration_seconds = 1
frequency = 440 # Hz
volume = 1.0 # Amplitude (0.0 to 1.0)
num_channels = 1 # mono
sample_width_bytes = 2 # 2 bytes = 16-bit audio

# Generate audio data (sine wave samples)
max_amplitude = (2**15 - 1) # Max value for 16-bit signed integer
num_samples = int(sample_rate * duration_seconds)
pcm_data = []
for i in range(num_samples):
    sample = volume * math.sin(2.0 * math.pi * frequency * i / sample_rate)
    # Scale and convert to 16-bit integer
    pcm_data.append(int(sample * max_amplitude))

# Write to WAV file
with wave.open('sine_wave.wav', 'wb') as wavfile:
    wavfile.setnchannels(num_channels)
    wavfile.setsampwidth(sample_width_bytes)
    wavfile.setframerate(sample_rate)
    # Pack the list of integers into a bytes object
    for sample in pcm_data:
        # '<h' specifies little-endian, signed short (2 bytes)
        wavfile.writeframes(struct.pack('<h', sample))
