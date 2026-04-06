import time
import threading
from picamera2 import Picamera2
from libcamera import Transform
from picamera2.encoders import JpegEncoder

picam2 = Picamera2()
video_config = picam2.create_video_configuration({"format": "YUV420", "size": (1280, 1024)}, transform=Transform(hflip=True, vflip=True))
picam2.configure(video_config)
encoder = JpegEncoder(q=73)
picam2.start()

# Flag to stop the thread
recording = True

def record_video():
    """Function to be run in a separate thread"""
    picam2.start_recording(encoder, 'test-again2.mjpeg')
    
    print("Recording started...")
    time.sleep(10)
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
    