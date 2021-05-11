FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt
<<<<<<< HEAD
RUN curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"
RUN sudo dpkg -i session-manager-plugin.deb
=======
>>>>>>> 81d1184a68f8eb8db769fc2ccbb7f005f18b9266

ENTRYPOINT [ "python3"]