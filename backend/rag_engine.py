import os
import google.generativeai as genai
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

class RAGEngine:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = self.pc.Index("neet-knowledge-base")
    
    def search(self, query: str, top_k=3):
        """Load model only when needed, then immediately clean up"""
        import gc
        from sentence_transformers import SentenceTransformer
        
        try:
            # Load model temporarily
            embedder = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Generate embedding
            query_embedding = embedder.encode(query).tolist()
            
            # Immediately delete model and free memory
            del embedder
            gc.collect()
            
            # Query Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            return results['matches']
        except Exception as e:
            print(f"Search error: {e}")
            # Fallback: return empty matches if search fails
            return []

    def generate_answer(self, query: str, context_matches):
        context_str = "\n\n".join([m['metadata']['text'] for m in context_matches])
        sources = [m['metadata']['source'] for m in context_matches]
        
        prompt = f"""You are a friendly NEET tutor. Answer the student's question using the NCERT content provided below.

=== NCERT Content ===
{context_str}
====================

Student's Question: {query}

INSTRUCTIONS:
1. Use the NCERT content above to answer the question
2. Explain in SIMPLE, everyday language (like talking to a friend)
3. Break down complex ideas into easy words
4. Use bullet points and short sentences
5. Give examples when helpful
6. If the exact answer isn't in the content but you can explain the concept from what's given, DO IT
7. ONLY say "I don't have information" if the content is completely unrelated to the question

Answer the question clearly and simply:"""
        
        response = self.model.generate_content(prompt)
        return {
            "answer": response.text,
            "sources": list(set(sources))
        }
