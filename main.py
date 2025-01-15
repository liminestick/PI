from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import torchaudio  # Добавляем импорт torchaudio
import shutil
import os
from model_test import XttsInference  # Импортируем класс для инференса

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

# Эндпоинт для синтеза речи ыыыы
@app.post("/synthesize-speech")
async def synthesize_speech(src_text: str, file: UploadFile = File(...)):
    """
    Эндпоинт для синтеза речи. Принимает текст и аудиофайл с голосом для обучения модели.

    Параметры:
    - src_text: текст для синтеза.
    - file: файл .wav с голосом для обучения модели.
    - да
    Возвращает:
    - аудиофайл с синтезированной речью.
    """
    # Временная директория для сохранения загруженного файла
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)

    # Сохраняем загруженный файл .wav
    wav_file_path = os.path.join(temp_dir, file.filename)
    with open(wav_file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Инициализируем инференс с учетом загруженного аудиофайла
    xtts_inference = XttsInference(reference_audio=wav_file_path)

    # Генерация аудио для данного текста
    tts_text, audio = xtts_inference(src_text)

    # Сохраняем аудио в выходной файл
    output_audio_path = "output_audio.wav"
    torchaudio.save(output_audio_path, audio, sample_rate=24000)  # Сохраняем аудио

    return FileResponse(output_audio_path, filename="output_audio.wav")
