import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_acceptance():
    response = client.post(
        "/process-file",
        files={"file": ("test_voice.wav", b"Fake audio content")}
    )
    assert response.status_code == 200, "API should return status 200"
    assert "result" in response.json(), "Response should contain 'result'"
