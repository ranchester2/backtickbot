FROM debian:buster

RUN apt-get update
RUN apt-get -y install python3-pip firefox-esr

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt

# This directory should be a volume, with the .env
RUN mkdir /app/secrets
# This should also be a volume with the persistent data
RUN mkdir /app/runtime
# There should also be a bind mount to the webserver directory
RUN mkdir /app/webdata

CMD python3 backtickbot.py