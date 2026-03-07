from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, File
from app.services.document_service import save_uploaded_file

app = FastAPI(
    title="AI Financial Operations Platform",
    description="AI-powered document intelligence and financial risk system",
    version="1.0"
)

@app.get("/")
def root():
    return {"message": "AI FinOps Platform Running"}

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):

    document = save_uploaded_file(file)

    return {
        "message": "Document uploaded successfully",
        "document_id": document["document_id"],
        "file_path": document["file_path"]
    }