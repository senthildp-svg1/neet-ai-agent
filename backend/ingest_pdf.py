import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "neet-knowledge-base"
index = pc.Index(index_name)
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"❌ Error reading PDF {pdf_path}: {e}")
        return ""

def load_text(file_path):
    """Load text from .txt file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def chunk_text(text, chunk_size=700):
    """Split text into chunks of specified size"""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

def ingest_file(file_path):
    """Ingest either PDF or TXT file into Pinecone"""
    print(f"\n📄 Processing {os.path.basename(file_path)}...")
    
    # Extract text based on file type
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.txt'):
        text = load_text(file_path)
    else:
        print(f"⚠️  Skipping unsupported file type: {file_path}")
        return
    
    if not text.strip():
        print(f"⚠️  No text extracted from {os.path.basename(file_path)}")
        return
    
    chunks = chunk_text(text)
    
    vectors = []
    for i, chunk in enumerate(chunks):
        if chunk.strip():  # Skip empty chunks
            embedding = model.encode(chunk).tolist()
            chunk_id = f"{os.path.basename(file_path).replace('.', '_')}_{i}"
            vectors.append({
                "id": chunk_id,
                "values": embedding,
                "metadata": {
                    "text": chunk,
                    "source": os.path.basename(file_path),
                    "chunk_index": i
                }
            })
    
    # Batch upsert
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i+batch_size]
        index.upsert(vectors=batch)
    
    print(f"✅ Uploaded {len(vectors)} chunks from {os.path.basename(file_path)}")
    return len(vectors)

def find_all_files(directory, extensions=('.txt', '.pdf')):
    """Recursively find all files with given extensions"""
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extensions):
                files.append(os.path.join(root, filename))
    return files

def get_index_stats():
    """Get current Pinecone index statistics"""
    stats = index.describe_index_stats()
    return stats

if __name__ == "__main__":
    print("=" * 70)
    print("🎓 NEET AI Agent - NCERT Content Ingestion (Recursive)")
    print("=" * 70)
    
    # Show current stats
    print("\n📊 Current Index Statistics:")
    stats = get_index_stats()
    print(f"   Total vectors: {stats.total_vector_count}")
    print(f"   Dimension: {stats.dimension}")
    
    # Process all files in data directory (including subdirectories)
    data_dir = "data"
    if os.path.exists(data_dir):
        files = find_all_files(data_dir)
        
        if not files:
            print(f"\n⚠️  No .txt or .pdf files found in {data_dir}/")
            print("\n📥 To add NCERT content:")
            print("   1. Download NCERT PDFs from https://ncert.nic.in/textbook.php")
            print(f"   2. Place them in the '{data_dir}/' directory")
            print("   3. Run this script again: python ingest_pdf.py")
        else:
            print(f"\n📚 Found {len(files)} file(s) to process:")
            for f in files[:10]:  # Show first 10
                print(f"   - {os.path.relpath(f, data_dir)}")
            if len(files) > 10:
                print(f"   ... and {len(files) - 10} more files")
            
            print("\n🔄 Starting ingestion...")
            total_chunks = 0
            for file in files:
                chunks = ingest_file(file)
                if chunks:
                    total_chunks += chunks
            
            # Show updated stats
            print("\n" + "=" * 70)
            print(f"📊 Ingestion Summary:")
            print(f"   Files processed: {len(files)}")
            print(f"   Total chunks added: {total_chunks}")
            stats = get_index_stats()
            print(f"   Total vectors in index: {stats.total_vector_count}")
            print("=" * 70)
            print("\n✅ Ingestion complete!")
    else:
        print(f"❌ Data directory '{data_dir}/' not found.")
        print(f"   Creating directory now...")
        os.makedirs(data_dir)
        print(f"✅ Directory created. Please add NCERT PDFs and run again.")
