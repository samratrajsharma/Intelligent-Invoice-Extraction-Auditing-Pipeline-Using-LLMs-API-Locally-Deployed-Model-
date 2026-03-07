from app.config import SessionLocal
from app.models.document_model import Document
from sqlalchemy import func, Float


def get_vendor_insights(vendor_name):

    db = SessionLocal()

    invoices = db.query(Document).filter(
        Document.vendor_name == vendor_name
    )

    total_invoices = invoices.count()

    total_spent = db.query(
        func.sum(func.cast(Document.total_amount, Float))
    ).filter(
        Document.vendor_name == vendor_name
    ).scalar()

    average_invoice = db.query(
        func.avg(func.cast(Document.total_amount, Float))
    ).filter(
        Document.vendor_name == vendor_name
    ).scalar()

    risk_documents = invoices.filter(
        Document.risk_score != "0"
    ).count()

    first_invoice = invoices.order_by(Document.invoice_date.asc()).first()
    last_invoice = invoices.order_by(Document.invoice_date.desc()).first()

    db.close()

    return {
        "vendor": vendor_name,
        "total_invoices": total_invoices,
        "total_spent": float(total_spent) if total_spent else 0,
        "average_invoice": float(average_invoice) if average_invoice else 0,
        "risk_documents": risk_documents,
        "first_seen": first_invoice.invoice_date if first_invoice else None,
        "last_seen": last_invoice.invoice_date if last_invoice else None
    }