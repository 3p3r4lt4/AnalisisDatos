# Usar una imagen base de Ubuntu
FROM ubuntu:20.04

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Clonar el repositorio de OMniLeads
RUN git clone https://github.com/omnileads/omnileads /opt/omnileads

# Instalar dependencias de OMniLeads
WORKDIR /opt/omnileads
RUN pip3 install -r requirements.txt

# Exponer el puerto para OMniLeads
EXPOSE 8000

# Comando para iniciar OMniLeads
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]