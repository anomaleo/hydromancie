import sounddevice as sd
import soundfile as sf
import numpy as np

# Load a sound file as a NumPy array and get the sampling rate
# data, fs = sf.read('my_audio_file.wav', dtype='float32') #

# Play the audio data
#sd.play(data, fs) #

# Wait until the sound finishes playing
#sd.wait() #
devices = sd.query_devices()
print(devices)
print(len(devices))

recorders = []
for d in devices:
    if "USB Audio Device".lower() in d["name"].lower():
        recorders.append(d["index"])

#device = devices[d]
    #print(device)
    #if "USB Audio Device" in device:
    #    recorders.append(d)

print(recorders)

# Record audio (e.g., for 5 seconds at a specific sample rate)
#duration = 5  # seconds
#fs_rec = 44100  # sample rate
#print("Recording...")
#recording = sd.rec(int(duration * fs_rec), samplerate=fs_rec, channels=2, dtype='float32') #
#sd.wait()  # Wait until recording is finished
#print("Recording complete.")

# Save the recorded data to a WAV file
#sf.write('output_recording.wav', recording, fs_rec)
