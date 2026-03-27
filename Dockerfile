FROM python:3.10-slim

WORKDIR /app

# dépendances système nécessaires pour pandas / sklearn
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# installer dépendances python
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copier code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]