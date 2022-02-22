# From Docker documentation:
# https://docs.docker.com/samples/django/

FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install dependencies.
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/