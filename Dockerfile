# 1. A BASE
# Começa com um Linux super leve (slim) que já tem Python 3.12 instalado.
FROM python:3.12-slim

# 2. PREPARAÇÃO DO SISTEMA
# Instala compiladores básicos (gcc) caso alguma lib python precise compilar código C.
# O 'rm -rf' limpa o cache do apt para a imagem ficar pequena.
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 3. DIRETÓRIO DE TRABALHO
# Cria a pasta /app dentro do container e entra nela. Tudo acontece aqui agora.
WORKDIR /app

# 4. DEPENDÊNCIAS (CACHED)
# Copia SÓ o requirements primeiro.
# Por que? O Docker faz cache. Se você mudar seu código mas não mudar as libs,
# ele pula essa etapa demorada na próxima vez.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. O CÓDIGO
# Agora sim, copia todo o resto dos arquivos do seu PC para a pasta /app do container.
COPY . .

# 6. PORTA
# Apenas documenta que esse container vai "falar" na porta 5000.
EXPOSE 5000

# 7. LOGS EM TEMPO REAL
# Garante que os prints do Python apareçam imediatamente no terminal do Docker.
ENV PYTHONUNBUFFERED=1

# 8. O COMANDO FINAL
# O que ele executa quando você dá o "Start".
CMD ["python", "app.py"]