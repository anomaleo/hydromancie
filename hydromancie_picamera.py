import threading
import time
from picamera2 import Picamera2

# Create the camera object
picam2 = Picamera2()
config = picam2.create_video_configuration()
picam2.configure(config)
picam2.start()

# Flag to stop the thread
recording = True

def record_video():
    """Function to be run in a separate thread"""
    picam2.start_recording("output.mp4")
    print("Recording started...")
    while recording:
        time.sleep(1) # Keep the thread alive
    picam2.stop_recording()
    print("Recording stopped.")

# Start the recording thread
record_thread = threading.Thread(target=record_video)
record_thread.start()

# --- Main Thread ---
try:
    print("Main thread running other tasks...")
    time.sleep(10) # Perform other tasks for 10 seconds
finally:
    # Stop the recording
    recording = False
    record_thread.join()
    picam2.stop()
