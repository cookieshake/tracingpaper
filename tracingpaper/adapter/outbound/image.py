from PIL import ImageGrab
import cv2
import numpy as np

from tracingpaper.application.port.outbound import GetImagePort


class ReadImageFile(GetImagePort):
    def get_image(self) -> cv2.typing.MatLike:
        image = cv2.imread(self.path)
        return image

class ScreenCapture(GetImagePort):
    def get_image(self) -> cv2.typing.MatLike:
        image = ImageGrab.grab()
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image
