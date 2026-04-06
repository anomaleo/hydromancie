import time
import threading
from picamera2 import Picamera2
from libcamera import Transform
from picamera2.encoders import H264Encoder
# from picamera2.encoders import JpegEncoder
# from picamera2.outputs import PyavOutput


picam2 = Picamera2()
video_config = picam2.create_video_configuration({"format": "YUV420", "size": (640, 480)}, transform=Transform(hflip=True, vflip=True))
picam2.configure(video_config)
# encoder = JpegEncoder(q=73)
encoder = H264Encoder(bitrate=10000000) # 1 MBP = 1000000 | 10 MBPS = 10 000 000
picam2.start()

# Flag to stop the thread
recording = True

def record_video():
    # picam2.start_recording(encoder, 'test-again3.mjpeg')
    picam2.start_recording(encoder, 'test-again3.h264')
    
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
    