ARG eos_branch=v1.3.1
ARG eos_symbol=SYS

FROM tokenika/eosio:${eos_branch}

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
############## EOS CDT #############################################################################################

RUN wget https://github.com/eosio/eosio.cdt/releases/download/v1.4.1/eosio.cdt-1.4.1.x86_64.deb && \
    apt install ./eosio.cdt-1.4.1.x86_64.deb \
    && rm ./eosio.cdt-1.4.1.x86_64.deb

############## EOS FACTORY #############################################################################################

ARG eosfactory_branch=master
RUN git clone -b "$eosfactory_branch" https://github.com/tokenika/eosfactory.git /opt/eosfactory/
WORKDIR /opt/eosfactory/
RUN git branch
RUN git log -10 --oneline

RUN mkdir /opt/workspace
RUN mkdir ~/eosio-wallet/

RUN python -m pip install wheel twine

# replace version X.Y.Z in setup.py for X.Y.Z_test_<epoch_time>
RUN sed -i "s/version='\(.*\)'/version='\1.`date +%s`'/g" setup.py
RUN sed -n "s/\s*version='\(.*\)',/\1/p" setup.py > ./EOS_FACTORY_TEST_VERSION

RUN python setup.py sdist bdist_wheel

ARG test_pypi_password
RUN twine upload -u tokenika -p $test_pypi_password --repository-url https://test.pypi.org/legacy/ dist/*

WORKDIR /opt/eosfactory/tests/

RUN pip freeze
RUN python -m pip install --index-url https://test.pypi.org/simple/ eosfactory==$(cat ./../EOS_FACTORY_TEST_VERSION)
RUN pip freeze

# https://superuser.com/a/1253889/59009
RUN sed -i 's/mesg n || true/tty -s \&\& mesg n || true/g' /root/.profile
RUN chmod +x ./unittest.sh


# bash loads .profile by default
ENTRYPOINT ["/bin/bash", "-l", "-c"]
