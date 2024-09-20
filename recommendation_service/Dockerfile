# recommendation_service/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# Add --no-cache-dir to ensure we're not using cached packages
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_DEBUG=1

CMD ["python", "app.py"]