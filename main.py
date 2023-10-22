

from injector import Binder, Injector, Module, provider, singleton
from typer import Typer
from tracingpaper.adapter.inbound.scan import ScanImageAndGetResult
from tracingpaper.adapter.outbound.image import ReadImageFile
from tracingpaper.adapter.outbound.ocr import EasyOcrEngine, MangaOcrEngine
from tracingpaper.application.port.inbound import GetImageUseCase, GetTextFromImageUseCase

from tracingpaper.application.port.outbound import GetBoxesFromImagePort, GetImagePort, GetTextFromBoxPort
from tracingpaper.application.service.image import ImageService
from tracingpaper.application.service.ocr import OcrService


app = Typer()

@app.command()
def screenshot(path: str):
    class M(Module):
        @provider
        def provide_get_image_port(self) -> GetImagePort:
            return ReadImageFile(path)
        
        @provider
        def provide_get_boxes_from_image_port(self) -> GetBoxesFromImagePort:
            return EasyOcrEngine()
        
        @provider
        def provide_get_text_from_box_port(self) -> GetTextFromBoxPort:
            return MangaOcrEngine()
        
        @provider
        def provide_get_image_use_case(self) -> GetImageUseCase:
            return ImageService()
        
        @provider
        def provide_get_text_from_image_use_case(self) -> GetTextFromImageUseCase:
            return OcrService()
        
    injector = Injector([M])
    scan_image_and_get_result = injector.get(ScanImageAndGetResult)
    scan_image_and_get_result.execute()
        
    
        

        

if __name__ == "__main__":
    app()