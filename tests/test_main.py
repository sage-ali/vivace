import pytest
from tests import client


@pytest.mark.asyncio
async def test_modify_message(client):
    """
    Tests the /api/vivace endpoint.

    Sends a POST request to the endpoint with a valid JSON body containing a
    channel_id, settings, and message. The response should have a 200 status code
    and should contain the modified message.
    """
    response = client.post(
        "/api/vivace",
        json={
            "channel_id": "0192dd70-cdf1-7e15-8776-4fee4a78405e",
            "settings": [
                {
                    "label": "Knowledge Base URL(separate multiple sources with commas)",
                    "type": "text",
                    "required": True,
                    "default": "https://aws.amazon.com/what-is/retrieval-augmented-generation/",
                }
            ],
            "message": "What is RAG?",
        },
    )
    print(f"Response status: {response.status_code}, Response body: {response.json()}")
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_load_home(client):
    """
    Tests the / endpoint.

    Sends a GET request to the endpoint and checks that the response
    has a 200 status code and the expected JSON body.
    """
    response = client.get("/")
    print(f"Response status: {response.status_code}, Response body: {response.json()}")
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "message": "Vivace Telex Integration",
        "status": 200,
    }


@pytest.mark.asyncio
async def test_load_settings(client):
    """
    Tests the /integration_setting endpoint.

    Sends a GET request to the endpoint and checks that the response
    has a 200 status code and the expected JSON body with the "data" key.
    """
    response = client.get("/integration_setting")
    print(f"Response status: {response.status_code}, Response body: {response.json()}")
    assert response.status_code == 200
    assert "data" in response.json()  # Check for the correct key in the response


@pytest.mark.asyncio
async def test_health_check(client):
    """
    Tests the /healthcheck endpoint.

    Sends a GET request to the endpoint and checks that the response
    has a 200 status code and the expected JSON body with the "status" key set to "active".
    """
    response = client.get("/healthcheck")
    print(f"Response status: {response.status_code}, Response body: {response.json()}")
    assert response.status_code == 200
    assert response.json() == {"status": "active"}


@pytest.mark.asyncio
async def test_get_logo(client):
    """
    Tests the /logo.png endpoint.

    Sends a GET request to the endpoint and ensures that the response
    has a 200 status code and the content type is "image/png".
    """

    response = client.get("/logo.png")
    print(
        f"Response status: {response.status_code}, Response headers: {response.headers}"
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
