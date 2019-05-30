FROM python:3.7.0-alpine3.7

ENV PYTHONUNBUFFERED=1
ENV COLUMNS=200

COPY . /bot
WORKDIR /bot

RUN apk add --no-cache linux-headers bash gcc python3-dev \
    zlib-dev libmagic make libffi-dev && \
    pip install --upgrade pip && pip install -U -r requirements.txt
