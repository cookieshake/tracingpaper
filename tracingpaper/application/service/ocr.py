
import cv2
from tracingpaper.application.port.inbound import GetTextFromImageUseCase
from tracingpaper.application.port.outbound import GetBoxesFromImagePort, GetTextFromBoxPort
from tracingpaper.domain.ocr import TextBox


class OcrService(GetTextFromImageUseCase):
    def __init__(self,
                get_boxes_from_image_port: GetBoxesFromImagePort,
                get_text_from_box_port: GetTextFromBoxPort):
        self.get_boxes_from_image_port = get_boxes_from_image_port
        self.get_text_from_box_port = get_text_from_box_port

    def get_text_from_image(self, image: cv2.typing.MatLike) -> list[TextBox]:
        boxes = self.get_boxes_from_image_port.get_boxes_from_image(image)
        textboxes = self.get_text_from_box_port.get_text_from_boxes(image, boxes)
        return textboxes