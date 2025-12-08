import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "neet-knowledge-base"
index = pc.Index(index_name)

print("=" * 70)
print("📊 NEET AI Agent - Pinecone Index Statistics")
print("=" * 70)

# Get index stats
stats = index.describe_index_stats()

print(f"\n📈 Index Overview:")
print(f"   Total vectors: {stats.total_vector_count}")
print(f"   Dimension: {stats.dimension}")

# Query to get sample vectors and their sources
print(f"\n🔍 Sample vectors by source:")

# Check for specific physics files
physics_sources = [
    "physics_class11_part1.pdf",
    "physics_class11_part2.pdf", 
    "physics_class12_part1.pdf",
    "physics_class12_part2.pdf"
]

for source in physics_sources:
    # Try to query using metadata filter
    try:
        result = index.query(
            vector=[0.0] * 768,  # Dummy vector
            filter={"source": source},
            top_k=1,
            include_metadata=True
        )
        if result.matches:
            print(f"   ✅ {source}: Found in index")
        else:
            print(f"   ❌ {source}: NOT found in index")
    except Exception as e:
        print(f"   ⚠️  {source}: Error checking - {e}")

print("=" * 70)
