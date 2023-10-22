from abc import ABCMeta, abstractmethod

import cv2

from tracingpaper.domain.ocr import Box, TextBox


class GetBoxesFromImagePort(metaclass=ABCMeta):
    @abstractmethod
    def get_boxes_from_image(self, image: cv2.typing.MatLike) -> list[Box]:
        pass

class GetTextFromBoxPort(metaclass=ABCMeta):
    @abstractmethod
    def get_text_from_boxes(self,image: cv2.typing.MatLike, boxes: list[Box]) -> list[TextBox]:
        pass

class GetImagePort(metaclass=ABCMeta):
    @abstractmethod
    def get_image(self) -> cv2.typing.MatLike:
        pass