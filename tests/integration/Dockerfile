FROM eosio/builder as builder

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install openssl ca-certificates git python3-pip python3-setuptools && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN rm -f /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python && \
    rm -f /usr/bin/pip && ln -s /usr/bin/pip3 /usr/bin/pip

###########################################################33

ARG branch=v1.3.1
ARG symbol=SYS

RUN git clone https://github.com/EOSIO/eos.git --recursive --depth 1 /opt/eos
WORKDIR /opt/eos
RUN git checkout $branch

RUN apt-get update && apt-get -y install cmake libgmp3-dev doxygen graphviz

RUN ./eosio_build.sh
RUN ./eosio_install.sh

###########################################################

ARG eosfactory_branch=master

RUN git clone -b "$eosfactory_branch" https://github.com/tokenika/eosfactory.git /opt/eosfactory/
WORKDIR /opt/eosfactory/

RUN mkdir /opt/workspace
RUN export TERM=xterm && ./build.sh -e /opt/eos -w /opt/workspace

RUN python -m pip install termcolor

RUN mkdir ~/eosio-wallet/

# https://stackoverflow.com/questions/48109702/command-source-doesnt-work-in-dockerfile
RUN . ~/.profile && \
    python3 tests/01_hello_world.py && \
    python3 tests/02_eosio_token.py && \
    python3 tests/03_tic_tac_toe.py


