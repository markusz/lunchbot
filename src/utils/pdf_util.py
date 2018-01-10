from datetime import datetime
import PyPDF2
import requests
from io import BytesIO
from pdf2image import convert_from_path, convert_from_bytes

def url_to_pypdf(url):
    r = requests.get(url)
    f = BytesIO(r.content)

    images = convert_from_bytes(r.content)
    images[0].save('test.jpg')

    return PyPDF2.PdfFileReader(f)

def convert_pdf_from_url_to_pil_images(url):
    r = requests.get(url)

    images = convert_from_bytes(r.content)
    images[0].save('test.jpg')
    return images