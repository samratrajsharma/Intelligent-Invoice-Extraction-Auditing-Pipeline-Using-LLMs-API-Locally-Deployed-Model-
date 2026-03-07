from app.config import SessionLocal
from app.models.document_model import Document


def calculate_risk(structured_data):

    risk_score = 0
    reasons = []

    vendor = structured_data.get("vendor_name")
    amount = structured_data.get("total_amount")
    date = structured_data.get("invoice_date")

    # Missing field check
    if not vendor:
        risk_score += 20
        reasons.append("Missing vendor")

    if not amount:
        risk_score += 20
        reasons.append("Missing amount")

    # Suspicious amount
    try:
        amount_value = float(amount.replace("Rs.", "").replace(",", ""))
        if amount_value > 100000:
            risk_score += 30
            reasons.append("Unusually high amount")
    except:
        pass

    # Duplicate detection
    db = SessionLocal()

    duplicate = db.query(Document).filter(
        Document.vendor_name == vendor,
        Document.total_amount == amount,
        Document.invoice_date == date
    ).first()

    db.close()

    if duplicate:
        risk_score += 40
        reasons.append("Possible duplicate invoice")

    return risk_score, reasons