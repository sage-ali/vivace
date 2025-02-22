import pytest
from logic.services.rag_response import generate_response


def test_generate_response():
    """
    Tests the generate_response function.

    Given a query and a knowledge base URL, the function should return a response
    string that contains the query term and is a non-empty string.

    """

    query = "What is RAG?"
    knowledge_base_url = (
        "https://aws.amazon.com/what-is/retrieval-augmented-generation/"
    )

    response = generate_response(query, knowledge_base_url)
    assert isinstance(response, str)
    assert "RAG" in response
