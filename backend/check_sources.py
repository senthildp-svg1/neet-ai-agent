import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "neet-knowledge-base"
index = pc.Index(index_name)

print("=" * 70)
print("📊 NEET AI Agent - What's Actually in the Index")
print("=" * 70)

# Get index stats
stats = index.describe_index_stats()

print(f"\n📈 Index Overview:")
print(f"   Total vectors: {stats.total_vector_count}")
print(f"   Dimension: {stats.dimension}")

# Query to get sample vectors and check their sources
print(f"\n🔍 Querying sample vectors to identify sources:")

# Do a broad query to get any vectors
result = index.query(
    vector=[0.0] * 768,  # Dummy vector
    top_k=20,  # Get more samples
    include_metadata=True
)

# Collect unique sources
sources = set()
for match in result.matches:
    if 'metadata' in match and 'source' in match.metadata:
        sources.add(match.metadata['source'])

print(f"\n📚 Found {len(sources)} unique sources:")
for source in sorted(sources):
    # Count how many vectors for each source
    try:
        count_result = index.query(
            vector=[0.0] * 768,
            filter={"source": source},
            top_k=1,
            include_metadata=True
        )
        print(f"   • {source}")
    except:
        print(f"   • {source}")

print("=" * 70)
