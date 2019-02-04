import setuptools
import os
import eosfactory.core.config as config

def readme():
    with open('README.md') as f:
        return f.read()

def data_files_(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            dir = os.path.join(config.APP_DATA_DIR, path)
            file_list = [os.path.join(path, filename)]
            tuple = (dir, file_list)
            paths.append(tuple)
    return paths

data_files = [
    (config.APP_DATA_DIR, 
        ["config/config_distributed.json", "config/config.ini", 
                                                    "config/genesis.json"])] 
data_files.extend(data_files_('templates'))  

import pdb; pdb.set_trace()
setuptools.setup(
    name='eosfactory-tokenika',
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
    include_package_data = True,
    data_files=data_files,
    zip_safe=False)

