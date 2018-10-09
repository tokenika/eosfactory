import os
from termcolor import cprint, colored
import argparse

import eosfactory.core.utils as utils
import eosfactory.core.config as config

def install(wsl_root):
    if wsl_root:
        map = config.config_map()
        map[config.wsl_root_[0]] = wsl_root
        config.write_config_map(map)
    
    current_color = "green"
    map = config.config_map()
    if config.contract_workspace_[0] in map:
        contract_workspace = input(utils.heredoc('''
            Where are kept contract projects?
            The current place is 
                {}
            Input another existing directory path, or nothing to keep the current one:
            ''').format(colored(
                    map[config.contract_workspace_[0]], 
                    current_color)) + "\n\t")
    else:
        contract_workspace = input(utils.heredoc('''
            Where are kept contract projects?
            Input an existing directory path:
            ''') + "\n\t")
    while True:
        if not contract_workspace: #/mnt/c/Workspaces/EOS/contracts
            print()
            break
        
        if contract_workspace:
            if os.path.exists(contract_workspace) and os.path.isdir(contract_workspace):
                map = config.config_map()
                map[config.contract_workspace_[0]] = contract_workspace
                config.write_config_map(map)
                print()
                break
            else:
                print(utils.heredoc('''
            {}
            is not an existing directory path.
                ''').format(colored(contract_workspace), current_color))

    map = config.config_map()
    if config.eosio_repository_dir_[0] in map: #/mnt/c/Workspaces/EOS/eos
        eosio_repository_dir = input(utils.heredoc('''
            Where is an eosio repository?
            The current place is 
                {}
            Input another existing directory path, or nothing to keep the current one:
            ''').format(colored(
                map[config.eosio_repository_dir_[0]],
                current_color)) + "\n\t")
    else:
        eosio_repository_dir = input(utils.heredoc('''
            Where is an eosio repository?
            Input an existing directory path:
            ''') + "\n\t")
    while True:
        if not eosio_repository_dir:
            print()
            break

        if eosio_repository_dir:
            config.eosio_repository_dir_[1][0] = eosio_repository_dir
            if config.node_exe() and  config.cli_exe():
                map = config.config_map()
                map[config.eosio_repository_dir_[0]] = eosio_repository_dir
                config.write_config_map(map)
                print()
                break
        else:
            print(utils.heredoc('''
            {}
            is not a satisfactory path as the eosio executables are not in their places.
                ''').format(colored(contract_workspace), current_color))

        
parser = argparse.ArgumentParser(description='''
''')

parser.add_argument("root", default=None, help="WSL root path")
args = parser.parse_args()
install(args.root)