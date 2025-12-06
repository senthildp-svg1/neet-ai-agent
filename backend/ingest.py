import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import time

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "neet-knowledge-base"

# Create index if not exists
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384, # Dimension for all-MiniLM-L6-v2
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(index_name)
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def chunk_text(text, chunk_size=500):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

def ingest_file(file_path):
    print(f"Processing {file_path}...")
    text = load_text(file_path)
    chunks = chunk_text(text)
    
    vectors = []
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        # Create a unique ID for each chunk
        chunk_id = f"{os.path.basename(file_path)}_{i}"
        vectors.append({
            "id": chunk_id,
            "values": embedding,
            "metadata": {"text": chunk, "source": os.path.basename(file_path)}
        })
    
    # Batch upsert
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i+batch_size]
        index.upsert(vectors=batch)
    
    print(f"Uploaded {len(vectors)} chunks to Pinecone.")

if __name__ == "__main__":
    # Example usage
    data_dir = "data"
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith(".txt"):
                ingest_file(os.path.join(data_dir, file))
    else:
        print("Data directory not found.")
