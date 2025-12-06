from rag_engine import RAGEngine

# Test search functionality
rag = RAGEngine()

# Test query
query = "kinetic energy"
print(f"Searching for: '{query}'")
print("-" * 60)

# Get search results
results = rag.search(query, top_k=5)

if results:
    print(f"\nFound {len(results)} results:\n")
    for i, result in enumerate(results, 1):
        score = result.get('score', 0)
        source = result.get('metadata', {}).get('source', 'Unknown')
        text = result.get('metadata', {}).get('text', '')[:150]
        
        print(f"{i}. Score: {score:.4f}")
        print(f"   Source: {source}")
        print(f"   Text: {text}...")
        print()
else:
    print("No results found!")
