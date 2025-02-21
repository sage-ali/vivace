import pytest
from tests import client


@pytest.mark.asyncio
async def test_modify_message(client):
    response = client.post(
        "/api/vivace", json={
            "settings": [
                {
                    "label": "Knowledge Base URL(separate multiple sources with commas)",
                    "type": "text",
                    "required": True,
                    "default": "https://aws.amazon.com/what-is/retrieval-augmented-generation/"
                }
            ],
            "message": "This is a test message that will be formatted."
        })
    print(f"Response status: {response.status_code}, Response body: {response.json()}")
    assert response.status_code == 200
    assert "message" in response.json()

@pytest.mark.asyncio
async def test_load_home(client):
    response = client.get("/")
    print(f"Response status: {response.status_code}, Response body: {response.json()}")
    assert response.status_code == 200
    assert response.json() == {"code": 200, "message": "Vivace Telex Integration", "status": 200}

@pytest.mark.asyncio
async def test_load_settings(client):
    response = client.get("/integration_setting")
    print(f"Response status: {response.status_code}, Response body: {response.json()}")
    assert response.status_code == 200
    assert "data" in response.json()  # Check for the correct key in the response

@pytest.mark.asyncio
async def test_health_check(client):
    response = client.get("/healthcheck")
    print(f"Response status: {response.status_code}, Response body: {response.json()}")
    assert response.status_code == 200
    assert response.json() == {"status": "active"}

@pytest.mark.asyncio
async def test_get_logo(client):
    response = client.get("/logo.png")
    print(f"Response status: {response.status_code}, Response headers: {response.headers}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
