FROM python:3.12-slim

# Instala dependências do sistema (opcional) para compilação de libs, se necessário
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos o projeto inteiro (mas .dockerignore vai excluir coisas desnecessárias)
COPY . .

EXPOSE 5000
ENV PYTHONUNBUFFERED=1

# A URL do Anki precisa apontar para o host que roda o Anki (Docker Desktop: host.docker.internal)
# DATABASE_URL virá do docker-compose.yml
CMD ["python", "app.py"]
