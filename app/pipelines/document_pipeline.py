from app.services.text_extraction_service import extract_text
from app.services.llm_service import extract_document_fields
from app.services.database_services import save_document
from app.services.risk_engine import calculate_risk
from app.services.document_classifier import classify_document
from app.services.vector_service import store_embedding


def process_document(document_id, filename, file_path):

    text = extract_text(file_path)

    document_type = classify_document(text)

    structured_data = extract_document_fields(text)

    structured_data["document_type"] = document_type

    risk_score, reasons = calculate_risk(structured_data)

    structured_data["risk_score"] = risk_score
    structured_data["risk_reasons"] = reasons

    store_embedding(text)

    save_document(
        document_id,
        filename,
        file_path,
        text,
        structured_data
    )

    return {
        "structured_data": structured_data
    }