from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_regression():
    # Входные данные для теста
    test_text = "Привет, мир!"  # Замените на текст, который вы тестируете
    test_file_path = "test_voice.wav"  # Тестовый голосовой файл (должен существовать)

    # Ожидаемый результат (зависит от вашей модели)
    # Например, можно сохранить ранее полученный результат в файл и сравнивать с ним.
    expected_output_path = "expected_output.wav"

    with open(test_file_path, "rb") as test_file:
        response = client.post(
            "/synthesize-speech",
            data={"src_text": test_text},
            files={"file": (test_file_path, test_file, "audio/wav")},
        )

    # Проверяем успешность запроса
    assert response.status_code == 200, "API должен возвращать статус 200"

    # Сохраняем результат для сравнения
    result_audio_path = "test_output.wav"
    with open(result_audio_path, "wb") as f:
        f.write(response.content)

    # Сравнение результатов (ожидаемого и полученного)
    with open(expected_output_path, "rb") as expected_file, open(result_audio_path, "rb") as result_file:
        assert expected_file.read() == result_file.read(), "Выходной файл не совпадает с ожидаемым"
