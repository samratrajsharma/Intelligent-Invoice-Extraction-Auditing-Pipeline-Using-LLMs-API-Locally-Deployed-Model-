import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = "vector_store.index"

dimension = 384

if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
else:
    index = faiss.IndexFlatL2(dimension)


def create_embedding(text):

    embedding = MODEL.encode([text])[0]

    return np.array([embedding]).astype("float32")


def store_embedding(text):

    vector = create_embedding(text)

    index.add(vector)

    vector_id = index.ntotal - 1

    faiss.write_index(index, INDEX_PATH)

    return vector_id


def search_similar(text, k=3):

    vector = create_embedding(text)

    distances, indices = index.search(vector, k)

    return distances, indices