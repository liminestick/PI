from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_synthesize_speech():
    # Создаем текстовый вход и загружаем тестовый файл
    test_text = "Привет, мир!"
    test_file_path = "test_voice.wav"  # Замените на существующий тестовый .wav файл

    with open(test_file_path, "rb") as test_file:
        response = client.post(
            "/synthesize-speech",
            data={"src_text": test_text},
            files={"file": (test_file_path, test_file, "audio/wav")},
        )

    # Проверяем успешность запроса
    assert response.status_code == 200, "API должен возвращать статус 200"
    assert response.headers["content-disposition"].startswith(
        "attachment"
    ), "Должен быть загружен файл"
