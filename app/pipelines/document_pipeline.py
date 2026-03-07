from app.services.text_extraction_service import extract_text
from app.services.llm_service import extract_document_fields
from app.services.document_classifier import classify_document
from app.services.risk_engine import calculate_risk
from app.services.database_service import save_document
from app.services.vector_service import store_embedding
from app.services.vector_mapping_service import save_vector_mapping
from app.services.search_service import search_similar_documents


def process_document(document_id, filename, file_path):

    # Extract text
    text = extract_text(file_path)

    # Classify document
    document_type = classify_document(text)

    # Extract fields using LLM
    structured_data = extract_document_fields(text)

    if not structured_data:
        structured_data = {}

    structured_data["document_type"] = document_type

    # Risk analysis
    risk_score, reasons = calculate_risk(structured_data)

    structured_data["risk_score"] = risk_score
    structured_data["risk_reasons"] = reasons

    # 🔎 Search similar documents BEFORE storing new embedding
    similar_docs = search_similar_documents(text)

    # Store embedding
    vector_id = store_embedding(text)

    # Map vector → document
    save_vector_mapping(vector_id, document_id)

    # Save document
    save_document(
        document_id,
        filename,
        file_path,
        text,
        structured_data
    )

    return {
        "structured_data": structured_data,
        "similar_documents": similar_docs
    }