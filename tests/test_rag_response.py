import pytest
from logic.services.rag_response import generate_response


def test_generate_response():
    query = "What is RAG?"
    similar_docs = [
        "RAG stands for Retrieval-Augmented Generation.",
        "It is a method to improve the quality of generated responses."
    ]

    response = generate_response(query, similar_docs,
                                       "https://aws.amazon.com/what-is/retrieval-augmented-generation/", 500)
    assert isinstance(response, str)
    assert "RAG" in response
