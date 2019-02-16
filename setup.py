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
    with open('README.rst') as f:
        return f.read()

def data_files_(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            dir = os.path.join(config.EOSFACTORY_DIR, path)
            if "build" in dir:
                continue
            file_list = [os.path.join(path, filename)]
            tuple = (dir, file_list)
            paths.append(tuple)
    return paths

data_files = [
    (config.EOSFACTORY_DIR, ["wsl_root.sh"]),
    (os.path.join(config.EOSFACTORY_DIR, "config"),
        ["config/distributed/config.json", "config/config.ini", 
                                                    "config/genesis.json"])] 
data_files.extend(data_files_('templates'))
data_files.extend(data_files_('contracts'))

setuptools.setup(
    name=setuptools_name,
    version=config.VERSION,
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
    install_requires=['termcolor',],
    include_package_data = True,
    data_files=data_files,
    zip_safe=False)

