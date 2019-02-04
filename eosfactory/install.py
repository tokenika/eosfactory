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
    
    current_path_color = "green"
    error_path_color = "red"

    while True:
        map = config.config_map()
        contract_workspace_dir = None

        if config.contract_workspace_[0] in map:
            contract_workspace_dir = map[config.contract_workspace_[0]]
            _contract_workspace_dir = tilde(input(utils.heredoc('''
                Where do you prefer to keep your smart-contract projects?
                The current location is:
                {}
                Input another existing directory path, or nothing to keep the current one:
                ''').format(colored(contract_workspace_dir, current_path_color)) + "\n"))
        else:
            _contract_workspace_dir = tilde(input(utils.heredoc('''
                Where do you prefer to keep your smart-contract projects?
                Input an existing directory path:
                ''') + "\n"))
        if not _contract_workspace_dir:
            _contract_workspace_dir = contract_workspace_dir
        
        if _contract_workspace_dir and os.path.exists(
                _contract_workspace_dir) and os.path.isdir(
                    _contract_workspace_dir):
            map = config.config_map()
            map[config.contract_workspace_[0]] = _contract_workspace_dir
            config.write_config_map(map)
            print()
            break
        
        print("\n" + utils.heredoc('''
        The path you entered:
        {}
        doesn't seem to exist!
        ''').format(colored(_contract_workspace_dir, error_path_color)) + "\n")

        
parser = argparse.ArgumentParser(description='''
''')

install()