from app.services.text_extraction_service import extract_text
from app.services.llm_service import extract_document_fields
from app.services.database_services import save_document


def process_document(document_id, filename, file_path):

    text = extract_text(file_path)

    structured_data = extract_document_fields(text)

    save_document(
        document_id,
        filename,
        file_path,
        text,
        structured_data
    )

    return {
        "raw_text": text,
        "structured_data": structured_data
    }