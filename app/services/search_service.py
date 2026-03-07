from app.services.vector_service import search_similar
from app.config import SessionLocal
from app.models.vector_model import VectorMapping
from app.models.document_model import Document


def search_similar_documents(query_text, top_k=3):

    distances, indices = search_similar(query_text, top_k)

    db = SessionLocal()

    results = []

    for vector_id in indices[0]:

        mapping = db.query(VectorMapping).filter(
            VectorMapping.vector_id == int(vector_id)
        ).first()

        if mapping:

            doc = db.query(Document).filter(
                Document.id == mapping.document_id
            ).first()

            if doc:
                results.append({
                    "document_id": doc.id,
                    "vendor": doc.vendor_name,
                    "date": doc.invoice_date,
                    "amount": doc.total_amount,
                    "document_type": doc.document_type
                })

    db.close()

    return results