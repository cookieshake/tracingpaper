from PIL import ImageGrab
import cv2
import numpy as np
from mss import mss

from tracingpaper.application.port.outbound import GetImagePort


class ReadImageFile(GetImagePort):
    def __init__(self, path: str) -> None:
        self.path = path

    def get_image(self) -> cv2.typing.MatLike:
        image = cv2.imread(self.path)
        return image

class ScreenCapture(GetImagePort):
    def get_image(self) -> cv2.typing.MatLike:
        with mss() as sct:
            monitor = sct.monitors[2]
            image = np.array(sct.grab(monitor))[:, :, :3]
            return image
