FROM python:3.8-slim

RUN apt-get update
RUN apt-get install -y libpq-dev gcc

RUN mkdir -p /app
COPY ./requirements.txt .

# Install requirements
RUN pip install -U -r requirements.txt

COPY . /app
WORKDIR /app

RUN python manage.py collectstatic --noinput

RUN chmod +x run.sh

ENTRYPOINT ["bash","/app/run.sh"]
