import os
import pdfplumber
import pytesseract
import requests
from PIL import Image


INVOICE_FOLDER = "invoices"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"


def scan_invoices():

    return [
        f for f in os.listdir(INVOICE_FOLDER)
        if f.lower().endswith((".pdf", ".jpg", ".jpeg", ".png"))
    ]


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

    return extract_text_from_image(path)


def call_llm(text):

    short_text = text[:1500]

    prompt = f"""
Return invoice info as JSON only.

Format:
{{
 "Invoice_Date":"",
 "Vendor_Name":"",
 "Net_Amount":"",
 "Tax_Amount":"",
 "Total_Amount":""
}}

Invoice:
{short_text}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload)

    return r.json().get("response", "")


def main():

    invoices = scan_invoices()

    for file in invoices:

        path = os.path.join(INVOICE_FOLDER, file)

        print("Processing:", file)

        text = extract_text(path)

        llm_out = call_llm(text)

        print(llm_out)
        print()


if __name__ == "__main__":
    main()