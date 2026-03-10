import cv2

class Webcam:
    def __init__(self, index):
        self.index = index
        self.cap = None
        self._open_capture()

    def _backend_candidates(self):
        # On Windows, DSHOW is often more stable than MSMF for continuous reads.
        if cv2.__dict__.get("CAP_DSHOW") is not None:
            return [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
        return [cv2.CAP_ANY]

    def _open_capture(self):
        self.release()
        for backend in self._backend_candidates():
            cap = cv2.VideoCapture(self.index, backend)
            if cap.isOpened():
                self.cap = cap
                return
            cap.release()
        raise RuntimeError("Webcam not accessible")

    def read(self):
        for _ in range(3):
            if self.cap is None or not self.cap.isOpened():
                self._open_capture()

            ret, frame = self.cap.read()
            if ret:
                return frame

            # Recover from transient backend/camera failures by reopening capture.
            self._open_capture()

        raise RuntimeError("Failed to read webcam frame after retries")

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
