from abc import ABCMeta, abstractmethod

import cv2

from tracingpaper.domain.ocr import TextBox

class GetImageUseCase(metaclass=ABCMeta):
    @abstractmethod
    def get_image(self) -> cv2.typing.MatLike:
        pass

class GetTextFromImageUseCase(metaclass=ABCMeta):
    @abstractmethod
    def get_text_from_image(self, image: cv2.typing.MatLike) -> list[TextBox]:
        pass

class DrawTextBoxesToScreen(metaclass=ABCMeta):
    @abstractmethod
    def draw_text_boxes_to_screen(self, textboxes: list[TextBox]):
        pass
