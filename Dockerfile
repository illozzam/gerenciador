FROM python:3.11

# ARG DEBUG
# ARG MYSQL_HOST
# ARG MYSQL_PORT
# ARG MYSQL_USER
# ARG MYSQL_PASSWORD
# ARG MYSQL_DATABASE

# Working directory
RUN mkdir /gerenciador
RUN mkdir /logs
WORKDIR /gerenciador

# Environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update && apt-get install -y netcat
RUN apt-get install -y nginx

# Install Python dependencies
RUN pip install -U pip && pip install -U setuptools
COPY requirements.txt /gerenciador/
RUN pip install -r /gerenciador/requirements.txt

# Copy project files
COPY . /gerenciador/
COPY extras/nginx.conf /etc/nginx/nginx.conf

RUN rm /etc/nginx/sites-enabled/default
# RUN python manage.py wait_for_db
RUN python manage.py migrate
RUN python manage.py shell < inicio.py
RUN python manage.py collectstatic --noinput