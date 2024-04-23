# Usar la imagen base de Python
FROM python:3.11.8

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /code

# Actualizar pip y setuptools
RUN python -m pip install --upgrade pip setuptools

# Crear un entorno virtual en el directorio /code/movieapp
RUN python -m venv /code/movieapp

# Activar el entorno virtual para los comandos siguientes
ENV PATH="/code/movieapp/bin:$PATH"

# Copiar todos los archivos del directorio actual al directorio /code en el contenedor
COPY . /code/

# Instalar las dependencias en el entorno virtual
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Establecer el PYTHONPATH
ENV PYTHONPATH=/code

# Crear un script de entrada para activar el entorno virtual y ejecutar la aplicación
RUN echo "#!/bin/bash\nsource /code/movieapp/bin/activate\nexec uvicorn main:app --host 0.0.0.0 --port 9900" > /code/entrypoint.sh \
    && chmod +x /code/entrypoint.sh

# Configurar el script de entrada para que se ejecute al iniciar el contenedor
ENTRYPOINT ["/code/entrypoint.sh"]