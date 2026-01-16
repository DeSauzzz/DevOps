FROM ubuntu:22.04
WORKDIR ./DevOps
RUN apt-get update && apt-get install -y sudo
COPY install.sh ./install.sh
COPY myapp ./myapp
COPY config_examples ./config_examples
RUN chmod +x ./install.sh

