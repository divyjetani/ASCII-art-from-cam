import time
from pathlib import Path

import cv2

class Recorder:
    def __init__(self, fps=30, codec="mp4v", ext="mp4"):
        self.frames = []
        self.fps = fps
        self.codec = codec
        self.ext = ext

    def add(self, frame):
        self.frames.append(frame.copy())

    def save(self):
        recordings_dir = Path("recordings")
        recordings_dir.mkdir(parents=True, exist_ok=True)

        name = recordings_dir / f"ascii_{int(time.time())}.{self.ext}"
        first = self.frames[0]
        height, width = first.shape[:2]

        writer = cv2.VideoWriter(
            str(name),
            cv2.VideoWriter_fourcc(*self.codec),
            float(self.fps),
            (width, height),
        )

        for frame in self.frames:
            if frame.shape[0] != height or frame.shape[1] != width:
                frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
            writer.write(frame)

        writer.release()
        return str(name)
