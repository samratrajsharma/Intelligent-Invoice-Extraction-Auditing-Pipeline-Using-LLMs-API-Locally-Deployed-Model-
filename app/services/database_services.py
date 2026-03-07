from app.config import SessionLocal
from app.models.document_model import Document


def save_document(document_id, filename, file_path, raw_text, structured_data):

    db = SessionLocal()

    doc = Document(
        id=document_id,
        filename=filename,
        file_path=file_path,
        raw_text=raw_text,
        vendor_name=structured_data.get("vendor_name"),
        invoice_date=structured_data.get("invoice_date"),
        total_amount=structured_data.get("total_amount"),
        document_type=structured_data.get("document_type")
    )

    db.add(doc)
    db.commit()
    db.close()