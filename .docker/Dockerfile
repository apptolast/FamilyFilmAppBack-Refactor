# Usar una imagen oficial de Python optimizada para FastAPI
FROM python:3.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /code

# Install dependencies
# Ensure that the build context is the root of the project
COPY ../requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt


# Copiar el resto del código de la aplicación
COPY . .

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9900"]
