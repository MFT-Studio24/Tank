import time
import threading
import cv2
import imutils

class Camera(threading.Thread):
    def __init__(self):
        super(Camera, self).__init__()

        self.frame_width = 320
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def run(self):
        while True:
            (ret, frame) = self.video.read()
            (ret, jpeg) = cv2.imencode('.jpg', frame)
            self.jpeg = jpeg.tobytes()
