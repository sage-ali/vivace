import pytest
from tests import client


@pytest.mark.asyncio
async def test_modify_message():
    response = client.post(
        "/vivace", json={"message": "Tell me about RAG."})
    assert response.status_code == 200
    assert "message" in response.json()
