from injector import inject

from tracingpaper.application.port.inbound import GetImageUseCase, GetTextFromImageUseCase
from tracingpaper.domain.ocr import TextBox

class ScanImageAndGetResult(object):
    @inject
    def __init__(self,
                get_image_use_case: GetImageUseCase,
                get_text_boxes_from_image_use_case: GetTextFromImageUseCase):
        self.get_image_use_case = get_image_use_case
        self.get_text_boxes_from_image_use_case = get_text_boxes_from_image_use_case

    def execute(self) -> list[TextBox]:
        image = self.get_image_use_case.get_image()
        textboxes = self.get_text_boxes_from_image_use_case.get_text_from_image(image)
        return textboxes
