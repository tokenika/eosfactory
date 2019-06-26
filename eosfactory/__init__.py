'''Library for development and tests of the EOSIO smart contracts.

.. moduleauthor:: Tokenika
'''
import sys

try:
    import psutil
except ImportError:
    print('''
Module 'psutil' is not installed. Please, install it:
pip3 install --user psutil

Exiting ...
    ''')
    exit(-1)

try:
    import termcolor
except ImportError:
    print('''
Module 'termcolor' is not installed. Please, install it:
pip3 install --user termcolor

Exiting ...
    ''')
    exit(-1)

import eosfactory.core.config

name = "eosfactory"

__version__ = eosfactory.core.config.VERSION