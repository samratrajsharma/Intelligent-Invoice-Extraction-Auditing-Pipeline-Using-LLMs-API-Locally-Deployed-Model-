import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def call_llm(prompt):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json().get("response", "").strip()


def extract_json(text):

    match = re.search(r"\{[\s\S]*\}", text)

    if not match:
        return None

    try:
        return json.loads(match.group())
    except:
        return None


def extract_document_fields(raw_text):

    prompt = f"""
Extract key fields from this financial document and return ONLY JSON.

Fields:
{{
  "document_type": "",
  "vendor_name": "",
  "invoice_date": "",
  "total_amount": ""
}}

Document:
{raw_text[:1500]}
"""

    output = call_llm(prompt)

    data = extract_json(output)

    return data