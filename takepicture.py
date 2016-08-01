import tempfile
import time

try:
    import picamera
except ImportError:
    pass


def get_file_name():
    f = tempfile.NamedTemporaryFile(mode='w+b', suffix='.jpg', dir='pictures')
    name = f.name
    f.close()
    return name

def countdown(camera):
    camera.annotate_text_size = 64
    for msg in ["Get Ready!", "5", "4", "3", "2", "1"]:
        camera.annotate_text = msg
        time.sleep(1)
    camera.annotate_text = ""

def take_picture():
    with picamera.PiCamera() as camera:
        file_name = get_file_name()
        camera.start_preview()
        countdown(camera)
        camera.capture(file_name)
        camera.stop_preview()
        
