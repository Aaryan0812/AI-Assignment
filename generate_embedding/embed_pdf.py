import sys
import os
import uuid
from datetime import datetime

# Make project root visible
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utilities.create_llm_client import get_embedding  # your embedding function

import fitz  # PyMuPDF for reliable text extraction
from azure.identity import ClientSecretCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SemanticSearch,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile
)

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------
TENANT_ID = os.getenv("tenant_id")
CLIENT_ID = os.getenv("client_id")
CLIENT_SECRET = os.getenv("client_secret")

SEARCH_ENDPOINT = os.getenv("azure_search_endpoint")
INDEX_NAME = "testonepdf"

PDF_PATH = r"generate_embedding\Sample-Financial-Statements-1.pdf"

EMBED_DIM = 1536           # ada-002 dimension
CHUNK_SIZE = 800
CHUNK_OVERLAP = 200

# -------------------------------------------------------
# CLIENTS
# -------------------------------------------------------
credential = ClientSecretCredential(
    tenant_id=TENANT_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

index_client = SearchIndexClient(endpoint=SEARCH_ENDPOINT, credential=credential)
search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=INDEX_NAME, credential=credential)


# ============================================================
# CREATE/UPDATE AI SEARCH INDEX
# ============================================================
def create_search_index():
    print("\n=== Creating/Updating AI Search Index ===")

    fields = [
        SearchField(name="chunk_id", type=SearchFieldDataType.String, key=True, filterable=True),
        SearchField(name="source_system", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SearchField(name="subfolder", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SearchField(name="file_name", type=SearchFieldDataType.String, searchable=True, filterable=True),
        SearchField(name="file_path", type=SearchFieldDataType.String, filterable=True),
        SearchField(name="file_extension", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SearchField(name="last_modified", type=SearchFieldDataType.String, filterable=True, sortable=True),
        SearchField(name="chunk_index", type=SearchFieldDataType.Int32, filterable=True, sortable=True),
        SearchField(name="total_chunks", type=SearchFieldDataType.Int32, filterable=True),
        SearchField(name="chunk_text", type=SearchFieldDataType.String, searchable=True),
        SearchField(name="chunk_size", type=SearchFieldDataType.Int32, filterable=True),

        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=EMBED_DIM,
            vector_search_profile_name="embedding-profile"
        ),
    ]

    # Vector Search
    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="hnsw-config")],
        profiles=[VectorSearchProfile(name="embedding-profile", algorithm_configuration_name="hnsw-config")]
    )

    # Semantic Search
    semantic_fields = SemanticPrioritizedFields(
        title_field=SemanticField(field_name="file_name"),
        content_fields=[SemanticField(field_name="chunk_text")]
    )

    semantic_config = SemanticConfiguration(
        name="semantic-config",
        prioritized_fields=semantic_fields
    )

    semantic_search = SemanticSearch(configurations=[semantic_config])

    index = SearchIndex(
        name=INDEX_NAME,
        fields=fields,
        vector_search=vector_search,
        semantic_search=semantic_search
    )

    try:
        index_client.delete_index(INDEX_NAME)
        print("Old index deleted.")
    except:
        pass

    index_client.create_index(index)
    print(f"✔ Index '{INDEX_NAME}' created successfully.")


# ============================================================
# PDF → TEXT → CHUNKS
# ============================================================
def extract_pdf_text(pdf_path):
    """
    Use PyMuPDF for robust text extraction.
    """
    doc = fitz.open(pdf_path)
    extracted = ""

    for page in doc:
        extracted += page.get_text("text") + "\n"

    return extracted.strip()


def chunk_text(text):
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + CHUNK_SIZE, length)
        chunks.append(text[start:end])
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def extract_pdf_chunks(pdf_path):
    text = extract_pdf_text(pdf_path)

    if not text:
        print("⚠️ WARNING: PDF contains no extractable text (likely scanned).")
        return []

    all_chunks = []
    file_name = os.path.basename(pdf_path)
    chunks = chunk_text(text)
    total_chunks = len(chunks)
    now = datetime.utcnow().isoformat()

    for idx, chunk in enumerate(chunks, start=1):
        all_chunks.append({
            "chunk_id": str(uuid.uuid4()),
            "source_system": "local-pdf",
            "subfolder": "",
            "file_name": file_name,
            "file_path": pdf_path,
            "file_extension": ".pdf",
            "last_modified": now,
            "chunk_index": idx,
            "total_chunks": total_chunks,
            "chunk_text": chunk,
            "chunk_size": len(chunk),
        })

    return all_chunks


# ============================================================
# GENERATE EMBEDDINGS + UPLOAD
# ============================================================
def upload_to_search():
    chunks = extract_pdf_chunks(PDF_PATH)

    print(f"Extracted {len(chunks)} chunks… generating embeddings…")

    enriched = []
    for doc in chunks:
        doc["embedding"] = get_embedding(doc["chunk_text"])
        enriched.append(doc)

    print("Uploading to Azure Search…")
    result = search_client.upload_documents(enriched)

    print("Upload result:", result)
    print("✔ Upload completed.")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    create_search_index()
    upload_to_search()
    print("\n🎉 PDF processed, chunked, embedded and indexed successfully!")
