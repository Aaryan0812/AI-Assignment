"""
State definitions for RAG and SQL workflows
"""
from typing import TypedDict, Optional
from pydantic import BaseModel

# ============================================================
# State Definition 
# ============================================================
class RAGState(BaseModel):
    query: str = ""
    data_type: Optional[str] = None      # REQUIRED
    city: Optional[str] = None
    retrieved_chunks: Optional[list] = None
    final_answer: Optional[str] = None
    metadata: Optional[list] = None
 

