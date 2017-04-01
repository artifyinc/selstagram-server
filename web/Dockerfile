FROM python:3.4.6
MAINTAINER Yoonje Choi <yoonjechoi@gmail.com>

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y nginx supervisor
RUN pip install uwsgi

# install pip requirements
ADD requirements.txt /home/docker/code/requirements.txt
RUN pip install -r /home/docker/code/requirements.txt


# setup nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
ADD nginx/selstagram-server /etc/nginx/sites-available/selstagram-server
RUN ln -s /etc/nginx/sites-available/selstagram-server /etc/nginx/sites-enabled/
RUN rm /etc/nginx/sites-enabled/default

EXPOSE 80
EXPOSE 443


# setup django
ADD selstagram_server /home/docker/code/selstagram_server
WORKDIR /home/docker/code/selstagram_server

ARG PYTHONUNBUFFERED
ARG BROKER_URL
ARG DB_HOSTNAME
ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_NAME
ARG DJANGO_SETTINGS_MODULE
ARG SELSTA101_SLACK_INCOMING_HOOK_URL
ARG SELSTA101_ITUNES_SHARED_SECRET

RUN python manage.py collectstatic --no-input


# setup uwsgi
ADD uwsgi /home/docker/code/uwsgi


# setup supervisor
ADD supervisor/selstagram-server.conf /etc/supervisor/conf.d/
RUN mkdir /home/docker/log
CMD ["supervisord", "-n"]
