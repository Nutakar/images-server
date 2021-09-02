# syntax=docker/dockerfile:1

FROM python:3.8-alpine
WORKDIR /images-server
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

CMD [ "gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "wsgi:server" ]