
import fitz
import pdfplumber
import easyocr
from PIL import Image
import io

def extract_vector_pdf(pdf):
    doc =fitz.open(pdf)
    for page in doc:
        text = page.get_text()
        print(text)
extract_vector_pdf("sample_files/vector.pdf")


reader = easyocr.Reader(['en'])
def extract_raster_pdf(pdf):
    doc = fitz.open(pdf)
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img_bytes = pix.tobytes("png")
        text = reader.readtext(img_bytes, detail=0,paragraph=True) 
        print("\n".join(text))

extract_raster_pdf("sample_files/raster.pdf")

def extract_pdf_tables(pdf):
    doc = pdfplumber.open(pdf)
    for page in doc.pages:
        text = page.extract_text()
        print(text)

extract_pdf_tables("sample_files/table.pdf")


