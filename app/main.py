from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, File
from app.services.document_service import save_uploaded_file
from app.pipelines.document_pipeline import process_document
from app.config import engine, Base
from app.models.document_model import Document

app = FastAPI(
    title="AI Financial Operations Platform",
    description="AI-powered document intelligence and financial risk system",
    version="1.0"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "AI FinOps Platform Running"}

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
        "structured_data": result["structured_data"]
    }