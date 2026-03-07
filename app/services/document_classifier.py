from app.services.llm_service import call_llm
import json
import re


def extract_json(text):
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None

    try:
        return json.loads(match.group())
    except:
        return None


def classify_document(raw_text):

    prompt = f"""
Classify the following document into one of these types:

Invoice
Receipt
Purchase Order
Bank Statement
Utility Bill
Unknown

Return ONLY JSON like this:
{{"document_type": ""}}

Document:
{raw_text[:1000]}
"""

    output = call_llm(prompt)

    data = extract_json(output)

    if data and "document_type" in data:
        return data["document_type"]

    return "Unknown"