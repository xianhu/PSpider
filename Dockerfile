# Dockerfile by xianhu: build a docker image for spider or flask
# usage: docker build -t user/centos:v05 .

FROM daocloud.io/library/centos:6.8
MAINTAINER xianhu <qixianhu@qq.com>

# change system environments
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# change system local time
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# update yum and install something
RUN yum update -y
RUN yum install -y xz
RUN yum install -y vim
RUN yum install -y git
RUN yum install -y wget
RUN yum install -y crontabs
RUN yum install -y gcc
RUN yum install -y make
RUN yum install -y zlib-devel
RUN yum install -y openssl-devel
RUN yum clean all

# restart crontab service
RUN service crond restart

# download python3
WORKDIR /root/
RUN wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tar.xz
# or RUN COPY Python-3.5.2.tar.xz /root/
RUN tar -xf Python-3.5.2.tar.xz

# install python3
WORKDIR /root/Python-3.5.2
RUN ./configure
RUN make install
RUN make clean
RUN make distclean

# install libs of python3
ADD ./Dockerfile_requirements.txt /root/
WORKDIR /root/
RUN pip3 install --upgrade pip
RUN pip3 install -r Dockerfile_requirements.txt
RUN rm -rf /root/*

# change python to python3
RUN echo "alias python=python3" >> /root/.bashrc
RUN source /root/.bashrc

CMD [/bin/bash]
