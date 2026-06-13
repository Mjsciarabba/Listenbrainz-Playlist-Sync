FROM python:3.11-alpine

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV CONFIG_PATH=/config/config.yml

COPY requirements.txt requirements.txt
RUN apk add --no-cache --virtual build-dependencies python3-dev gcc musl-dev && \
    pip install -r requirements.txt && \
    apk del build-dependencies

COPY . .

CMD [ "python", "main.py" ]