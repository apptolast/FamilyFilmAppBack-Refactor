# Use the official Python image
FROM python:3.11.8

# Set the working directory in the container
WORKDIR /code

# Install system dependencies for PostgreSQL and psycopg2
RUN apt-get update && apt-get install -y postgresql libpq-dev gcc

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Specify the command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9900"]