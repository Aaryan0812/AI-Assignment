from fastapi import FastAPI
from pydantic import BaseModel
from workflow.rag_workflow import rag_agent_orchestrator

app = FastAPI(title="RAG Agent API")

class QueryRequest(BaseModel):
    query: str

@app.post("/rag/query")
async def rag_query(request: QueryRequest):
    """
    API that calls the RAG pipeline with a user query.
    """
    try:
        response = rag_agent_orchestrator(request.query)
        return {"query": request.query, "result": response}
    except Exception as e:
        return {"error": str(e)}
