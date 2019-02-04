import setuptools
import os
import eosfactory.core.config as config
from shutil import rmtree

setuptools_name = config.SETUPTOOLS_NAME

try:
    rmtree("build")
except:
    pass

try:
    rmtree("dist")
except:
    pass

try:
    rmtree(setuptools_name + ".egg-info")
except:
    pass

def readme():
    with open('README.md') as f:
        return f.read()

setuptools.setup(
    name=setuptools_name,
    version='2.1.0',
    description='Python-based EOS smart-contract development & testing framework',
    long_description=readme(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        'Topic :: Software Development :: Testing',
    ],
    keywords='EOSIO, smart contract unit testing',
    url='https://github.com/tokenika/eosfactory',
    author='Tokenika',
    author_email='contact@tokenika.io',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
        'termcolor',
    ],
    zip_safe=False)

