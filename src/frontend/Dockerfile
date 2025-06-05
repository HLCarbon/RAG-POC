FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y gettext-base && rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash", "-c", "envsubst < /app/script.js > /app/script.js.tmp && mv /app/script.js.tmp /app/script.js && python -m http.server 8000"]