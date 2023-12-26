from threading import Thread

import flet as ft
from mss import mss


from tracingpaper.application.port.outbound import GUIPort


class FletGUI(GUIPort):
    def __init__(self, monitor: int):
        with mss() as sct:
            self.monitor = sct.monitors[monitor]
        
        def startpage(page: ft.Page):
            page.window_bgcolor = ft.colors.TRANSPARENT
            page.bgcolor = ft.colors.TRANSPARENT
            page.window_title_bar_hidden = True
            page.window_frameless = False
            page.window_top = self.monitor["top"]
            page.window_left = self.monitor["left"]
            page.window_width = self.monitor["width"]
            page.window_height = self.monitor["height"]
            page.window_movable = False
            page.window_always_on_top = False
            page.window_maximized = False
            page.padding = 0
            self.stack = ft.Stack(controls=[], width=page.window_width, height=page.window_height)
            page.add(self.stack)
            self.page = page
        thread = Thread(target=ft.app, kwargs={"target": startpage})
        thread.run()

    def draw_text_boxes_to_screen(self, textboxes):
        controls = []
        for tb in textboxes:
            width = int((tb.box.top_right.x - tb.box.top_left.x) / 2)
            height = int((tb.box.bottom_left.y - tb.box.top_left.y) / 2)
            left = int(tb.box.top_left.x / 2)
            top = int(tb.box.top_left.y / 2)
            controls.append(ft.Container(bgcolor=ft.colors.BLACK, width=width, height=height, left=left, top=top))
        self.stack.controls = controls
        self.stack.update()
        self.page.update()
        

        