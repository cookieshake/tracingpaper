import cv2
from tracingpaper.application.port.inbound import GetImageUseCase
from tracingpaper.application.port.outbound import GetImagePort

class ImageService(GetImageUseCase):
    def __init__(self, get_image_port: GetImagePort):
        self.get_image_port = get_image_port

    def get_image(self) -> cv2.typing.MatLike:
        return self.get_image_port.get_image()
