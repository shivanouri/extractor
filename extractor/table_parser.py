import cv2

from extractor import Row, Cell, Table
from extractor.helpers import *


def parse_table(table_image_path):
    table_image = cv2.imread(table_image_path)

    horizontal_lines = detect_horizontal_lines(table_image, ratio=0.7)
    vertical_lines = detect_vertical_lines(table_image, ratio=0.7)

    rows_locations = segment_by_horizontal_lines(table_image, horizontal_lines)

    table = Table()
    for row_location in rows_locations:
        rows = list()
        row_image = crop(table_image, row_location)
        cells_locations = segment_by_vertical_lines(
            row_image,
            vertical_lines,
            x_offset=row_location.x,
            y_offset=row_location.y
        )
        cells = list()
        for cell_location in cells_locations:
            row = Row()
            cells.append(Cell(image=crop(table_image, cell_location)))
        row.cells = cells
        rows.append(row)
    table.rows = rows
