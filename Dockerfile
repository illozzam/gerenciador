FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR mkdir /gerenciador
RUN pip install -U pip && pip install -U setuptools
COPY requirements.txt /gerenciador/
RUN pip install -r /gerenciador/requirements.txt
ADD . /gerenciador/
EXPOSE 8000
