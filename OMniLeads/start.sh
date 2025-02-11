#!/bin/bash

# Detener contenedores si ya están en ejecución
echo "Deteniendo contenedores existentes (si los hay)..."
docker-compose down

# Construir y levantar los contenedores
echo "Construyendo y levantando los contenedores..."
docker-compose up --build

# Alternativa: Si no quieres ver los logs en la terminal, puedes usar:
# docker-compose up --build -d