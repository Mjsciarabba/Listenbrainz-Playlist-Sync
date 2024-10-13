FROM python:3.11-alpine

WORKDIR /app

COPY . /app

RUN apk add --no-cache --virtual build-dependencies python3-dev gcc musl-dev; \
    pip install -r requirements.txt; \
    apk del build-dependencies

CMD "/app/run.sh"