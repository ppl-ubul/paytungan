FROM python:3.8-slim

ARG DB_CONFIG
ARG DJANGO_SECRET_KEY
ARG DJANGO_SETTINGS_MODULE

ENV DB_CONFIG=$DB_CONFIG
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
ENV DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE


RUN apt-get update
RUN apt-get install -y libpq-dev gcc

RUN mkdir -p /app
COPY ./requirements.txt .

# Install requirements
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

RUN chmod +x deployment.sh run.sh
RUN bash deployment.sh

ENTRYPOINT ["bash","/app/run.sh"]
