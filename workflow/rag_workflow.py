"""
Main RAG workflow implementation
"""
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from workflow.state_definitions import RAGState
from workflow.orchestration_agent import orchestration_logic
from workflow.search_handler import hybrid_search_logic
from workflow.summary_handler import summary_logic
from workflow.weather_api_handler import weather_api
import os
from dotenv import load_dotenv
load_dotenv(override=True) 


def orchestration_agent(state: RAGState):
    """Wrapper for orchestration decision"""
    print("🔹 [orchestration_agent] Called")
    result = orchestration_logic(state.query)   # FIXED
    print("[orchestration_agent] output", result)
    return result


def pdf_handler(state: RAGState):
    """Wrapper for hybrid search / PDF RAG"""
    print("🔹 [pdf_handler] Called")
    result = hybrid_search_logic(
        state.query
    )
    return {"retrieved_chunks": result}


def weather_handler(state: RAGState):
    """Wrapper for Weather API"""
    print("🔹 [weather_handler] Called")

    api_key = os.getenv("weather_secret")

    result = weather_api(
        state.query,
        state.city,     # FIXED
        api_key
    )
    return {"retrieved_chunks": result}


def llm_summary_handler(state: RAGState):
    """Wrapper for LLM Summary"""
    print("🔹 [llm_summary_handler] Called")

    result = summary_logic(
        chunks=state.retrieved_chunks or [],   # FIXED
        query=state.query                      # FIXED
    )

    return {
        "final_answer": result.get("summary"),
        "metadata": result.get("metadata", [])
    }


def rag_app_builder():
    """Build and compile the main RAG workflow"""
    workflow = StateGraph(RAGState)

    # Add nodes
    workflow.add_node("orchestration_agent", orchestration_agent)
    workflow.add_node("pdf_handler", pdf_handler)
    workflow.add_node("weather_handler", weather_handler)
    workflow.add_node("llm_summary_handler", llm_summary_handler)

    # Entry point
    workflow.set_entry_point("orchestration_agent")

    # Conditional edge routing (FIXED)
    workflow.add_conditional_edges(
        "orchestration_agent",
        lambda state: "weather" if state.data_type == "weather" else "pdf",   # FIXED
        {
            "weather": "weather_handler",
            "pdf": "pdf_handler",
        },
    )

    # Edges
    workflow.add_edge("pdf_handler", "llm_summary_handler")
    workflow.add_edge("weather_handler", "llm_summary_handler")
    workflow.add_edge("llm_summary_handler", END)

    return workflow.compile()



def rag_agent_orchestrator(query: str):
    """
    Main orchestrator for the RAG pipeline.
    Supports:
        - Weather queries
        - Finance (PDF) queries
    """

    print("🚀 [rag_agent_orchestrator] Starting RAG/Weather workflow")

    # Build workflow
    app = rag_app_builder()

    # Initial state
    initial_state = {
        "query": query
    }

    print("🟦 Initial State:", initial_state)

    # Run graph
    state = app.invoke(initial_state)

    print("📦 Final State After Pipeline:", state)

    final_output = {
        "summary": state.get("final_answer", "No summary found."),
        "metadata": state.get("metadata", [])
    }

    print("✅ Final Output:", final_output)

    return final_output
