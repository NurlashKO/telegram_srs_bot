FROM python:3.7-alpine

ENV PYTHONUNBUFFERED=1
ENV COLUMNS=200

COPY . /bot
WORKDIR /bot

RUN echo -e "http://nl.alpinelinux.org/alpine/v3.9/main\nhttp://nl.alpinelinux.org/alpine/v3.7/community" > /etc/apk/repositories

RUN apk add --no-cache linux-headers bash gcc python3-dev \
    zlib-dev libmagic make libffi-dev && \
    pip install --upgrade pip && \
    pip install -U -r requirements.txt && \
    pip install -U -r dev_requirements.txt
