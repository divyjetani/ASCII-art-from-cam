import time

class Recorder:
    def __init__(self):
        self.frames = []

    def add(self, frame):
        self.frames.append(frame)

    def save(self):
        name = f"recordings/ascii_{int(time.time())}.txt"
        with open(name, "w") as f:
            for frame in self.frames:
                f.write(frame + "\n---FRAME---\n")
        return name
