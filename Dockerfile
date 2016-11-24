# build a docker image for spider or flask
# Dockerfile by xianhu
# usage: docker build -t="user/centos:v01" .

FROM centos:latest

MAINTAINER xianhu <qixianhu@qq.com>

ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN yum update -y
RUN yum install -y vim
RUN yum install -y git
RUN yum install -y wget
RUN yum install -y gcc
RUN yum install -y make
RUN yum install -y zlib-devel
RUN yum install -y openssl-devel
RUN yum clean all

ADD ./Dockerfile_requirements.txt /root/

WORKDIR /root/
RUN wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tar.xz
RUN tar -xf Python-3.5.2.tar.xz

WORKDIR /root/Python-3.5.2
RUN ./configure
RUN make install
RUN make clean
RUN make distclean

WORKDIR /root/
RUN pip3 install --upgrade pip
RUN pip3 install -r Dockerfile_requirements.txt
RUN rm -rf /root/*

WORKDIR /root/
RUN echo "alias python=python3" >> /root/.bashrc
RUN source /root/.bashrc

CMD /bin/bash
