import os
from termcolor import cprint, colored
import argparse
import pathlib

import eosfactory.core.utils as utils
import eosfactory.core.config as config


def tilde(tilde_path):
    return tilde_path.replace("~", str(pathlib.Path.home()))


def install(wsl_root=None):
    wsl_root = config.wsl_root()
    if wsl_root:
        print('''
The root is the Windows Subsystem Linux is
'{}'
        '''.format(wsl_root))
    
    config.set_contract_workspace_dir()
        
parser = argparse.ArgumentParser(description='''
''')

install()