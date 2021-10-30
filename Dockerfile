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
RUN apt install -y python3-gdal

#copy source code
COPY . /code/

#migrations entrypoint
COPY migrate-entrypoint.sh /code/migrate-entrypoint.sh
RUN chmod +x migrate-entrypoint.sh
ENTRYPOINT ["sh", "migrate-entrypoint.sh"]
