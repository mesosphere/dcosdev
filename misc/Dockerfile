FROM ubuntu:16.04
  
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN apt-get install -y python
RUN apt-get install -y python-pip

RUN curl -O https://downloads.dcos.io/binaries/cli/linux/x86-64/dcos-1.11/dcos
RUN mv dcos /usr/local/bin
RUN chmod +x /usr/local/bin/dcos

COPY . /dcosdev
RUN cd /dcosdev && pip install . && cd .. && rm -rf /dcosdev
