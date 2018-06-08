from io import BytesIO

import PyPDF2
import requests
from pdf2image import convert_from_bytes


def url_to_pypdf(url):
    r = requests.get(url)
    f = BytesIO(r.content)

    return PyPDF2.PdfFileReader(f)


def convert_pdf_from_url_to_pil_images(url):
    r = requests.get(url)

    return convert_from_bytes(r.content)
