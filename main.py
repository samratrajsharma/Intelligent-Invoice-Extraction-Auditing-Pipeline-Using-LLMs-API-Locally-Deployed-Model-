import os
import pdfplumber
import pytesseract
from PIL import Image
import requests
import json
import re
from dateutil import parser
import pandas as pd


INVOICE_FOLDER = "invoices"

APPROVED_FILE = "outputs/approved_invoices.csv"
REVIEW_FILE = "outputs/manual_review_needed.txt"


def scan_invoices():

    files = os.listdir(INVOICE_FOLDER)

    invoice_files = []

    for file in files:
        if file.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
            invoice_files.append(file)

    return invoice_files


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

    else:
        return ""


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def extract_invoice_data_with_llm(raw_text):

    short_text = raw_text[:1500]

    # Primary prompt (lightweight)
    prompt_1 = f"""
Extract invoice fields and return JSON only.

Format:
{{
  "Invoice_Date": "YYYY-MM-DD",
  "Vendor_Name": "",
  "Net_Amount": "",
  "Tax_Amount": "",
  "Total_Amount": ""
}}

Invoice:
{short_text}
"""

    # Fallback prompt (stronger)
    prompt_2 = f"""
Return ONLY this JSON. No text. No explanation.

{{
  "Invoice_Date": "",
  "Vendor_Name": "",
  "Net_Amount": "",
  "Tax_Amount": "",
  "Total_Amount": ""
}}

Fill using this invoice:

{short_text}
"""

    def call_llm(prompt):

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {"num_ctx": 2048}
        }

        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        return response.json().get("response", "").strip()

    try:
        # First attempt
        output = call_llm(prompt_1)

        if extract_json_from_text(output):
            return output

        # Retry with strict prompt
        output = call_llm(prompt_2)

        return output

    except Exception as e:
        print(f"LLM Error: {e}")
        return ""
    
def extract_json_from_text(text):
    """
    Extract JSON object from messy LLM output
    """

    # Try to find first JSON object
    match = re.search(r"\{[\s\S]*\}", text)

    if not match:
        return None

    json_text = match.group(0)

    try:
        return json.loads(json_text)

    except json.JSONDecodeError:
        return None
    
def clean_amount(value):
    """
    Convert currency string to float
    """
    if not value:
        return 0.0

    value = value.replace("$", "").replace(",", "").strip()

    try:
        return float(value)
    except:
        return 0.0
def normalize_date(date_str):
    """
    Convert date to YYYY-MM-DD
    """
    try:
        dt = parser.parse(date_str, dayfirst=True)
        return dt.strftime("%Y-%m-%d")
    except:
        return ""
    

def process_llm_output(llm_text):
    """
    Parse, clean, and standardize LLM output
    """

    data = extract_json_from_text(llm_text)

    if not data:
        return None

    cleaned = {
        "Invoice_Date": normalize_date(data.get("Invoice_Date", "")),
        "Vendor_Name": data.get("Vendor_Name", "").strip(),
        "Net_Amount": clean_amount(data.get("Net_Amount", "")),
        "Tax_Amount": clean_amount(data.get("Tax_Amount", "")),
        "Total_Amount": clean_amount(data.get("Total_Amount", ""))
    }

    return cleaned

def is_invoice_valid(data):
    """
    Validate net + tax == total (±0.01)
    """

    calculated = data["Net_Amount"] + data["Tax_Amount"]
    reported = data["Total_Amount"]

    if abs(calculated - reported) <= 0.01:
        return True, calculated, reported

    return False, calculated, reported

def save_to_csv(data):

    df = pd.DataFrame([data])

    if not os.path.exists(APPROVED_FILE):
        df.to_csv(APPROVED_FILE, index=False)
    else:
        df.to_csv(APPROVED_FILE, mode="a", header=False, index=False)

def log_invalid_invoice(filename, calc, reported):

    message = (
        f"{filename} | Math Mismatch: "
        f"Calculated {calc:.2f} vs Total {reported:.2f}\n"
    )

    with open(REVIEW_FILE, "a") as f:
        f.write(message)

def main():

    invoices = scan_invoices()

    print(f"\nFound {len(invoices)} invoice files\n")

    for file in invoices:

        path = os.path.join(INVOICE_FOLDER, file)

        print("=" * 60)
        print(f"Processing: {file}\n")

        text = extract_text(path)

        print("Sending to LLM...\n")

        llm_output = extract_invoice_data_with_llm(text)

        parsed = process_llm_output(llm_output)

        if not parsed:
            print("Failed to parse LLM output\n")
            continue

        valid, calc, reported = is_invoice_valid(parsed)

        if valid:
            print("Status: APPROVED ✅\n")
            save_to_csv(parsed)

        else:
            print("Status: FLAGGED ❌\n")
            log_invalid_invoice(file, calc, reported)
        print("=" * 60)
        print("\n")


if __name__ == "__main__":
    main()