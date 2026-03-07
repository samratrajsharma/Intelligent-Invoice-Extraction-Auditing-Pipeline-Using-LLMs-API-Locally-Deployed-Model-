from sqlalchemy import Column, Integer, String
from app.config import Base


class VectorMapping(Base):

    __tablename__ = "vector_mappings"

    id = Column(Integer, primary_key=True, index=True)
    vector_id = Column(Integer)
    document_id = Column(String)