import os
import re
import json
import requests
import pdfplumber
import pytesseract
import pandas as pd
from PIL import Image
from dateutil import parser


INVOICE_FOLDER = "invoices"
APPROVED_FILE = "outputs/approved_invoices.csv"
REVIEW_FILE = "outputs/manual_review_needed.txt"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def scan_invoices():
    return [
        f for f in os.listdir(INVOICE_FOLDER)
        if f.lower().endswith((".pdf", ".jpg", ".jpeg", ".png"))
    ]


def extract_text(path):
    if path.lower().endswith(".pdf"):
        with pdfplumber.open(path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    image = Image.open(path)
    return pytesseract.image_to_string(image)


def call_llm(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"num_ctx": 2048}
    }
    r = requests.post(OLLAMA_URL, json=payload)
    r.raise_for_status()
    return r.json().get("response", "").strip()


def extract_invoice_data_with_llm(text):
    text = text[:1500]

    prompts = [
        f"""
Extract invoice fields and return JSON only.

{{
  "Invoice_Date":"YYYY-MM-DD",
  "Vendor_Name":"",
  "Net_Amount":"",
  "Tax_Amount":"",
  "Total_Amount":""
}}

Invoice:
{text}
""",
        f"""
Return ONLY this JSON. No explanation.

{{
  "Invoice_Date":"",
  "Vendor_Name":"",
  "Net_Amount":"",
  "Tax_Amount":"",
  "Total_Amount":""
}}

{text}
"""
    ]

    for prompt in prompts:
        try:
            output = call_llm(prompt)
            if extract_json(output):
                return output
        except:
            pass

    return ""


def extract_json(text):
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except:
        return None


def clean_amount(val):
    if not val:
        return 0.0
    try:
        return float(val.replace("$", "").replace(",", ""))
    except:
        return 0.0


def normalize_date(date):
    try:
        return parser.parse(date, dayfirst=True).strftime("%Y-%m-%d")
    except:
        return ""


def process_llm_output(text):
    data = extract_json(text)
    if not data:
        return None
    return {
        "Invoice_Date": normalize_date(data.get("Invoice_Date")),
        "Vendor_Name": data.get("Vendor_Name", "").strip(),
        "Net_Amount": clean_amount(data.get("Net_Amount")),
        "Tax_Amount": clean_amount(data.get("Tax_Amount")),
        "Total_Amount": clean_amount(data.get("Total_Amount"))
    }


def validate(data):
    calc = data["Net_Amount"] + data["Tax_Amount"]
    total = data["Total_Amount"]
    return abs(calc - total) <= 0.01, calc, total


def save_csv(data):
    df = pd.DataFrame([data])
    df.to_csv(
        APPROVED_FILE,
        mode="a",
        header=not os.path.exists(APPROVED_FILE),
        index=False
    )


def log_error(file, calc, total):
    with open(REVIEW_FILE, "a") as f:
        f.write(
            f"{file} | Math Mismatch: "
            f"Calculated {calc:.2f} vs Total {total:.2f}\n"
        )


def main():
    invoices = scan_invoices()

    print(f"\nFound {len(invoices)} invoice files\n")

    for file in invoices:
        print("=" * 60)
        print(f"Processing: {file}\n")

        path = os.path.join(INVOICE_FOLDER, file)
        text = extract_text(path)

        print("Sending to LLM...\n")

        llm_out = extract_invoice_data_with_llm(text)
        data = process_llm_output(llm_out)

        if not data:
            print("Failed to parse LLM output\n")
            continue

        valid, calc, total = validate(data)

        if valid:
            print("Status: APPROVED ✅\n")
            save_csv(data)
        else:
            print("Status: FLAGGED ❌\n")
            log_error(file, calc, total)

        print("=" * 60, "\n")


if __name__ == "__main__":
    main()