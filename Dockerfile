FROM python:3.12-slim

WORKDIR /usr/src

COPY . /usr/src

RUN chmod +x ./entrypoint.sh

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["/usr/src/entrypoint.sh"]