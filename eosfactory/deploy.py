import os
import argparse

import eosfactory.core.errors as errors
import eosfactory.core.testnet
import eosfactory.core.teos as teos
import eosfactory.shell.account as account
import eosfactory.shell.contract as contract

def deploy(
        contract_dir="",
        testnet_account_name="",
        c_cpp_properties_path="", 
        silent=False):

    if not contract_dir:
        contract_dir = os.getcwd()
    verbosity=[] if silent else None

    if not testnet_account_name:
        c_cpp_properties = teos.get_c_cpp_properties(
                                        contract_dir, c_cpp_properties_path)
        if not c_cpp_properties:
            raise errors.Error('''
                The testnet account is not set and it can not be found any 
                c_cpp_properties json file.
                ''')
        if not "contractAccount" in c_cpp_properties:
            raise errors.Error('''
                The testnet account is not set and it can not be found in a 
                c_cpp_properties json file.
                ''')

        testnet_account_name = c_cpp_properties["contractAccount"]["template"]
    
    testnet_account = eosfactory.core.testnet.get_testnet(testnet_account_name)
    if not testnet_account:
        raise errors.Error('''
        There is not any testnet account named '{}' in the list. 
        Use the bash command 
        `python3 -m eosfactory.register_testnet -h`
        to get instructions how to register a testnet account.
        '''.format(testnet_account_name))
    
    testnet_account.configure()
    testnet_account.verify_production()
    contract_account = account.restore_account(
                                        testnet_account_name, testnet_account)
    contract.Contract(contract_account).deploy()

def main():
    '''
    usage: python3 -m eosfactory.deploy.py [-h] [--dir DIR] 
                                                [--c_cpp_prop C_CPP_PROP]
                                                [--testnet TESTNET] [--silent]

    Deploy a given contract to a given account.
    
    The contract is determined with its project directory. The directory may be
    absolute or relative to the *contract workspace* directory as defined with
    :func:`.core.config.contract_workspace_dir(). If the *dir* argument is not set,
    it is substituted with the current working directory.

    The contract account is determined with the name of *Testnet* object in the
    :func:`.core.testnet.testnets()` list. If the *template* argument is not 
    set, is is substituted with the value of the key  
    ["contractAccount"]["template"] of the json file given with the argument
    *c_cpp_prop* -- if it is set -- of 
    *.vscode/c_opp_properties.json* in the project's directory, otherwise.

    Args:
        --dir: Contract name or directory.
        --c_cpp_prop: c_cpp_properties.json file path.        
        --testnet: Testnet account.
        --silent: Do not print info.
        -h: Show help message and exit
    '''
    parser = argparse.ArgumentParser(description='''
    Deploy a contract to an account.
    
    The contract is determined with its project directory. The directory may be
    absolute or relative to the *contract workspace* directory as defined with
    :func:`.core.config.contract_workspace_dir(). If the *dir* argument is not set,
    it is substituted with the current working directory.

    The contract account is determined with the name of *Testnet* object in the
    :func:`.core.testnet.testnets()` list. If the *template* argument is not 
    set, is is substituted with the value of the key  
    ["contractAccount"]["template"] of the json file given with the argument
    *c_cpp_prop* -- if it is set -- or with the file 
    *.vscode/c_opp_properties.json* in the project's directory, otherwise.
    ''')

    parser.add_argument("--dir", help="Contract name or directory.", default="")
    parser.add_argument(
        "--c_cpp_prop", help="c_cpp_properties.json file path.", default="")
    parser.add_argument(
        "--testnet", help="Testnet account.", default="")
    parser.add_argument(
        "--silent", help="Do not print info.", action="store_true")


    args = parser.parse_args()
    deploy(args.dir, args.testnet, args.c_cpp_prop, args.silent)    

if __name__ == '__main__':
    main()
