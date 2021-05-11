FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

RUN apt-get update; apt-get install curl -y
RUN curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"
RUN dpkg -i session-manager-plugin.deb

ENTRYPOINT [ "python3"]