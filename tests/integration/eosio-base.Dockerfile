FROM eosio/builder as builder

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get -y install openssl         \
                       ca-certificates    \
                       git                \
                       python3-pip        \
                       python3-setuptools \
                       cmake              \
                       libgmp3-dev        \
                       doxygen            \
                       graphviz           \
                       tk-dev             \
    && rm -rf /var/lib/apt/lists/*

##############     EOS     #############################################################################################

ARG eos_branch=v1.3.1
ARG eos_symbol=SYS
 
RUN git clone -b $eos_branch https://github.com/EOSIO/eos.git --recursive /opt/eos
WORKDIR /opt/eos

RUN ./eosio_build.sh
RUN ./eosio_install.sh
