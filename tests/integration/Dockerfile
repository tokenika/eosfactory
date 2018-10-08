FROM eosio/builder as builder

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install openssl ca-certificates git && \
    rm -rf /var/lib/apt/lists/*

ARG branch=v1.3.1
ARG symbol=SYS

RUN git clone -b $branch https://github.com/EOSIO/eos.git --recursive \
    && cd eos && echo "$branch:$(git rev-parse HEAD)" > /etc/eosio-version \
    && cmake -H. -B"/tmp/build" -GNinja -DCMAKE_BUILD_TYPE=Release -DWASM_ROOT=/opt/wasm -DCMAKE_CXX_COMPILER=clang++ \
       -DCMAKE_C_COMPILER=clang -DCMAKE_INSTALL_PREFIX=/tmp/build -DBUILD_MONGO_DB_PLUGIN=true -DCORE_SYMBOL_NAME=$symbol \
    && cmake --build /tmp/build --target install && rm /tmp/build/bin/eosiocpp

RUN git clone https://github.com/tokenika/eosfactory.git /opt/eosfactory/
WORKDIR /opt/eosfactory/

RUN mv /eos /opt/eos
RUN mv /tmp/build /opt/eos/build

RUN apt-get update
RUN apt-get install -y python3-pip python3-setuptools
RUN pip3 install --upgrade pip
RUN rm -f /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python && \
    rm -f /usr/bin/pip && ln -s /usr/bin/pip3 /usr/bin/pip

RUN mkdir /opt/workspace
RUN export TERM=xterm && ./build.sh -e /opt/eos -w /opt/workspace

RUN python -m pip install termcolor

# https://stackoverflow.com/questions/48109702/command-source-doesnt-work-in-dockerfile
#RUN . ~/.profile && \
#    python3 tests/01_hello_world.py && \
#    python3 tests/02_eosio_token.py && \
#    python3 tests/03_tic_tac_toe.py


