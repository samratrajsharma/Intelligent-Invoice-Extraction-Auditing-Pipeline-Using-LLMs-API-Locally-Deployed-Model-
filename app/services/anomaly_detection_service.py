from app.config import SessionLocal
from app.models.document_model import Document
from sqlalchemy import func, Float


def detect_amount_anomaly(vendor_name, amount):

    db = SessionLocal()

    avg_amount = db.query(
        func.avg(func.cast(Document.total_amount, Float))
    ).filter(
        Document.vendor_name == vendor_name
    ).scalar()

    db.close()

    if not avg_amount:
        return False, None

    try:
        amount = float(amount)
    except:
        return False, avg_amount

    if amount > (3 * avg_amount):
        return True, avg_amount

    return False, avg_amount