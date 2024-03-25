FROM python:3.11-slim

WORKDIR /Bot

COPY requirements.txt requirements.txt

RUN apt-get update && pip install -r requirements.txt


RUN rm ./requirements.txt

COPY ./TgBot ./TgBot

CMD ["python", "./TgBot/run.py"]
