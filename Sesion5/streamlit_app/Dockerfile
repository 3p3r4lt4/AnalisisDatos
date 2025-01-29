FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt /app/

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . /app/

# Expone el puerto usado por Streamlit
EXPOSE 8501

# Comando por defecto para ejecutar la aplicación
CMD ["streamlit", "run", "app.py"]
