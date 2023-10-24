from typer import Typer
import flet as ft

from tracingpaper.adapter.outbound.image import ScreenCapture
from tracingpaper.adapter.outbound.ocr import EasyOcrEngine, MangaOcrEngine
from tracingpaper.application.service.image import ImageService
from tracingpaper.application.service.ocr import OcrService


app = Typer()

@app.command()
def screenshot():
    get_image_port = ScreenCapture()
    get_boxes_from_image_port = EasyOcrEngine()
    get_text_from_box_port = MangaOcrEngine()

    get_image_use_case = ImageService(get_image_port=get_image_port)
    get_text_from_image_use_case = OcrService(get_boxes_from_image_port=get_boxes_from_image_port, get_text_from_box_port=get_text_from_box_port)
   
    image = get_image_use_case.get_image()
    textboxes = get_text_from_image_use_case.get_text_from_image(image)

    def testpage(page: ft.Page):
        page.window_bgcolor = ft.colors.TRANSPARENT
        page.bgcolor = ft.colors.TRANSPARENT
        page.window_title_bar_hidden = True
        page.window_frameless = False
        page.window_top = 0
        page.window_left = 0
        page.window_width = 3840
        page.window_height = 2160
        page.window_movable = False
        page.window_always_on_top = False
        page.window_maximized = False
        page.padding = 0
        texts = []
        for tb in textboxes:
            width = int((tb.box.top_right.x - tb.box.top_left.x) / 2)
            height = int((tb.box.bottom_left.y - tb.box.top_left.y) / 2)
            left = int(tb.box.top_left.x / 2)
            top = int(tb.box.top_left.y / 2)
            texts.append(ft.Container(bgcolor=ft.colors.BLACK, width=width, height=height, left=left, top=top))
        page.add(ft.Stack(texts, width=page.window_width, height=page.window_height))
    ft.app(target=testpage)

@app.command()
def test():
    pass

        

        

if __name__ == "__main__":
    app()