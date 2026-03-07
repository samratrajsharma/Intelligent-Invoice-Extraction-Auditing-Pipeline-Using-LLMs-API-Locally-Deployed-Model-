from app.config import SessionLocal
from app.models.document_model import Document
from sqlalchemy import func
from sqlalchemy import func, Float

def get_system_analytics():

    db = SessionLocal()

    total_documents = db.query(Document).count()

    high_risk_docs = db.query(Document).filter(
        Document.risk_score != "0"
    ).count()

    vendor_spending = db.query(
        Document.vendor_name,
        func.sum(func.cast(Document.total_amount, Float))
    ).group_by(Document.vendor_name).all()

    db.close()

    vendors = []

    for vendor in vendor_spending:
        vendors.append({
            "vendor": vendor[0],
            "total_spent": float(vendor[1]) if vendor[1] else 0
        })

    return {
        "total_documents": total_documents,
        "high_risk_documents": high_risk_docs,
        "vendor_spending": vendors
    }