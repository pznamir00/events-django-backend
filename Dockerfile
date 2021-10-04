FROM python:3.8

ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
COPY users.json /code/
RUN pip install -r requirements.txt
COPY . /code/