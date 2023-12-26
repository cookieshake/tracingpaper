import math
from pathlib import Path
import re

import cv2
import easyocr
import pytesseract
import numpy as np
import jaconv

from tracingpaper.application.port.outbound import (
    GetBoxesFromImagePort,
    GetTextFromBoxPort,
)
from tracingpaper.domain.ocr import Box, Point, TextBox


class EasyOcrEngine(GetBoxesFromImagePort, GetTextFromBoxPort):
    def __init__(self):
        self._reader = easyocr.Reader(["ja", "en"])

    def get_boxes_from_image(self, image: cv2.typing.MatLike) -> list[Box]:
        boxes = []
        horizontal, free = self._reader.detect(image, width_ths=.1, text_threshold=.1, link_threshold=.1)
        for box in horizontal[0]:
            boxes.append(
                Box(
                    top_left=Point(x=box[0], y=box[2]),
                    top_right=Point(x=box[1], y=box[2]),
                    bottom_left=Point(x=box[0], y=box[3]),
                    bottom_right=Point(x=box[1], y=box[3])
                )
            )
        for box in free[0]:
            boxes.append(
                Box(
                    top_left=Point(x=round(box[0][0]), y=round(box[0][1])),
                    top_right=Point(x=round(box[1][0]), y=round(box[1][1])),
                    bottom_left=Point(x=round(box[3][0]), y=round(box[3][1])),
                    bottom_right=Point(x=round(box[2][0]), y=round(box[2][1]))
                )
            )
        return boxes
    
    def get_text_from_boxes(self, image: cv2.typing.MatLike, boxes: list[Box]) -> list[TextBox]:
        textboxes = []
        horizontal = []
        free = []
        for box in boxes:
            if box.is_rectangle():
                horizontal.append([box.top_left.x, box.top_right.x, box.top_right.y, box.bottom_right.y])
            else:
                free.append([
                    [box.top_left.x, box.top_left.y],
                    [box.top_right.x, box.top_right.y],
                    [box.bottom_right.x, box.bottom_right.y],
                    [box.bottom_left.x, box.bottom_left.y]
                ])
        result = self._reader.recognize(image, horizontal_list=horizontal, free_list=free, output_format="dict")
 
        for box in result:
            textboxes.append(
                TextBox(
                    text=box["text"],
                    box=Box(
                        top_left=Point(x=box["boxes"][0][0], y=box["boxes"][0][1]),
                        top_right=Point(x=box["boxes"][1][0], y=box["boxes"][1][1]),
                        bottom_left=Point(x=box["boxes"][3][0], y=box["boxes"][3][1]),
                        bottom_right=Point(x=box["boxes"][2][0], y=box["boxes"][2][1])
                    ),
                    score=box["confident"]
                )
            )
        return textboxes

class MangaOcrEngine(GetTextFromBoxPort):
    model_name='kha-white/manga-ocr-base'

    def __init__(self):
        from transformers import AutoFeatureExtractor, AutoTokenizer, VisionEncoderDecoderModel
        self.feature_extractor = AutoFeatureExtractor.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = VisionEncoderDecoderModel.from_pretrained(self.model_name)

    def get_text_from_boxes(self, image: cv2.typing.MatLike, boxes: list[Box]) -> list[TextBox]:
        textboxes = []
        for box in boxes:
            boxx = box.get_container_box()
            img = image[boxx.top_left.y:boxx.bottom_left.y, boxx.top_left.x:boxx.top_right.x]
            
            x = self._preprocess(img)
            x = self.model.generate(x[None], max_length=300, return_dict_in_generate=True, output_scores=True)
            transition_scores = self.model.compute_transition_scores(
                x.sequences, x.scores, x.beam_indices, normalize_logits=False
            )
            x = self.tokenizer.decode(x.sequences[0], skip_special_tokens=True)
            x = self._post_process(x)
            textboxes.append(
                TextBox(
                    text=x,
                    box=box,
                    score=np.exp(transition_scores).mean()
                )
            )
        return textboxes

    def _preprocess(self, img: cv2.typing.MatLike):
        pixel_values = self.feature_extractor(img, return_tensors="pt").pixel_values
        return pixel_values.squeeze()
    
    def _post_process(self, text: str):
        text = ''.join(text.split())
        text = text.replace('…', '...')
        text = re.sub('[・.]{2,}', lambda x: (x.end() - x.start()) * '.', text)
        text = jaconv.h2z(text, ascii=True, digit=True)

        return text
                


if __name__ == "__main__":
    image = cv2.imread("data/ocr_test_3.webp")

    e = EasyOcrEngine()
    boxes = e.get_boxes_from_image(image)
    boxes = MangaOcrEngine().get_text_from_boxes(image, boxes)

    from PIL import Image, ImageDraw, ImageFont
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/Users/cookieshake/Downloads/motomachi-20220718/Motomachi-Regular.ttf", 15)
    for box in boxes:
        draw.polygon(box.box.as_np_array().flatten().tolist(), outline=(255, 255, 0))

        text = box.text
        text_position = (box.box.bottom_left.x, box.box.bottom_left.y)
        bbox = draw.textbbox(xy=text_position, text=text, font=font)
        draw.rectangle(bbox, fill=(255, 255, 0))
        draw.text(xy=text_position, text=text, fill=(0, 0, 0), font=font)
        
    image.show()
    
