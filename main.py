import os
import pdfplumber
import pytesseract
from PIL import Image


INVOICE_FOLDER = "invoices"


def scan_invoices():

    files = os.listdir(INVOICE_FOLDER)

    invoice_files = []

    for file in files:
        if file.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
            invoice_files.append(file)

    return invoice_files


def extract_text_from_pdf(path):

    text = ""

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"

    return text


def extract_text_from_image(path):

    img = Image.open(path)
    return pytesseract.image_to_string(img)


def extract_text(path):

    if path.lower().endswith(".pdf"):
        return extract_text_from_pdf(path)
    else:
        return extract_text_from_image(path)


def main():

    invoices = scan_invoices()

    for file in invoices:

        path = os.path.join(INVOICE_FOLDER, file)

        print("=" * 50)
        print("Processing:", file)

        text = extract_text(path)

        print(text)


if __name__ == "__main__":
    main()