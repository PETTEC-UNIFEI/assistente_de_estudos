import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from main import extract_text_from_pdfs, chunk_text, build_faiss_index

model = SentenceTransformer('all-MiniLM-L6-v2')

print("Extraindo texto dos PDFs...")
text = extract_text_from_pdfs("pdfs")
chunks = chunk_text(text)
print("Texto extraído:\n", text[:1000])  # mostra os 1000 primeiros caracteres


print("Construindo índice FAISS com embeddings...")
index = build_faiss_index(chunks, model)

os.makedirs("embeddings", exist_ok=True)
faiss.write_index(index, "embeddings/index.faiss")
with open("embeddings/chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("Indexação concluída com sucesso.")
