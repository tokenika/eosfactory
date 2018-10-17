import os
from termcolor import cprint, colored
import argparse
import pathlib

import eosfactory.core.utils as utils
import eosfactory.core.config as config


def tilde(tilde_path):
    return tilde_path.replace("~", str(pathlib.Path.home()))


def install(wsl_root):
    if wsl_root:
        map = config.config_map()
        map[config.wsl_root_[0]] = wsl_root
        config.write_config_map(map)
    
    current_path_color = "green"
    error_path_color = "red"

    while True:
        map = config.config_map()
        eosio_repository_dir = None

        if config.eosio_repository_dir_[0] in map:
            eosio_repository_dir = map[config.eosio_repository_dir_[0]]
            _eosio_repository_dir = tilde(input(utils.heredoc('''
                Where is the EOSIO repository located on your machine?
                The current location is:
                {}
                Input another existing directory path, or nothing to keep the current one:
                ''').format(colored(eosio_repository_dir, current_path_color)) + "\n"))
        else:
            _eosio_repository_dir = tilde(input(utils.heredoc('''
                Where is the EOSIO repository located on your machine?
                Input an existing directory path:
                ''') + "\n"))

        if not _eosio_repository_dir:
            _eosio_repository_dir = eosio_repository_dir

        ok = os.path.exists(os.path.join(_eosio_repository_dir, config.node_exe_[1][0]))

        if ok:
            map = config.config_map()
            map[config.eosio_repository_dir_[0]] = _eosio_repository_dir
            config.write_config_map(map)
            print()
            break

        print("\n" + utils.heredoc('''
        The path you entered:
        {}
        doesn't seem to be correct! EOSIO executables are not detected there.
        ''').format(colored(_eosio_repository_dir, error_path_color)) + "\n")

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
        
        if os.path.exists(_contract_workspace_dir) and os.path.isdir(_contract_workspace_dir):
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

parser.add_argument("root", default=None, help="WSL root path")
args = parser.parse_args()
install(args.root)