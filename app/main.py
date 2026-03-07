from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List

from app.services.document_service import save_uploaded_file
from app.pipelines.document_pipeline import process_document
from app.config import engine, Base
from app.models.document_model import Document
from app.models.vector_model import VectorMapping
from app.services.search_service import search_similar_documents
from app.services.assistant_service import ask_financial_assistant
from app.services.analytics_service import get_system_analytics
from app.services.vendor_intelligence_service import get_vendor_insights

app = FastAPI(
    title="AI Financial Operations Platform",
    description="AI-powered document intelligence and financial risk system",
    version="1.0"
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "AI FinOps Platform Running"}

@app.get("/vendor-insights/{vendor_name}")
async def vendor_insights(vendor_name: str):

    insights = get_vendor_insights(vendor_name)

    return insights

@app.get("/analytics")
async def analytics():

    data = get_system_analytics()

    return data


@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):

    document = save_uploaded_file(file)

    result = process_document(
        document["document_id"],
        document["filename"],
        document["file_path"]
    )

    return {
        "message": "Document uploaded and processed",
        "document_id": document["document_id"],
        "structured_data": result["structured_data"],
        "similar_documents": result["similar_documents"]
    }

@app.post("/ask-ai")
async def ask_ai(question: str):

    answer = ask_financial_assistant(question)

    return {
        "question": question,
        "answer": answer
    }