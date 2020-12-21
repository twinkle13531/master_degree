FROM ubuntu:bionic
RUN apt update \
&& apt-get -yV install -y python3 python3-pip \
&& apt-get -yV install libgmp-dev libglpk-dev \
&& apt-get -yV install make libc-dev make automake autoconf libtool clang wget unzip \
&& apt-get -yV install yum \
&& apt-get clean
RUN cd /opt \
&& wget https://github.com/4ti2/4ti2/archive/master.zip \
&& unzip master.zip \
&& mv 4ti2-master 4ti2 \
&& rm master.zip \
&& cd 4ti2 \
&& ./autogen.sh \
&& CC=clang ./configure \ 
&& make \
&& make check \
&& make install-exec \
&& rm -rf /var/lib/apt/lists/* \
&& pip3 install \
jupyterlab==2.1.4
