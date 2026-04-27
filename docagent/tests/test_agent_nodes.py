import pytest
from unittest.mock import patch, MagicMock
from docagent.agent.nodes import route_node, generate_node
from docagent.agent.state import AgentState

def test_route_node_code():
    """Test that code content routes to api_doc."""
    state = AgentState(
        content="def hello(): pass",
        content_type="code",
        document_type=None,
        generated_document=None,
        error=None
    )

    with patch('docagent.agent.nodes.llm') as mock_llm:
        mock_response = MagicMock()
        mock_response.content = "code"
        mock_llm.invoke.return_value = mock_response

        result = route_node(state)
        assert result["document_type"] == "api_doc"

def test_route_node_markdown():
    """Test that markdown content routes to readme."""
    state = AgentState(
        content="# Hello",
        content_type="markdown",
        document_type=None,
        generated_document=None,
        error=None
    )

    with patch('docagent.agent.nodes.llm') as mock_llm:
        mock_response = MagicMock()
        mock_response.content = "markdown"
        mock_llm.invoke.return_value = mock_response

        result = route_node(state)
        assert result["document_type"] == "readme"

def test_generate_node():
    """Test that generate_node produces document content."""
    state = AgentState(
        content="def hello(): pass",
        content_type="code",
        document_type="api_doc",
        generated_document=None,
        error=None
    )

    with patch('docagent.agent.nodes.llm') as mock_llm:
        mock_response = MagicMock()
        mock_response.content = "# API Documentation\n\nThis is an API doc."
        mock_llm.invoke.return_value = mock_response

        result = generate_node(state)
        assert "API" in result["generated_document"] or "api" in result["generated_document"].lower()

def test_generate_node_missing_document_type():
    """Test that missing document_type raises ValueError."""
    state = AgentState(
        content="def hello(): pass",
        content_type="code",
        document_type=None,
        generated_document=None,
        error=None
    )

    with pytest.raises(ValueError, match="document_type is required"):
        generate_node(state)

def test_route_node_error_handling():
    """Test that route_node raises RuntimeError on LLM failure."""
    state = AgentState(
        content="def hello(): pass",
        content_type="code",
        document_type=None,
        generated_document=None,
        error=None
    )

    with patch('docagent.agent.nodes.llm') as mock_llm:
        mock_llm.invoke.side_effect = Exception("API Error")

        with pytest.raises(RuntimeError, match="Failed to route content"):
            route_node(state)