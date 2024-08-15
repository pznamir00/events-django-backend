FROM python:3.8

#init
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

#Django gis
RUN apt-get update -y
RUN apt-get install -y gdal-bin
RUN apt-get update -y
RUN apt-get install -y python3-gdal
RUN apt-get update -y
RUN apt-get install -y rabbitmq-server 

#copy source code
COPY . /code/
RUN chmod +x /code/scripts/wait-for-it.sh


