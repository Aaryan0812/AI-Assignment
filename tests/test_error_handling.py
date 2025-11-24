from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_rag_query_invalid():
    payload = {"query": ""}  # Invalid query

    response = client.post("/rag/query", json=payload)
    data = response.json()

    # Should not crash
    assert response.status_code == 200
    assert "error" in data or "result" in data
