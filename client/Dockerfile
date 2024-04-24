FROM python:3.9
#FROM python:3.8-slim-buster

WORKDIR /nebula_client

COPY . .

RUN apt update && apt upgrade -y
RUN apt install python3-dev -y
RUN python3.9 -m pip install -r requirements.txt
RUN apt update && apt install awscli -y
RUN apt-get update; apt-get install curl -y
RUN curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"
RUN dpkg -i session-manager-plugin.deb

ENTRYPOINT ["python3.9"]
#ENTRYPOINT [ "/bin/bash"]
