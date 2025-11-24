from workflow.rag_workflow import rag_agent_orchestrator

def test_rag_orchestrator_response():
    query = "temperature in Indore"

    result = rag_agent_orchestrator(query)

    # Basic checks
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0
