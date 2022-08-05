FROM python:3.10

# Working directory
WORKDIR mkdir /gerenciador

# Environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update && apt-get install -y netcat

# Install Python dependencies
RUN pip install -U pip && pip install -U setuptools
COPY requirements.txt /gerenciador/
RUN pip install -r /gerenciador/requirements.txt

# Migrations and static files
RUN python gerenciador/manage.py migrate
RUN python gerenciador/manage.py shell < inicio.py
RUN python gerenciador/manage.py collectstatic --noinput


# Copy project
COPY . /gerenciador/