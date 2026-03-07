import os
import uuid
from pathlib import Path

UPLOAD_FOLDER = "data/invoices"

Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)


def save_uploaded_file(file):

    file_extension = file.filename.split(".")[-1]

    document_id = str(uuid.uuid4())

    filename = f"{document_id}.{file_extension}"

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return {
        "document_id": document_id,
        "file_path": file_path,
        "filename": filename
    }