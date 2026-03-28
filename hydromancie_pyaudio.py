import pyaudio
import wave
import threading
import queue
import time

# --- Configuration ---
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024  # Frames per buffer
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "threaded_output.wav"

# Queue for inter-thread communication
audio_queue = queue.Queue()
# Event to signal when recording should stop
stop_recording_event = threading.Event()

def callback(in_data, frame_count, time_info, status):
    """This function is called continuously by the audio stream thread."""
    audio_queue.put(in_data)
    # If the stop event is set, stop the stream
    if stop_recording_event.is_set():
        return (in_data, pyaudio.paComplete)
    return (in_data, pyaudio.paContinue)

def record_audio_in_thread():
    """Manages the PyAudio stream in a separate thread."""
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index = device_id,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)

    print("--- Recording started in background thread. Press Ctrl+C to stop. ---")

    stream.start_stream()

    # Wait for the stop event to be set (e.g., via KeyboardInterrupt in the main thread)
    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("--- Recording stopped. ---")

def write_wav_file(filename, frames):
    """Writes the recorded frames to a WAV file."""
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"--- Audio saved to {filename} ---")

# --- Main execution ---
if __name__ == "__main__":
    recorded_frames = []
    
    # Start the audio recording thread
    audio_thread = threading.Thread(target=record_audio_in_thread)
    audio_thread.start()

    try:
        # The main thread can do other things or just wait
        print(f"Main thread waiting for {RECORD_SECONDS} seconds...")
        time.sleep(RECORD_SECONDS)
        print("Main thread done waiting. Signaling stop.")

    except KeyboardInterrupt:
        print("Keyboard interrupt received in main thread.")

    finally:
        # Signal the recording thread to stop
        stop_recording_event.set()
        # Wait for the recording thread to finish
        audio_thread.join()

        # Retrieve all recorded data from the queue
        while not audio_queue.empty():
            recorded_frames.append(audio_queue.get())
        
        # Save the collected data to a file
        if recorded_frames:
            write_wav_file(WAVE_OUTPUT_FILENAME, recorded_frames)
        else:
            print("No audio frames recorded.")
