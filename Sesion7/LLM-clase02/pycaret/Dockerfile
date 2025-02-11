# Usa una imagen oficial de Python compatible con PyCaret
FROM python:3.10

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt requirements.txt
# COPY streamlit_pycaret/app.py /app/app.py

# EXPOSE 8501

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /root/.jupyter

RUN echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py && \ 
    echo "c.NotebookApp.password = ''" >> /root/.jupyter/jupyter_notebook_config.py && \ 
    echo "c.NotebookApp.open_browser = False" >> /root/.jupyter/jupyter_notebook_config.py && \ 
    echo "c.NotebookApp.allow_root = True" >> /root/.jupyter/jupyter_notebook_config.py

# Especifica el comando por defecto al ejecutar el contenedor
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root"]

# Comando por defecto para ejecutar Streamlit
# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
