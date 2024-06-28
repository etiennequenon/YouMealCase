FROM python:3.12-slim

WORKDIR /usr/src

COPY . /usr/src

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

RUN chmod +x ./entrypoint.sh ./wait_for_db.sh

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["/usr/src/entrypoint.sh"]