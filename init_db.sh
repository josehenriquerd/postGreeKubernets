#!/bin/bash
# Esperar o PostgreSQL iniciar
sleep 10

# Criar o usuário e o banco de dados
service postgresql start
su - postgres -c "psql -c \"CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';\""
su - postgres -c "psql -c \"CREATE DATABASE $POSTGRES_DB WITH ENCODING 'UTF8';\""
su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;\""
