# AI Financial Intelligence Platform

An **AI-powered financial document intelligence platform** that automatically processes invoices and financial documents, extracts structured information using LLMs, detects financial risks, performs semantic document search, and provides intelligent analytics through a dashboard interface.

This system combines **OCR, LLM reasoning, vector databases, and financial analytics** to create a complete document analysis pipeline.

---

# Project Overview

Organizations process thousands of financial documents such as:

- invoices  
- receipts  
- purchase orders  
- bills  

Manual processing leads to issues like:

- incorrect totals
- duplicate invoices
- fraudulent transactions
- inconsistent vendor activity

This platform automates the entire process using **AI-based document understanding and financial analytics**.

The system can:

- extract structured financial data
- classify document types
- detect anomalies and suspicious activity
- perform semantic document search
- analyze vendor behavior
- answer financial questions through an AI assistant

---

# System Architecture

The platform is built as a **modular AI system** consisting of several components.
# AI Financial Intelligence Platform

An **AI-powered financial document intelligence platform** that automatically processes invoices and financial documents, extracts structured information using LLMs, detects financial risks, performs semantic document search, and provides intelligent analytics through a dashboard interface.

This system combines **OCR, LLM reasoning, vector databases, and financial analytics** to create a complete document analysis pipeline.

---

# Project Overview

Organizations process thousands of financial documents such as:

- invoices  
- receipts  
- purchase orders  
- bills  

Manual processing leads to issues like:

- incorrect totals
- duplicate invoices
- fraudulent transactions
- inconsistent vendor activity

This platform automates the entire process using **AI-based document understanding and financial analytics**.

The system can:

- extract structured financial data
- classify document types
- detect anomalies and suspicious activity
- perform semantic document search
- analyze vendor behavior
- answer financial questions through an AI assistant

---

# System Architecture

The platform is built as a **modular AI system** consisting of several components.
Streamlit Dashboard
│
▼
FastAPI Backend
│
├── Document Upload
│
├── AI Assistant
│
▼
Document Processing Pipeline
│
├── OCR / PDF Parsing
├── Document Classification
├── LLM Data Extraction
├── Risk Engine
├── Financial Anomaly Detection
│
▼
Vector Database (FAISS)
│
▼
SQLite Database
│
▼
Analytics & Vendor Intelligence

---

# Document Processing Pipeline

Each uploaded document follows this AI pipeline:
Document Upload
│
▼
File Storage
│
▼
Text Extraction (OCR / PDF)
│
▼
Document Classification
│
▼
LLM Field Extraction
│
▼
Risk Engine
│
▼
Financial Anomaly Detection
│
▼
Vector Embedding Creation
│
▼
FAISS Vector Database
│
▼
Database Storage
│
▼
Analytics + AI Assistant


---

# Features

## Document Upload and Processing

Upload financial documents through API or dashboard.

Supported formats:

- PDF  
- JPG  
- PNG  
- JPEG  
- TXT  

The system automatically processes the document through the AI pipeline.

---

# OCR and Text Extraction

The platform extracts text from documents using:

- **pdfplumber** for digital PDFs  
- **Tesseract OCR** for scanned images  

This enables processing both **digital invoices and scanned receipts**.

---

# Document Classification

An LLM classifies the document type:

- Invoice  
- Receipt  
- Purchase Order  
- Bank Statement  
- Utility Bill  
- Unknown  

This helps the system apply the correct extraction logic.

---

# LLM Data Extraction

A locally deployed LLM extracts structured financial fields:

- Vendor Name  
- Invoice Date  
- Net Amount  
- Tax Amount  
- Total Amount  

The system uses prompt engineering to enforce **structured JSON outputs**.

---

# Risk Detection Engine

The platform automatically detects suspicious documents.

Rules implemented:

- Duplicate invoices  
- Missing financial fields  
- Incorrect totals  
- Suspicious values  

Each document receives:

- **Risk Score**
- **Risk Reasons**

Example:
Risk Score: 30
Reason: Amount anomaly detected

---

# Financial Anomaly Detection

Vendor spending history is analyzed to detect abnormal invoices.

Example logic:
Vendor average = $200
New invoice = $900
→ flagged as anomaly

This allows detection of:

- vendor fraud
- unusual invoice spikes
- abnormal vendor behavior

---

# Vector Database (FAISS)

Each document is converted into **vector embeddings** using:
sentence-transformers(MiniLM)

Vectors are stored in **FAISS** for semantic search.

This enables:

- similar document detection
- duplicate invoice discovery
- semantic document queries

---

# Semantic Document Search

The system can retrieve documents based on semantic similarity.

Example queries:
Find invoices related to Alibaba
Find similar restaurant receipts
Detect duplicate invoices

---

# AI Financial Assistant (RAG)

An AI assistant answers questions using:
Vector Search + LLM Reasoning

# Example Queries
Show suspicious invoices
Find invoices from Alibaba
Summarize vendor spending

---

# Vendor Intelligence

The system tracks vendor financial behavior.

Metrics include:

- Total invoices  
- Total spending  
- Average invoice value  
- Vendor risk score  
- Invoice history  

Example output:
Vendor: Alibaba Cloud
Total Invoices: 3
Total Spending: $3600
Average Invoice: $1200
Risk Documents: 1


---

# Financial Analytics

The analytics engine provides insights into system data.

Metrics available:

- Total documents processed  
- High-risk documents  
- Vendor spending distribution  
- Financial trends  

---

# Dashboard Interface

A **Streamlit dashboard** provides a user interface for interacting with the system.

Dashboard modules:

- Document Upload  
- Analytics Overview  
- Vendor Intelligence  
- AI Assistant  

---

# Tech Stack

## Backend

- FastAPI  
- Python  
- SQLAlchemy  
- SQLite  

## AI / ML

- Ollama (local LLM)  
- Sentence Transformers  
- FAISS Vector Database  

## Document Processing

- Tesseract OCR  
- pdfplumber  
- Pillow  

## Frontend

- Streamlit Dashboard  

---

# Project Structure
AI_FINOps_Project
│
├── app
│ ├── main.py
│ ├── config.py
│
│ ├── pipelines
│ │ └── document_pipeline.py
│
│ ├── services
│ │ ├── llm_service.py
│ │ ├── text_extraction_service.py
│ │ ├── risk_engine.py
│ │ ├── anomaly_detection_service.py
│ │ ├── vector_service.py
│ │ ├── search_service.py
│ │ ├── analytics_service.py
│ │ ├── vendor_intelligence_service.py
│ │ └── assistant_service.py
│
│ └── models
│ ├── document_model.py
│ └── vector_model.py
│
├── ui
│ └── app.py
│
├── data
│ ├── invoices
│ └── outputs
│
├── vector_store.index
├── finops.db
├── requirements.txt
└── README.md

---

# Installation

## Clone Repository
git clone https://github.com/samratrajsharma/AI-Financial-Operations-&-Risk-Platform

cd AI-Financial-Operations-&-Risk-Platform

# Install Dependencies


pip install -r requirements.txt


---

# Install Ollama

Download:


https://ollama.com


Pull LLM model:


ollama pull qwen2.5:3b


---

# Install Tesseract OCR

Windows download:


https://github.com/UB-Mannheim/tesseract/wiki


Add it to **system PATH**.

---

# Running the Platform

## Start Backend


python run.py


Backend API:


http://127.0.0.1:8000


---

## Start Dashboard


streamlit run ui/app.py


---

# API Endpoints

## Upload Document


POST /upload-document


Uploads and processes a financial document.

---

## Semantic Search


POST /search-similar-documents


Find similar documents using vector search.

---

## AI Assistant


POST /ask-ai


Ask financial questions about stored documents.

---

## Analytics


GET /analytics


Returns financial statistics and insights.

---

## Vendor Insights


GET /vendor-insights/{vendor_name}


Returns vendor spending analysis.

---

# Screenshots

## Dashboard

![Dashboard](data/outputs/dashboard.png)

## Upload Result

![Upload](data/outputs/upload_result.png)

## Analytics

![Analytics](data/outputs/analytics_view.png)

---

# Future Improvements

Possible upgrades:

- PostgreSQL database
- Docker deployment
- Real-time document processing queue
- Advanced fraud detection models
- Multi-user authentication
- Cloud storage integration

---

# Author

Samrat Raj Sharma  
AI / ML Engineer  

---

# License

MIT License

