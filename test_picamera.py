#from picamera import Picamera

#camera = PiCamera()
#camera.resolution = (640, 480)
#camera.start_recording('test_picamera.h264')
#camera.wait_recording(60)
#camera.stop_recording()

import time
from io import BytesIO
from picamera2 import Picamera2
#from picamera2.encoders import H264Encoder, MJPEGEncoder

stream = BytesIO()
camera = Picamera2()
camera.resolution(640, 480)
camera.start_recording(stream, format='mp4', quality=23)
#video_config = picam2.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"},
#                                                 lores={"size": (640, 480), "format": "YUV420"})

#picam2.configure(video_config)

#encoder1 = H264Encoder(10000000)
#encoder2 = MJPEGEncoder(10000000)

# picam2.start_recording('test1.mp4')
#picam2.start_recording(encoder2, 'test2.mjpeg', name="lores")
#time.sleep(10)
camera.wait_recording(15)
camera.stop_recording()
