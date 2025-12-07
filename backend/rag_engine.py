import os
import google.generativeai as genai
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

class RAGEngine:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        # Configure safety settings to avoid blocking educational content
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
        ]
        # Use gemini-1.5-flash for better stability and free tier limits
        self.model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
        
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = self.pc.Index("neet-knowledge-base")
    
    def search(self, query: str, top_k=3):
        """Use Gemini's embedding API (768 dims) to save memory"""
        try:
            # Use Gemini's embedding model (no local memory needed!)
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=query,
                task_type="retrieval_query"
            )
            query_embedding = result['embedding']
            
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            return results['matches']
        except Exception as e:
            print(f"Search error: {e}")
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
        
        try:
            response = self.model.generate_content(prompt)
            return {
                "answer": response.text,
                "sources": list(set(sources))
            }
        except Exception as e:
            print(f"Generation error: {e}")
            return {
                "answer": "I'm sorry, I couldn't generate an answer due to safety filters or an API error. Please try rephrasing your question.",
                "sources": []
            }
