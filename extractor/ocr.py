from PIL import Image
from tesserocr import PyTessBaseAPI

from extractor.exceptions import NoImageError

OCR_CHARACTER_WHITELIST = '0123456789abcdefghijklmnopqrstuvwxyz' \
                          'ABCDEFGHIJKLMNOPQRSTUVWXYZ$/-.'


class Ocr:
    def __init__(self):
        self.api = None

    def __enter__(self):
        self.api = PyTessBaseAPI().__enter__()
        self.api.SetVariable(
            'tessedit_char_whitelist', OCR_CHARACTER_WHITELIST
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.api.__exit__(exc_type, exc_val, exc_tb)

    def get_characters(self, image):
        h, w = image.shape[:2]

        if h < 1 or w < 1:
            raise NoImageError()

        img_pil = Image.fromarray(image)
        self.api.SetImage(img_pil)
        cell_text = self.api.GetUTF8Text().strip()
        confidence = self.api.MeanTextConf()

        return cell_text, confidence
