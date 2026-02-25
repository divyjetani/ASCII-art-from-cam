import cv2
import numpy as np
from config import ASCII_CHARS, FRAME_WIDTH, ASPECT_RATIO_CORRECTION

class ASCIIConverter:
    def convert(self, frame, brightness, contrast):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply brightness & contrast
        adjusted = cv2.convertScaleAbs(
            gray,
            alpha=contrast,
            beta=brightness
        )

        h, w = adjusted.shape
        new_h = int(FRAME_WIDTH * (h / w) * ASPECT_RATIO_CORRECTION)
        resized = cv2.resize(adjusted, (FRAME_WIDTH, new_h))

        chars = ASCII_CHARS
        scale = len(chars) - 1

        lines = []
        for row in resized:
            line = "".join(chars[int(p) * scale // 255] for p in row)
            lines.append(line)

        return "\n".join(lines)
