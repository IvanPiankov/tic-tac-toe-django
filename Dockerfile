FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /tictactoe
COPY requirements.txt /tictactoe/

RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev

RUN pip install -r requirements.txt

COPY . /tictactoe/