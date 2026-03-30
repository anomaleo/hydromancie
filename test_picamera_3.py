import queue
import threading
from picamera2 import Picamera2
import time
import cv2
import numpy as np

# A queue to hold captured requests
q = queue.Queue()
event = threading.Event()

def camera_producer(picam):
    while True:
        request = picam.capture_request()
        if request is not None:
            q.put(request)
            event.set()

def processing_consumer():
    while True:
        event.wait() # Wait for a frame to be available
        try:
            request = q.get_nowait()
            # Process the image in this separate thread
            image = request.make_image("main") # Convert to numpy array
            # ... perform OpenCV or other processing on the 'image' ...
            cv2.imshow("Processed Image", image)
            cv2.waitKey(1)
            request.release() # Release the buffer back to the camera
            if q.empty():
                event.clear()
        except queue.Empty:
            pass # Continue loop if queue is empty after event

# Setup camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "XRGB888"})
picam2.configure(config)
picam2.start()

# Start threads
cam_thread = threading.Thread(target=camera_producer, args=(picam2,))
proc_thread = threading.Thread(target=processing_consumer)

cam_thread.start()
proc_thread.start()

# Main thread can continue with other tasks or simply wait
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    picam2.stop()

