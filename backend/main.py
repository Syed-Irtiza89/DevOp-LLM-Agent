try:
    from agent import get_qa_chain, initialize_vector_db
except ImportError:
    from .agent import get_qa_chain, initialize_vector_db
import os

# Ensure data directory exists for local preview
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)
    with open(os.path.join(DATA_PATH, "intro.md"), "w") as f:
        f.write("# Welcome\nThis is your DevOps Knowledge base.")

app = FastAPI(title="DevOps LLM Agent API")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: list

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest):
    try:
        qa_chain = get_qa_chain()
        result = qa_chain({"query": request.query})
        
        sources = [doc.metadata.get("source", "unknown") for doc in result["source_documents"]]
        
        return {
            "answer": result["result"],
            "sources": list(set(sources))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def ingest():
    """Trigger document re-indexing."""
    try:
        initialize_vector_db()
        return {"message": "Knowledge base updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
