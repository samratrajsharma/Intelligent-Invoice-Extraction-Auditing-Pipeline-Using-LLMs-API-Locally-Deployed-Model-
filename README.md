# Intelligent Invoice Extraction & Auditing Pipeline

This project implements an automated pipeline to extract, validate, and audit invoice data using OCR and a local Large Language Model (LLM). It processes PDF and image invoices, verifies financial accuracy, and routes results for approval or manual review.

---

## 📌 Objective

The goal of this project is to automate invoice processing by:

- Extracting key invoice fields using an LLM  
- Normalizing and cleaning extracted data  
- Validating financial calculations  
- Routing valid and invalid invoices to appropriate outputs  

This system is designed to handle noisy OCR output, inconsistent formats, and unreliable LLM responses.

---

## 📂 Project Structure

Wisdom-Tree-Project/

    ├── invoices/                  # Input invoice files
    ├── outputs/                   # Generated outputs
    │   ├── approved_invoices.csv
    │   └── manual_review_needed.txt
    ├── main.py
    ├── requirements.txt
    └── README.md

---

## ⚙️ Setup Instructions

### 1. Install Dependencies

Run:
pip install -r requirements.txt


---

### 2. Install Ollama

Download from:  
https://ollama.com

Pull the required model:
ollama pull qwen2.5:3b


---

### 3. Install Tesseract OCR (Windows)

Download from:  
https://github.com/UB-Mannheim/tesseract/wiki

Ensure `tesseract` is added to the system PATH.

---

## ▶️ Running the Pipeline

Run the script using:
python main.py


---

### 3. Install Tesseract OCR (Windows)

Download from:  
https://github.com/UB-Mannheim/tesseract/wiki

Ensure `tesseract` is added to the system PATH.

---

## ▶️ Running the Pipeline

Run the script using:
outputs/approved_invoices.csv


Contains structured and validated invoice data.

---

### Invalid Invoices

Logged in:
outputs/manual_review_needed.txt

Includes filename and validation error.

Example:
invoice_c.pdf | Math Mismatch: Calculated 220.00 vs Total 5000.00


---

## 🧠 LLM & Prompting Strategy

- A local LLM (Qwen2.5:3B) is used via Ollama  
- The prompt enforces strict JSON output  
- Two prompt versions are used:
  - Lightweight prompt for efficiency  
  - Fallback prompt for stronger structure enforcement  
- Output is sanitized using regex-based JSON extraction  

This improves reliability when dealing with inconsistent LLM responses.

---

## 📅 Handling Ambiguous Dates

Invoices may contain ambiguous formats such as:
02/03/24


The system uses `dateutil.parser` with `dayfirst=True` to normalize dates into:
YYYY-MM-DD


This ensures consistent handling across regional formats.

---

## ✅ Validation Logic

Each invoice is validated using:
| (Net_Amount + Tax_Amount) - Total_Amount | ≤ 0.01


If the difference exceeds this threshold, the invoice is flagged for manual review.

---

## 💻 Computing Constraints & Optimization

This project was developed on a low-resource system:

- RAM: 8 GB  
- CPU: Intel i5 (11th Gen)  
- GPU: Not available  

### Challenges Faced

- Memory errors with larger models (Mistral, LLaMA)  
- Ollama server crashes on large prompts  
- Unstable JSON output from small models  

### Solutions Implemented

- Switched to lightweight instruction-tuned model (Qwen2.5:3B)  
- Limited prompt size to 1500 characters  
- Reduced context window  
- Closed background applications  
- Restarted Ollama between runs  
- Implemented prompt fallback mechanism  

These optimizations ensured stable performance without GPU acceleration.

---

## 📊 System Statistics

| Component     | Technology Used        |
|---------------|------------------------|
| OCR           | Tesseract + Pillow     |
| PDF Parsing   | pdfplumber             |
| LLM Backend   | Ollama (Qwen2.5:3B)     |
| Data Handling | pandas                 |
| Date Parsing  | python-dateutil        |

---

## 👤 Author
Samrat Raj Sharma
