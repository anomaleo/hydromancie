import wave
import math
import struct

# Parameters
sample_rate = 44100.0
duration = 1.0  # seconds
frequency = 440.0
volume = 0.5
num_samples = int(sample_rate * duration)

# Generate raw sample data
raw_samples = []
for i in range(num_samples):
    sample = volume * math.sin(2. * math.pi * frequency * i / sample_rate)
    # Convert to 16-bit integer format and pack into bytes
    int_sample = int(sample * (2**15 - 1))
    raw_samples.append(struct.pack('<h', int_sample)) # '<h' for little-endian short

# Write to WAV file
with wave.open("sine_wave_pure_python.wav", "wb") as wf:
    wf.setnchannels(1)  # Mono
    wf.setsampwidth(2)  # 2 bytes per sample (16-bit)
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(raw_samples))
