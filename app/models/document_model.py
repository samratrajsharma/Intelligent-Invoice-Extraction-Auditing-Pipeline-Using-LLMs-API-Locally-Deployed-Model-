from sqlalchemy import Column, String, Text
from app.config import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String)
    file_path = Column(String)

    raw_text = Column(Text)

    vendor_name = Column(String)
    invoice_date = Column(String)
    total_amount = Column(String)
    document_type = Column(String)
    risk_score = Column(String)
    risk_reasons = Column(Text)