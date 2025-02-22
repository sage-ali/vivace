from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app, base_url="http://test/api")



@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
