# Указываем базовый образ
FROM python:3.8-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости и утилиты
RUN apt-get update && apt-get install -y curl wget \
    && pip install -r requirements.txt

# Копируем файлы проекта в контейнер
COPY app.py .
COPY static/ ./static/
COPY k8s/ ./k8s/

# Открываем порт 5000
EXPOSE 5000

# Запускаем приложение
CMD ["python3", "app.py"]

