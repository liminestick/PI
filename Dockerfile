# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем системные зависимости (включая Git)
RUN apt-get update && apt-get install -y git && apt-get clean

# Копируем все файлы из текущей директории на контейнер
COPY . /app

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 8000 для доступа к приложению
EXPOSE 8000

# Команда для запуска FastAPI приложения через Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
