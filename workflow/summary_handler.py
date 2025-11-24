from typing import List
from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import StrOutputParser
from utilities.create_llm_client import create_llm_client 

# ============================================================
# LLM Summary Logic
# ============================================================
def summary_logic(chunks: List[dict], query: str = None):
    """
    Generate a summary using the retrieved chunks.
    Works for:
    - Weather API chunks
    - Finance RAG chunks
    - SQL agent chunks
    """

    print(f"[summary_handler] Summarizing {len(chunks)} chunks")

    if not chunks:
        return {
            "summary": "No relevant information was found for your query.",
            "metadata": []
        }

    # ============================================================
    # Step 1: Create LLM Client
    # ============================================================
    llm = create_llm_client()

    # ============================================================
    # Step 2: Build context from retrieved chunks
    # ============================================================
    context = "\n\n".join(
        [f"Document {i+1}:\n{chunk.get('content', '')}" for i, chunk in enumerate(chunks)]
    )

    # ============================================================
    # Step 3: Build metadata
    # ============================================================
    seen = set()
    metadata = []

    for chunk in chunks:
        fname = chunk.get("file_name", "unknown")
        if fname not in seen:
            seen.add(fname)
            metadata.append({
                "chunk_id": chunk.get("chunk_id", ""),
                "file_name": fname,
                "file_path": chunk.get("file_path", ""),
            })

    # ============================================================
    # Step 4: Define the prompt
    # ============================================================
    prompt = PromptTemplate.from_template("""
You are a helpful AI assistant who summarizes information only from the provided context.

**Your Task:**
1. Read all document chunks.
2. Combine the information to answer the query.
3. Keep the answer factual, concise (150–250 words), and well structured.

**User Query:** {query}

**Context:**
{context}

**Rules:**
- Do NOT use external knowledge.
- If the context is insufficient, explicitly say so.
""")

    # ============================================================
    # Step 5: Build chain
    # ============================================================
    chain = prompt | llm | StrOutputParser()

    # ============================================================
    # Step 6: Execute summarization
    # ============================================================
    try:
        response = chain.invoke({
            "query": query or "N/A",
            "context": context
        })

        print("✅ [summary_handler] Successfully generated summary.")

        return {
            "summary": response,
            "metadata": metadata
        }

    except Exception as e:
        print(f"❌ [summary_handler] LLM summarization failed: {e}")
        return {
            "summary": "An error occurred during summarization.",
            "metadata": metadata
        }

