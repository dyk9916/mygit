from fpdf import FPDF
from PIL import Image

def png_to_pdf(png_path, pdf_path):
    image = Image.open(png_path)
    pdf = FPDF()
    pdf.add_page()
    pdf.image(png_path, x=10, y=8, w=190)
    pdf.output(pdf_path)