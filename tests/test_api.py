from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_rag_query_api():
    payload = {"query": "temperature in Indore"}
    response = client.post("/rag/query", json=payload)

    # Status check
    assert response.status_code == 200
    
    data = response.json()
    assert "result" in data or "error" in data
    assert data["query"] == payload["query"]
