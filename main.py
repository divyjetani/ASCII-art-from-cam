import time
import cv2
import numpy as np

from camera.webcam import Webcam
from ascii_converter.converter import ASCIIConverter
from recorder.recorder import Recorder
from state import AppState
from config import *


WINDOW_NAME = "ASCII Camera (Original | ASCII)"


def ascii_to_image(ascii_frame, target_height, target_width):
    lines = ascii_frame.splitlines()
    if not lines:
        return np.zeros((target_height, target_width, 3), dtype=np.uint8)

    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 0.7
    thickness = 1
    line_height = 11

    max_cols = max(len(line) for line in lines)
    (char_width, _), _ = cv2.getTextSize("W", font, font_scale, thickness)

    width = max(1, max_cols * max(1, char_width))
    height = max(1, len(lines) * line_height + 6)
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    y = line_height
    for line in lines:
        cv2.putText(
            canvas,
            line,
            (0, y),
            font,
            font_scale,
            (255, 255, 255),
            thickness,
            cv2.LINE_AA,
        )
        y += line_height

    return cv2.resize(canvas, (target_width, target_height), interpolation=cv2.INTER_AREA)

def main():
    cam = Webcam(CAMERA_INDEX)
    conv = ASCIIConverter()
    state = AppState()
    recorder = Recorder(FPS_LIMIT, RECORD_VIDEO_CODEC, RECORD_VIDEO_EXT)
    last_time = time.time()
    last_ascii_frame = ""
    last_display_frame = None

    try:
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key != 255:
                k = chr(key).lower() if key < 128 else ""
                if k == "q":
                    break
                elif k == "p":
                    state.paused = not state.paused
                elif k == "r":
                    state.recording = not state.recording
                elif k == "+":
                    state.brightness = min(100, state.brightness + 5)
                elif k == "-":
                    state.brightness = max(-100, state.brightness - 5)
                elif k == "]":
                    state.contrast = min(3.0, state.contrast + 0.1)
                elif k == "[":
                    state.contrast = max(0.5, state.contrast - 0.1)
                elif k == "f":
                    state.show_fps = not state.show_fps
                elif k == "c":
                    state.brightness = 0
                    state.contrast = 1.0

            if not state.paused or last_display_frame is None:
                frame = cam.read()
                if FLIP_HORIZONTAL:
                    frame = cv2.flip(frame, 1)

                ascii_frame = conv.convert(
                    frame,
                    state.brightness,
                    state.contrast
                )
                last_ascii_frame = ascii_frame
                last_display_frame = frame
            else:
                frame = last_display_frame
                ascii_frame = last_ascii_frame

            now = time.time()
            fps = 1 / (now - last_time)
            last_time = now

            frame_with_hud = frame.copy()
            hud_text = (
                f"FPS:{fps:5.1f} | B:{state.brightness:+4d} "
                f"| C:{state.contrast:.1f} | REC:{state.recording} | PAUSE:{state.paused}"
            )
            cv2.putText(
                frame_with_hud,
                hud_text,
                (10, 24),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

            ascii_width = max(1, int(frame_with_hud.shape[1] * ASCII_PANEL_WIDTH_RATIO))
            ascii_img = ascii_to_image(ascii_frame, frame_with_hud.shape[0], ascii_width)
            combined = np.hstack((frame_with_hud, ascii_img))
            cv2.imshow(WINDOW_NAME, combined)

            if state.recording:
                recorder.add(combined)

            time.sleep(max(0, 1 / FPS_LIMIT))
    finally:
        cam.release()
        cv2.destroyAllWindows()

    if recorder.frames:
        path = recorder.save()
        print(f"\nSaved recording: {path}")

if __name__ == "__main__":
    main()
