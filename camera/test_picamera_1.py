import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import PyavOutput
picam2 = Picamera2()
config = picam2.create_video_configuration({'size': (640, 480), 'format': 'YUV420'})
picam2.configure(config)
time.sleep(2)
encoder = H264Encoder(bitrate=1000000) # 1 MBP = 1000000 | 10 MBPS = 10 000 000
picam2.start()
time.sleep(2)
# encoder.audio = True
output = PyavOutput("anomaleo2.mp4")
picam2.start_recording(encoder, "anomaleo.h264")
time.sleep(10)
picam2.stop_recording()
