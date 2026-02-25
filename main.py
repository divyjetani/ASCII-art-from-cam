import time
import cv2

from camera.webcam import Webcam
from ascii_converter.converter import ASCIIConverter
from utils.terminal import init_terminal, draw, restore_terminal
from utils.keyboard import Keyboard, get_key
from recorder.recorder import Recorder
from state import AppState
from config import *

def main():
    cam = Webcam(CAMERA_INDEX)
    conv = ASCIIConverter()
    state = AppState()
    recorder = Recorder()

    init_terminal()
    last_time = time.time()

    with Keyboard():
        while True:
            key = get_key()

            if key:
                if key == "q":
                    break
                elif key == "p":
                    state.paused = not state.paused
                elif key == "r":
                    state.recording = not state.recording
                elif key == "+":
                    state.brightness = min(100, state.brightness + 5)
                elif key == "-":
                    state.brightness = max(-100, state.brightness - 5)
                elif key == "]":
                    state.contrast = min(3.0, state.contrast + 0.1)
                elif key == "[":
                    state.contrast = max(0.5, state.contrast - 0.1)
                elif key == "f":
                    state.show_fps = not state.show_fps
                elif key == "c":
                    state.brightness = 0
                    state.contrast = 1.0

            if state.paused:
                time.sleep(0.05)
                continue

            frame = cam.read()
            if FLIP_HORIZONTAL:
                frame = cv2.flip(frame, 1)

            ascii_frame = conv.convert(
                frame,
                state.brightness,
                state.contrast
            )

            now = time.time()
            fps = 1 / (now - last_time)
            last_time = now

            hud = ""
            if state.show_fps:
                hud = (
                    f"\nFPS:{fps:5.1f} "
                    f"| B:{state.brightness:+4d} "
                    f"| C:{state.contrast:.1f} "
                    f"| REC:{state.recording} "
                    f"| PAUSE:{state.paused}\n"
                )
            output = ascii_frame + hud

            draw(output)

            if state.recording:
                recorder.add(ascii_frame)

            time.sleep(max(0, 1 / FPS_LIMIT))

    cam.release()
    restore_terminal()
    
    if recorder.frames:
        path = recorder.save()
        print(f"\nSaved recording: {path}")

if __name__ == "__main__":
    main()
