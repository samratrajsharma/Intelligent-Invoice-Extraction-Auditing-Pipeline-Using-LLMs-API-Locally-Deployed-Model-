import os
import re
import json
import requests
import pdfplumber
import pytesseract
from PIL import Image
from dateutil import parser


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

    short = text[:1500]

    prompt = f"""
Return ONLY JSON.

{{
 "Invoice_Date":"",
 "Vendor_Name":"",
 "Net_Amount":"",
 "Tax_Amount":"",
 "Total_Amount":""
}}

{short}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload)

    return r.json().get("response", "")


def extract_json(text):

    m = re.search(r"\{[\s\S]*\}", text)

    if not m:
        return None

    try:
        return json.loads(m.group())
    except:
        return None


def clean_amount(val):

    if not val:
        return 0.0

    val = val.replace("$", "").replace(",", "")

    return float(val)


def normalize_date(d):

    try:
        dt = parser.parse(d, dayfirst=True)
        return dt.strftime("%Y-%m-%d")
    except:
        return ""


def main():

    invoices = scan_invoices()

    for file in invoices:

        path = os.path.join(INVOICE_FOLDER, file)

        text = extract_text(path)

        llm = call_llm(text)

        data = extract_json(llm)

        if not data:
            print("Parse failed:", file)
            continue

        cleaned = {
            "Invoice_Date": normalize_date(data["Invoice_Date"]),
            "Vendor_Name": data["Vendor_Name"],
            "Net_Amount": clean_amount(data["Net_Amount"]),
            "Tax_Amount": clean_amount(data["Tax_Amount"]),
            "Total_Amount": clean_amount(data["Total_Amount"])
        }

        print(cleaned)


if __name__ == "__main__":
    main()