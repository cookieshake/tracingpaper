
from tracingpaper.application.port.inbound import DrawTextBoxesToScreen
from tracingpaper.application.port.outbound import GUIPort
from tracingpaper.domain.ocr import TextBox


class GUIService(DrawTextBoxesToScreen):
    def __init__(self, gui_port: GUIPort):
        self.gui_port = gui_port

    def draw_text_boxes_to_screen(self, textboxes: list[TextBox]):
        return self.gui_port.draw_text_boxes_to_screen(textboxes)