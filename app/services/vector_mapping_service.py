from app.config import SessionLocal
from app.models.vector_model import VectorMapping


def save_vector_mapping(vector_id, document_id):

    db = SessionLocal()

    mapping = VectorMapping(
        vector_id=vector_id,
        document_id=document_id
    )

    db.add(mapping)
    db.commit()
    db.close()