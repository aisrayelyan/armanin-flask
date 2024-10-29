FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y curl wget && pip install -r requirements.txt

COPY app.py .
COPY static/ ./static/
COPY k8s/ ./k8s/

RUN ls -al ./k8s  # Добавлено для проверки содержимого директории k8s

EXPOSE 5000

CMD ["python3", "app.py"]
