from tkinter import Tk
from tkinter.filedialog import askopenfilename

from extractor.table_parser import parse_table


def file_reader():
    Tk().withdraw()
    filename = askopenfilename()
    parse_table(filename)


if __name__ == '__main__':
    file_reader()
