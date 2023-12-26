from typer import Typer
import flet as ft
from tracingpaper.adapter.outbound.gui import FletGUI

from tracingpaper.adapter.outbound.image import ScreenCapture
from tracingpaper.adapter.outbound.ocr import EasyOcrEngine, MangaOcrEngine
from tracingpaper.application.service.gui import GUIService
from tracingpaper.application.service.image import ImageService
from tracingpaper.application.service.ocr import OcrService


app = Typer()

@app.command()
def screenshot():
    get_image_port = ScreenCapture(monitor=1)
    get_boxes_from_image_port = EasyOcrEngine()
    get_text_from_box_port = MangaOcrEngine()

    get_image_use_case = ImageService(get_image_port=get_image_port)
    get_text_from_image_use_case = OcrService(get_boxes_from_image_port=get_boxes_from_image_port, get_text_from_box_port=get_text_from_box_port)
   
    image = get_image_use_case.get_image()
    textboxes = get_text_from_image_use_case.get_text_from_image(image)
    print(textboxes)
    gui_port = FletGUI(monitor=1)
    gui_service = GUIService(gui_port=gui_port)
    gui_service.draw_text_boxes_to_screen(textboxes)

@app.command()
def test():
    pass
        

if __name__ == "__main__":
    app()