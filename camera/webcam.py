import cv2

class Webcam:
    def __init__(self, index):
        self.cap = cv2.VideoCapture(index)
        if not self.cap.isOpened():
            raise RuntimeError("Webcam not accessible")

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to read webcam frame")
        return frame

    def release(self):
        self.cap.release()
