FROM python:3.9
#FROM python:3.8-slim-buster

WORKDIR /nebula
COPY . .

RUN apt-get update && apt-get upgrade -y
RUN apt install python3-dev -y
RUN apt install docker.io -y
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt update && apt install awscli -y
RUN apt-get update; apt-get install curl -y
RUN curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"
RUN dpkg -i session-manager-plugin.deb
RUN service docker start
RUN ls /nebula

ENTRYPOINT python3.9 teamserver.py -c teamserver.conf
