# Usar la imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /code

# Actualizar pip y setuptools
RUN python -m pip install --upgrade pip setuptools

# Crear un entorno virtual en el directorio /code/venv
RUN python -m venv /code/venv

# Activar el entorno virtual para los comandos siguientes
ENV PATH="/code/venv/bin:$PATH"

# Copiar todos los archivos del directorio actual al directorio /code en el contenedor
COPY . /code/

# Instalar las dependencias en el entorno virtual
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Establecer el PYTHONPATH
ENV PYTHONPATH=/code

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9900"]
