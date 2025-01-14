import requests

# Адрес нашего API
url = "http://127.0.0.1:8000/synthesize-speech"  # Убедитесь, что URL совпадает с вашим API

# Путь к файлам
audio_file_path = "test_voice.wav"  # Путь к файлу с аудио
text_file_path = "test_text.txt"  # Путь к файлу с текстом

# Открытие файлов для отправки
with open(audio_file_path, "rb") as audio_file, open(text_file_path, "r", encoding='utf-8') as text_file:
    # Чтение текста из файла
    text_content = text_file.read().strip()  # Убираем лишние пробелы или новые строки

    # Отправка POST-запроса с файлом .wav и текстом в query-параметре
    response = requests.post(
        url,
        params={"src_text": text_content},  # Текст передаем как query-параметр
        files={"file": (audio_file_path, audio_file, "audio/wav")}  # Аудиофайл
    )

# Проверка, что запрос прошел успешно
if response.status_code == 200:
    # Сохранение полученного аудиофайла
    download_audio_path = "output_audio.wav"  # Путь для сохраненного аудио
    with open(download_audio_path, "wb") as f:
        f.write(response.content)
    print(f"Файл успешно загружен и сохранен как {download_audio_path}")
else:
    print(f"Ошибка! Статус: {response.status_code}")
    print(response.text)  # Выводим текст ошибки, чтобы понять что именно не так
