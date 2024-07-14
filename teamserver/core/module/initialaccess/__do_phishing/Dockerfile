# A basic apache server with PHP. To use either add or bind mount content under /var/www
# https://docs.docker.com/engine/reference/builder/

FROM ubuntu:16.04

# Use bash instead of sh.
SHELL ["/bin/bash", "-c"]

WORKDIR /app
ADD . /app

# Use the default UTF-8 language.
ENV LANG C.UTF-8

RUN apt-get update && apt-get install -y apache2 php libapache2-mod-php php-curl php-json php-cgi php-cli 

EXPOSE 80 443

RUN cp info.php /var/www/html/

ENTRYPOINT ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
