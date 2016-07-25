import time
import picamera


camera = picamera.PiCamera()

camera.start_preview()

time.sleep(5)

camera.stop_preview()


