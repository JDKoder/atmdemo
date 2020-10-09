
FROM ubuntu:18.04
MAINTAINER JDKoder@github.com

#Install python with it library dependencies
RUN apt-get update && \
apt-get upgrade -y && \
apt-get -y install python3 python3-pip && \
pip3 install pymongo dnspython

#expose for internet traffic
EXPOSE 8080
#expose for mongdb transactions
EXPOSE 27017

RUN mkdir /demo

COPY . /demo
