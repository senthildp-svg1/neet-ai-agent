from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from rag_engine import RAGEngine

load_dotenv()

app = FastAPI(title="NEET AI Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow ALL origins to fix CORS issues once and for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Engine
try:
    rag_engine = RAGEngine()
except Exception as e:
    print(f"Warning: RAG Engine failed to initialize. Check API keys. Error: {e}")
    rag_engine = None

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "NEET AI Agent Backend is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(request: ChatRequest):
    if not rag_engine:
        raise HTTPException(status_code=503, detail="RAG Engine not initialized")
    
    try:
        # 1. Retrieve context
        matches = rag_engine.search(request.message)
        
        # 2. Generate answer
        result = rag_engine.generate_answer(request.message, matches)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
