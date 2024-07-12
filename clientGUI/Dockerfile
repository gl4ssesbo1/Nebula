FROM python:3.9

WORKDIR /clientGUI
COPY . .

RUN apt-get update && apt-get upgrade -y
RUN apt install python3 python3-dev python3-pip -y
#RUN apt install docker.io -y
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt update && apt install awscli -y
RUN apt-get update; apt-get install curl -y
#RUN curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"
#RUN dpkg -i session-manager-plugin.deb
#RUN service docker start
#RUN ls /nebula

ENTRYPOINT ["python3", "/clientGUI/widget.py"]
