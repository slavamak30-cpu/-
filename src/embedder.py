import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
client = chromadb.PersistentClient(path="./chroma_db", settings=Settings(anonymized_telemetry=False))
collection = client.get_or_create_collection(name="docs")

def add_to_db(chunks, filename, doc_id):
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        collection.add(
            ids=[f"{doc_id}_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"source": filename, "doc_id": doc_id}]
        )

def search(query, k=8): 
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    return results['documents'][0], results['metadatas'][0]
