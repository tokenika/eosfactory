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

##############   PYTHON    #############################################################################################
## Based mostly on https://github.com/docker-library/python/blob/005dda958/3.5/jessie/Dockerfile
ARG python_version=3.5.6

ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8
ENV TERM xterm

RUN set -ex \
	\
	&& wget -O python.tar.xz "https://www.python.org/ftp/python/${python_version%%[a-z]*}/Python-$python_version.tar.xz" \
	&& wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${python_version%%[a-z]*}/Python-$python_version.tar.xz.asc" \
	&& mkdir -p /usr/src/python \
	&& tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
	&& rm python.tar.xz \
	\
	&& cd /usr/src/python \
	&& gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" \
	&& ./configure \
		--build="$gnuArch" \
		--enable-loadable-sqlite-extensions \
		--enable-shared \
		--with-system-expat \
		--with-system-ffi \
		--without-ensurepip \
	&& make -j "$(nproc)" \
	&& make install \
	&& ldconfig \
	\
	&& find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' + \
	&& rm -rf /usr/src/python \
	\
	&& python3 --version

# make some useful symlinks that are expected to exist
RUN cd /usr/local/bin \
	&& ln -s idle3 idle \
	&& ln -s pydoc3 pydoc \
	&& ln -s python3 python \
	&& ln -s python3-config python-config

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 18.0

RUN set -ex; \
	\
	wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py'; \
	\
	python get-pip.py \
		--disable-pip-version-check \
		--no-cache-dir \
		"pip==$PYTHON_PIP_VERSION" \
	; \
	pip --version; \
	\
	find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' +; \
	rm -f get-pip.py

RUN python -m pip install termcolor
############## EOS FACTORY #############################################################################################

ARG eosfactory_branch=master

RUN git clone -b "$eosfactory_branch" https://github.com/tokenika/eosfactory.git /opt/eosfactory/
WORKDIR /opt/eosfactory/

RUN mkdir /opt/workspace
RUN ./build.sh -e /opt/eos -w /opt/workspace

RUN mkdir ~/eosio-wallet/

# https://superuser.com/a/1253889/59009
RUN sed -i 's/mesg n || true/tty -s \&\& mesg n || true/g' /root/.profile
RUN chmod +x ./tests/unittest.sh

WORKDIR /opt/eosfactory/tests/

# bash loads .profile by default
ENTRYPOINT ["/bin/bash", "-l", "-c"]
