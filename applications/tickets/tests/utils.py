import os
from typing import cast
from PyPDF2 import PdfFileReader
from PIL import Image

_dir = os.path.dirname(os.path.realpath(__file__))


def load_mock_pdf() -> bytes:
    reader = PdfFileReader(f"{_dir}/fixtures/document.pdf")
    return cast(bytes, reader.stream)


def load_mock_image():
    return Image.open(f"{_dir}/fixtures/qr.png")
