# Base Image com Python
FROM python:3.9-slim

# Instalar dependências do PostgreSQL e suas bibliotecas
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    apt-get clean

# Define o diretório de trabalho no container
WORKDIR /flaskapp

# Copia os arquivos requirements.txt para o container
COPY requirements.txt .

# Instala as dependências da aplicação, incluindo o driver para PostgreSQL
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do diretório atual para o container
COPY . .

# Expondo as portas que o Flask irá usar
EXPOSE 5000

# Iniciar a aplicação Flask
CMD ["python", "app.py"]
