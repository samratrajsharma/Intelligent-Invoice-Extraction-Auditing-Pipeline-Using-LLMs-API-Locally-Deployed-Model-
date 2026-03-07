from app.services.search_service import search_similar_documents
from app.services.llm_service import call_llm


def ask_financial_assistant(question):

    # Retrieve relevant documents using vector search
    similar_docs = search_similar_documents(question, top_k=5)

    context = ""

    for doc in similar_docs:
        context += f"""
Vendor: {doc['vendor']}
Date: {doc['date']}
Amount: {doc['amount']}
Type: {doc['document_type']}
"""

    prompt = f"""
You are a financial document assistant.

Use the following document data to answer the user's question.

Documents:
{context}

Question:
{question}

Answer clearly and concisely.
"""

    response = call_llm(prompt)

    return response