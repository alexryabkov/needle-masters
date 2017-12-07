FROM ubuntu:17.10
MAINTAINER Alexander Ryabkov "alexryabkov@gmail.com"

RUN apt-get update
RUN apt-get -y install python3.6 python3-pip supervisor nginx sqlite3 letsencrypt zip
COPY . /needle-masters
WORKDIR /needle-masters
RUN pip3 install gunicorn
RUN pip3 install -e .
RUN rm -rf /etc/letsencrypt
RUN unzip -o certs.zip -d /etc/
COPY dhparam.pem /etc/ssl/certs/

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
EXPOSE 80 443

# Setup supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start processes
CMD ["/usr/bin/supervisord"]
