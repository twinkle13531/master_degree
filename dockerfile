FROM ubuntu:bionic
RUN apt update \
&& apt install -y python3 python3-pip \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*
RUN pip3 install \
pycaret==1.0.0 \
jupyterlab==2.1.4
