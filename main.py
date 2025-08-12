import os
import fitz
import faiss
import numpy as np
import pickle
import requests
from sentence_transformers import SentenceTransformer

PDF_DIR = "pdfs"
CHUNK_SIZE = 500
EMBED_DIR = "embeddings"
INDEX_PATH = os.path.join(EMBED_DIR, "index.faiss")
CHUNKS_PATH = os.path.join(EMBED_DIR, "chunks.pkl")

def extract_text_from_pdfs(pdf_dir):
    all_text = ""
    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            path = os.path.join(pdf_dir, file)
            doc = fitz.open(path)
            for page in doc:
                all_text += page.get_text() + "\n"
    return all_text

def chunk_text(text, chunk_size=CHUNK_SIZE):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def build_faiss_index(chunks, model):
    embeddings = model.encode(chunks)
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index

def search_context(index, chunks, query, model, top_k=5):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), top_k)
    return [chunks[i] for i in I[0]]

def generate_answer(context, question):
    prompt = f"""
Responda APENAS com base no contexto abaixo. NÃO invente informações.

Contexto:
{context}

Pergunta: {question}
Resposta:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    return response.json().get('response', 'Erro: resposta não recebida da API.')

def load_index_and_model():
    index = faiss.read_index(INDEX_PATH)
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return index, chunks, model
