FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc libpq-dev build-essential && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc build-essential libpq-dev && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*
COPY . .
CMD ["python", "-m", "app.main"]

