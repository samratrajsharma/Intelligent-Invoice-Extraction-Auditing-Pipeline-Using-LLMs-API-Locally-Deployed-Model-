import pdfplumber
import pytesseract
from PIL import Image


def extract_text_from_pdf(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


def extract_text_from_image(file_path):

    image = Image.open(file_path)

    text = pytesseract.image_to_string(image)

    return text


def extract_text(file_path):

    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.lower().endswith((".jpg", ".jpeg", ".png")):
        return extract_text_from_image(file_path)

    return ""