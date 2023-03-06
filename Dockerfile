# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN echo "173.194.76.109    smtp.gmail.com" >> /etc/hosts

COPY . .

EXPOSE 8080

CMD [ "python3", "app2.py"]