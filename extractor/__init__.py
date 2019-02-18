__version__ = 'v0.1.0'


class Location:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Cell:
    def __init__(self, image, text=None):
        self.image = image
        self.text = text

    def ocr(self):
        # do ocr on self.image
        # return text
        pass


class Row:
    def __init__(self, cells: list=None):
        self.cells = cells or list()


class Table:
    def __init__(self, rows: list=None):
        self.rows = rows or list()
