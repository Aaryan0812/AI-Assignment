from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery, QueryType
from typing import List, Dict, Any
from utilities.create_llm_client import get_embedding
from utilities.search_client import get_search_client
from azure.search.documents.models import VectorizedQuery


def hybrid_search_logic(query: str) -> List[Dict[str, Any]]:
    """
    Perform hybrid (vector + keyword) search on Azure AI Search
    for the simplified index that contains only:
    - chunk_id
    - file_name
    - content
    - file_path
    """

    print(f"🔹 [hybrid_search_logic] Running hybrid search for query: '{query}'")

    # ============================================================
    # Step 1: Embed the query
    # ============================================================
    try:
        embedding_vector = get_embedding(query)
    except Exception as e:
        print(f"⚠️ [hybrid_search_logic] Embedding failed: {e}")
        return []

    # ============================================================
    # Step 2: Create vectorized query
    # ============================================================
    vector_query = VectorizedQuery(
        vector=embedding_vector,
        k_nearest_neighbors=20,
        fields="embedding"
    )

    # ============================================================
    # Step 3: Execute hybrid search (vector + keyword)
    # ============================================================
    search_client = get_search_client()

    try:
        results = search_client.search(
            search_text=query,           # keyword part
            vector_queries=[vector_query],  # semantic part
            top=5,
            select=["chunk_id", "file_name", "chunk_text", "file_path"]
        )
    except Exception as e:
        print(f"❌ [hybrid_search_logic] Search failed: {e}")
        return []

    # ============================================================
    # Step 4: Collect top chunks
    # ============================================================
    chunks = []
    for r in results:
        chunks.append({
            "chunk_id": r.get("chunk_id"),
            "file_name": r.get("file_name"),
            "content": r.get("chunk_text"),
            "file_path": r.get("file_path"),
        })

    print(f"✅ [hybrid_search_logic] Retrieved {len(chunks)} chunks")
    return chunks


