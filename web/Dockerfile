FROM python:3.4.6
MAINTAINER Yoonje Choi <yoonjechoi@gmail.com>

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y nginx supervisor
RUN pip install uwsgi


# setup nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default

ADD nginx/selstagram-server /etc/nginx/sites-available/selstagram-server
RUN ln -s /etc/nginx/sites-available/selstagram-server /etc/nginx/sites-enabled/
ADD supervisor-selstagram.conf /etc/supervisor/conf.d/


# install pip requirements
ADD requirements.txt /home/docker/code/requirements.txt
RUN pip install -r /home/docker/code/requirements.txt

# copy source code
ADD . /home/docker/code/


WORKDIR /home/docker/code/selstagram_server
RUN python manage.py collectstatic --no-input

EXPOSE 80
EXPOSE 443

CMD ["supervisord", "-n"]

