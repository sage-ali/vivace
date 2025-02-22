from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app, base_url="http://test/api")


@pytest.fixture(scope="module")
def client():
    """
    A fixture to create a TestClient instance for the app.

    Yields a TestClient instance which can be used to make requests to the app.
    The scope of the fixture is "module", meaning that the same instance will be yielded for all tests in the same module.
    """
    with TestClient(app) as c:
        yield c
