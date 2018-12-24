import threading
from time import sleep


class FrameGetterWorker(threading.Thread):
    def __init__(self, frames_queue, capture):
        threading.Thread.__init__(self)
        self.frames_queue = frames_queue
        self.capture = capture
        self.daemon = True
        self.run_thread = True

    def run(self):
        self.get_frames()

    def get_frames(self):

        while not self.capture.isOpened():
            pass

        while self.run_thread:

            grabbed, frame_original = self.capture.read()

            if grabbed:
                self.frames_queue.put(frame_original)
                sleep(0.001)
