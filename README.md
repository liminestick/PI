# Приложение для синтеза речи на основе текста

Это приложение использует модель XTTS для генерации речи из текста. Пользователи могут отправлять текст и аудиофайл с голосом, на котором будет обучаться модель, а взамен получать аудиофайл с озвученным текстом.

## Требования

Перед запуском приложения убедитесь, что у вас установлены все зависимости:

1. Python 3.9 или выше.
2. Установите виртуальное окружение (необязательно, но рекомендуется):

    ```bash
    python -m venv .venv
    ```

3. Активируйте виртуальное окружение:

    - Для Windows:
      ```bash
      .\.venv\Scripts\activate
      ```
    - Для macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```

4. Установите все зависимости из файла `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

5. Клонируйте модель XTTS для русского языка с Hugging Face:

    ```bash
    git clone https://huggingface.co/omogr/XTTS-ru-ipa model
    ```

6. Установите зависимость `omogre`, которая используется для транскриптора:

    ```bash
    pip install git+https://github.com/omogr/omogre.git
    ```

## Запуск API

Приложение использует FastAPI для обработки запросов и синтеза речи. Для запуска API выполните следующую команду:

```bash
uvicorn main:app --reload
