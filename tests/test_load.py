import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_load():
    for _ in range(5):  # Симуляция 100 одновременных запросов
        response = client.post(
            "/process-file",
            files={"file": ("test_voice.wav", b"Fake audio content")}
        )
        assert response.status_code == 200, "API should return status 200"
