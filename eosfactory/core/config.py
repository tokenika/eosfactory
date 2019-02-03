import os
import argparse
import json
import re

import eosfactory.core.errors as errors
import eosfactory.core.logger as logger
import eosfactory.core.utils as utils

VERSION = "2.1.0"
EOSIO_VERSION = "1.6.0"
EOSIO_CDT_VERSION = "1.4.1"
PYTHON_VERSION = "3.5 or higher"
APP_DATA_DIR = "/usr/local/eosfactory/"
SETUPTOOLS_NAME = "eosfactory_tokenika"

LOCALHOST_HTTP_ADDRESS = "127.0.0.1:8888"
contractsDir = "contracts"
DEFAULT_TEMPLATE = "01_hello_world"
FROM_HERE_TO_EOSF_DIR = "../../../"
CONFIG_JSON = "config/config.json"
CONTRACTS_DIR = "contracts/"
EOSIO_CPP_DIR = "/usr/opt/eosio.cdt/0.0.0/"

node_address_ = ("LOCAL_NODE_ADDRESS", [LOCALHOST_HTTP_ADDRESS])
wallet_address_ = ("WALLET_MANAGER_ADDRESS", [LOCALHOST_HTTP_ADDRESS])
genesis_json_ = ("EOSIO_GENESIS_JSON", 
                ["/home/cartman/.local/share/eosio/nodeos/config/genesis.json"])
data_dir_ = ("LOCAL_NODE_DATA_DIR", 
                            ["/home/cartman/.local/share/eosio/nodeos/data/"])
config_dir_ = ("LOCAL_NODE_CONFIG_DIR", 
                            ["/home/cartman/.local/share/eosio/nodeos/config/"])
keosd_wallet_dir_ = ("KEOSD_WALLET_DIR", ["${HOME}/eosio-wallet/"])
chain_state_db_size_mb_ = ("EOSIO_SHARED_MEMORY_SIZE_MB", ["200"])

wsl_root_ = ("WSL_ROOT", [None])
nodeos_stdout_ = ("NODEOS_STDOUT", [None])


cli_exe_ = ("EOSIO_CLI_EXECUTABLE", ["/usr/bin/cleos"])
keosd_exe_ = ("KEOSD_EXECUTABLE", ["/usr/bin/keosd"])
node_exe_ = ("LOCAL_NODE_EXECUTABLE", ["/usr/bin/nodeos"])
eosio_cpp_ = ("EOSIO_CPP", ["/usr/bin/eosio-cpp"])
eosio_cpp_dir_ = ("EOSIO_CPP_DIR", [EOSIO_CPP_DIR])
eosio_cpp_includes_ = (
    "EOSIO_CPP_INCLUDES", 
    [["include", "include/eosiolib", "include/libc", "include/libcxx"]])

key_private_ = (
    "EOSIO_KEY_PRIVATE", 
    ["5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"])
key_public_ = (
    "EOSIO_KEY_PUBLIC",
    ["EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"])
contract_workspace_ = (
    "EOSIO_CONTRACT_WORKSPACE", [CONTRACTS_DIR])


def eosf_dir():
    '''The absolute directory of the EOSFactory installation.
    '''
    path = os.path.realpath(os.path.join(__file__, FROM_HERE_TO_EOSF_DIR))
    if os.path.exists(path):
        return path

    raise errors.Error('''
        Cannot determine the root directory of EOSFactory.
        It is attempted to be derived from the path of the configuration file
            '{}'.
        Therefore, this file has to remain in its original position.
        Currently, its path is '{}'.
    '''.format(__file__, path))


def eosio_key_private():
    '''*eosio* account private key.
    
    A private key used as the value of the option *signature-provider* in
    the command line for the *nodeos* executable. 
    
    It may be changed with 
    *EOSIO_KEY_PRIVATE* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    return config_value_checked(key_private_)


def eosio_key_public():
    '''*eosio* account public key.
    
    A public key used as the value of the option *signature-provider* in
    the command line for the *nodeos* executable.

    It may be changed with 
    *EOSIO_KEY_PUBLIC* entry in the *config.json* file, 
    see :func:`.current_config`.    
    '''
    return config_value_checked(key_public_)


def data_dir():
    '''Directory containing runtime data of *nodeos*.

    It may be changed with 
    *LOCAL_NODE_DATA_DIR* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    return first_valid_path(data_dir_)
    

def config_dir():
    '''Directory containing configuration files such as config.ini.

    It may be changed with 
    *LOCAL_NODE_CONFIG_DIR* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    return first_valid_path(config_dir_)


def genesis_json():
    '''File to read Genesis State from.

    It may be changed with 
    *EOSIO_GENESIS_JSON* entry in the *config.json* file, 
    see :func:`.current_config`.    
    '''
    return first_valid_path(genesis_json_)


def chain_state_db_size_mb():
    '''The size of the buffer of the local node. 

    The value of the option *chain-state-db-size-mb* in the command line for 
    the *nodeos* executable.

    It may be changed with 
    *EOSIO_SHARED_MEMORY_SIZE_MB* entry in the *config.json* file, 
    see :func:`.current_config`.  
    '''
    return config_value_checked(chain_state_db_size_mb_)


def wsl_root():
    '''The root directory of the Windows WSL.
    
    The root directory of the Ubuntu file system, owned by the installation,
    if any, of the Windows Subsystem Linux (WSL).

    It may be changed with 
    *WSL_ROOT* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    path = config_value(wsl_root_)
    if path is None:
        return None
    else:
        path = path.strip()
    return path.replace("\\", "/")


def nodeos_stdout():
    '''Set *stdout* file for the *stdout* stream of the local node.

    If the value of *NODEOS_STDOUT* entry in the *config.json* file is set,
    the local node logs to the specified file its output, 
    see :func:`.current_config`.

    Note:
        The same may be achieved with the *nodeos_stdout* argument in the
        function :func:`.core.manager.resume`.
    '''
    return config_value(nodeos_stdout_)


def http_server_address():
    '''The http/https URL where local *nodeos* is running.

    The setting may be changed with 
    *LOCAL_NODE_ADDRESS* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    return config_value_checked(node_address_)


def http_wallet_address():
    '''The http/https URL where keosd is running.

    The setting may be changed with 
    *WALLET_MANAGER_ADDRESS* entry in the *config.json* file, 
    see :func:`.current_config`.    
    '''
    retval = config_value(wallet_address_)
    if not retval:
        retval = http_server_address()
    return retval


def node_exe():
    '''The path to the *nodeos* executable.

    The setting may be changed with 
    *LOCAL_NODE_EXECUTABLE* entry in the *config.json* file, 
    see :func:`.current_config`.    
    '''
    return first_valid_path(node_exe_) 


def cli_exe():
    '''The path to the *cleos* executable.
    
    The setting may be changed with 
    *EOSIO_CLI_EXECUTABLE* entry in the *config.json* file, 
    see :func:`.current_config`.    
    '''
    return first_valid_path(cli_exe_)


def keosd_exe():
    '''The path to the *keosd* executable.
    
    The setting may be changed with 
    *KEOSD_EXECUTABLE* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    return first_valid_path(keosd_exe_)


def eosio_cpp():
    '''The path to the *eosio-cpp* executable.
    
    The setting may be changed with 
    *EOSIO_CPP* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    return first_valid_path(eosio_cpp_)


def eosio_cpp_dir():
    '''The path to the *eosio-cpp* installation directory.
    
    The setting may be changed with 
    *EOSIO_CPP* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    eosio_cpp_version = utils.process(
            [eosio_cpp(), "-version"],
            "Cannot determine the version of the expected 'eosio.cpp' package."
        ).replace("eosio-cpp version ", "")
    version_pattern = re.compile(".+/eosio\.cdt/(\d\.\d\.\d)/$")
    dir = eosio_cpp_dir_[1][0]    
    if not version_pattern.match(dir):
        raise errors.Error(
            '''
The assumed pattern
{}
does not match the directory template 'core.config.EOSIO_CPP_DIR'
{}
            '''.format(version_pattern, EOSIO_CPP_DIR)
        )
    dir = dir.replace(
        re.findall(version_pattern, dir)[0], eosio_cpp_version) 

    return dir   


def eosio_cpp_includes():
    '''The list of eosio cpp_ includes.
    
    The setting may be changed with 
    *EOSIO_CPP* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    list = []
    dir = eosio_cpp_dir()
    for include in eosio_cpp_includes_[1][0]:
        list.append(dir + include)
    return list


def keosd_wallet_dir(raise_error=True):
    '''The path to the local wallet directory.

    The path is hard-coded in the *keosd* wallet manager.

    Args:
        raise_error (bool): If set, rise an error if the path is invalid.

    Raises:
        .core.errors.Error: If the directory does not exist.
    '''
    return first_valid_path(keosd_wallet_dir_, raise_error=raise_error)


def config_file():
    '''The path to the *config.json* file.
    '''
    file = os.path.join(eosf_dir(), CONFIG_JSON)
        
    if not os.path.exists(file):
        with open(file, "w") as output:
            output.write("{}")

            logger.INFO('''
        Cannot find the config file. It is expected to be 
            '{}'.
        Creating an empty config file there.
            '''.format(file))

    return file


def config_map():
    '''Return a JSON object read from the *config.json* file.

    Raises:
        .core.errors.Error: If the JSON object cannot be returned.
    '''
    path = config_file()
    if os.path.exists(path):
        try:
            with open(path, "r") as input:
                text = input.read()
                if not text:
                    return {}
                else:
                    return json.loads(text)
        except Exception as e:
            raise errors.Error(str(e))

    raise errors.Error('''
Cannot find the config file.       
    ''')


def write_config_map(map):
    '''Write the given json object to *config.json*.

    Args:
        map (json): The json object to be saved.

    Raises:
        .core.errors.Error: If the JSON object cannot be saved.        
    '''
    path = config_file()
    if os.path.exists(path):
        with open(path, "w+") as output:
            output.write(json.dumps(map, indent=4))
        return

    raise errors.Error('''
Cannot find the config file.       
    ''')
    

def config_values(config_list):
    '''List values ascribed to the key of a hard-codded configuration list.

    First, consider the *config.json*, next the values of the hard-codded 
    configuration list.

    Args:
        config_list (tuple): A configure list tuple.
    '''
    config_key = config_list[0]

    retval = []
    # First, configure file ...
    config_json = config_map()
    if config_key in config_json and config_json[config_key]:
        retval.append(config_json[config_key])
        return retval

    # Finally, hard-codded values, if any.
    values = config_list[1]
    if values:
        return values

    return retval


def config_value(config_list):
    '''Get the first item from :func:`.config_values`.

    Args:
        config_list (()): A configure list tuple.    
    '''
    retval = config_values(config_list) 
    return retval[0] if retval else None


def config_value_checked(config_list):
    '''Get the first item from :func:`.config_values`. Raise an error if fails.

    Args:
        config_list (tuple): A configure list tuple.  

    Raises:
        .core.errors.Error: If the result is not defined.
    '''
    retval = config_value(config_list)
    if not retval is None:
        return retval

    raise errors.Error('''
The value of {} is not defined.
Define it in the config file
{}       
    '''.format(config_list[0], config_file()))


def first_valid_path(config_list, find_file=None, raise_error=True):
    '''Given a key to the config list, get a valid file system path.

    Applicable if the *config_list* argument refers to a file path.
    The path may be absolute or relative to the root of the EOSFactory 
    installation.
    
    Also, the path may be relative to the *HOME* environment variable.

    Args:
        config_list (tuple): A configure list tuple.
        find_file (str): If set, the given file has to exist.
        raise_error (bool): If set, raise an error on failure.
        
    Raises:
        .core.errors.Error: If the *raise_error* argument is set and the \
            result is not defined.            
    '''
    values = config_values(config_list)
    for path in values:

        if "${HOME}" in path: 
            home = None
            if "HOME" in os.environ:
                home = os.environ["HOME"]
                
            if home:
                path = path.replace("${HOME}", home)
                if find_file: 
                    if os.path.exists(os.path.join(path, find_file)):
                        return path
                else:
                    if os.path.exists(path):
                        return path

        if os.path.isabs(path):
            if find_file:
                if os.path.exists(os.path.join(path, find_file)):
                    return path
            else:
                if os.path.exists(path):
                    return path
        else:
            full_path = os.path.join(eosf_dir(), path)
            if find_file:
                if os.path.exists(os.path.join(full_path, find_file)):
                    return full_path
            else:
                if os.path.exists(full_path):
                    return full_path        

    if raise_error:
        raise errors.Error('''
        Cannot find any path for '{}'.
        '''.format(config_list[0]))


def contract_dir(contract_dir_hint):
    '''Given a hint, determine the contract root directory.

    The ``contract_dir_hint`` is tested to be either
        - an absolute path, or
        - a path relative to either
            - the directory given with :func:`contract_workspace`, or
            - the directory given with :func:`eosf_dir` ``/contracts``.

    Args:
        contract_dir_hint (path): A directory path, may be not absolute.
        
    Raises:
        .core.errors.Error: If the result is not defined.
    '''
    contract_dir_hint = utils.wslMapWindowsLinux(contract_dir_hint)

    # ? the absolute path to a contract directory
    trace = contract_dir_hint + "\n"
    if os.path.isfile(contract_dir_hint):
        contract_dir_hint = os.path.dirname(contract_dir_hint)
    if os.path.isabs(contract_dir_hint):
        return contract_dir_hint

    # ? the relative path to a contract directory, relative to the directory 
    # set with the 'contract_workspace()' function
    contract_dir_ = os.path.join(
        config_value(contract_workspace_), contract_dir_hint)
    trace = trace + contract_dir_ + "\n"
    if os.path.isdir(contract_dir_):
        return os.path.abspath(contract_dir_)

    # ? the relative path to a contract directory, relative to the 
    # set with the 'eosf_dir() / contracts' function
    contract_dir_ = os.path.join(
            eosf_dir(), 
            CONTRACTS_DIR, contract_dir_hint)
    trace = trace + contract_dir_ + "\n"
    if os.path.isdir(contract_dir_):
        return os.path.abspath(contract_dir_)
    
    raise errors.Error('''
        Cannot determine the contract directory.
        Tried path list:
        {}
    '''.format(trace))


def source_files(source_dir):
    '''List files CPP/C and ABI files from the given directory
    '''
    srcs = []
    extensions = [".cpp", ".cxx", ".c", ".abi"]
    files = os.listdir(source_dir)
    for file in files:
        path = os.path.join(source_dir, file)
        if os.path.splitext(file)[1] in extensions:
            if os.path.isfile(path):
                srcs.append(path)
    return srcs
    

def contract_source_files(contract_dir_hint):
    '''List files CPP/C and ABI files from directory given with a hint.

    Args:
        contract_dir_hint (str): An argument to the function 
            :func:`.contract_dir`

    Raises:
        .core.errors.Error: If the list is empty.
    '''
    contract_dir_ = contract_dir(utils.wslMapWindowsLinux(contract_dir_hint))
    trace = contract_dir_ + "\n"

    source_dir = contract_dir_
    srcs = source_files(source_dir)
    if srcs:
        return (source_dir, srcs)            

    source_dir = os.path.join(contract_dir_, "src")
    trace = trace + source_dir + "\n"
    srcs = source_files(source_dir)
    if srcs:
        return (source_dir, srcs)            

    raise errors.Error('''
        Cannot find any contract source directory.
        Tried path list:
        {}
    '''.format(trace))


def contract_file(contract_dir_hint, contract_file_hint):
    ''' Given contract directory and contract file hints, determine a contract 
    file.

    The contract directory is determined with the function 
    :func:`.contract_dir`, basing on the *contract_dir_hint* argument.

    Contract files are ABI or WASM ones. Contract file hint is an absolute path
    to a contract file, or it is relative to the contract dir, ir it is 
    a file extension.

    Any contract directory considered to be structured according to one of the 
    following patterns:

        - all the files in the contract directory,
        - contract files in the *build* subdirectory.  

    Args:
        contract_dir_hint (path): A directory path, may be not absolute.
        contract_file_hint (str or path): A file extension, or file path, 
            may be not absolute.

    Raises:
        .core.errors.Error: If the result is not defined.
    '''
    contract_dir_hint = utils.wslMapWindowsLinux(contract_dir_hint)
    contract_file_hint = utils.wslMapWindowsLinux(contract_file_hint)

    # Contract file hint is an absolute path to a contract file:
    trace = contract_file_hint + "\n" 
    if os.path.isabs(contract_file_hint) \
                                    and os.path.isfile(contract_file_hint):
        return contract_file_hint

    contract_dir_ = contract_dir(contract_dir_hint)

    # All the files in the contract directory:
    contract_file = os.path.join(contract_dir_, contract_file_hint)
    trace = trace + contract_file + "\n"
    if os.path.isfile(contract_file):
        return contract_file

    # Contract files in the *build* subdirectory,
    # and *contract_file_hint* is a relative file
    contract_file = os.path.join(contract_dir_, "build", contract_file_hint)
    trace = trace + contract_file + "\n"
    if os.path.isfile(contract_file):
        return contract_file

    # Contract files in the *build* subdirectory,
    # and *contract_file_hint* is a file extension merely
    build_dir = os.path.join(contract_dir_, "build")
    trace = trace + build_dir + "\n"
    files = os.listdir(build_dir)
    for file in files:
        if os.path.splitext(file)[1] == contract_file_hint:
            return os.path.join(build_dir, file)

    raise errors.Error('''
        Cannot determine the contract file basing on hints:
        contract dir hint: {}
        contract file hint: {}
        Tried path list:
        {}
    '''.format(contract_dir_hint, contract_file_hint, trace))  


def contract_workspace():
    '''The absolute path to the contract workspace of the user.

    The contract workspace is a directory where automatically created projects
    are placed by default. It is set while the EOSFactory is installed. 

    If not set, the projects are stored in the *contracts* directory of the 
    EOSFActory installation.

    The setting may be changed with 
    *EOSIO_CONTRACT_WORKSPACE* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    workspacePath = config_value(contract_workspace_)
    trace = workspacePath + "\n"
    
    if not os.path.isabs(workspacePath):
        workspacePath = os.path.join(eosf_dir(), workspacePath)
        trace = trace + workspacePath + "\n"
    if os.path.exists(workspacePath):
        return workspacePath

    raise errors.Error('''
        Cannot determine the contract workspace.
        Tried path list:
        {}
    '''.format(trace))


def abi_file(contract_dir_hint):
    '''Given a contract directory hint, return the ABI file path.
    See :func:`contract_file`.

    Args:
        contract_dir_hint: A directory path, may be not absolute.

    Raises:
        .core.errors.Error: If the result is not defined.
    '''
    return os.path.relpath(
        contract_file(contract_dir_hint, ".abi"), contract_dir_hint)


def wast_file(contract_dir_hint):
    '''Given the contract directory, return the WAST file path.
    See :func:`contract_file`.

    Args:
        contract_dir_hint: A directory path, may be not absolute.

    Raises:
        .core.errors.Error: If the result is not defined.    
    '''
    return os.path.relpath(
        contract_file(contract_dir_hint, ".wast"), contract_dir_hint)


def wasm_file(contract_dir_hint):
    '''Given the contract directory, return the WASM file path.
    See :func:`contract_file`.
    
    Args:
        contract_dir_hint: A directory path, may be not absolute.

    Raises:
        .core.errors.Error: If the result is not defined.    
    '''
    return os.path.relpath(
        contract_file(contract_dir_hint, ".wasm"), contract_dir_hint)


def update_eosio_cpp_includes(c_cpp_properties_path, root=""):
    c_cpp_properties_path = utils.wslMapWindowsLinux(c_cpp_properties_path)
    with open(c_cpp_properties_path) as f:
        c_cpp_properties = f.read()

    dir_pattern = re.compile(
        '^.*{}(/.+/eosio\.cdt/\d\.\d\.\d/).+'.format(root), re.M)

    dir = eosio_cpp_dir()
    if re.findall(dir_pattern, c_cpp_properties):
        new = c_cpp_properties.replace(re.findall(
                                        dir_pattern, c_cpp_properties)[0], dir)
        if not new == c_cpp_properties:
            with open(c_cpp_properties_path,'w') as f:
                f.write(new)


def not_defined():
    map = current_config()
    retval = {}
    for key, value in map.items():
        if value == None or value is None:
            retval[key] = value
    return retval


def installation_dependencies():
    '''Verify whether 'eosio' and 'eosio.cpp' packages are properly installed.
    '''
    eosio_version = utils.process(
                            [node_exe(), "--version"],
                            raise_exception=False)
    if not eosio_version[1]:
        eosio_version = eosio_version[0].replace("v", "")
        if not eosio_version == EOSIO_VERSION:
            print('''NOTE!
The version of the installed 'eosio' package is {} while the expected
version is {}
            '''.format(eosio_version, EOSIO_VERSION))
    else:
        print('''ERROR!
Cannot determine the version of the expected 'eosio' package.
The error message:
{}
        '''.format(eosio_version[1]))

    eosio_cpp_version = utils.process(
                            [eosio_cpp(), "-version"],
                            raise_exception=False)
    if not eosio_cpp_version[1]:
        eosio_cpp_version = eosio_cpp_version[0].replace(
                                                    "eosio-cpp version ", "")
        if not eosio_cpp_version == EOSIO_CDT_VERSION:
            print('''NOTE!
The version of the installed 'eosio.cpp' package is {} while the expected
version is {}
            '''.format(eosio_cpp_version, EOSIO_CDT_VERSION))
    else:
        print('''ERROR!
Cannot determine the version of the expected 'eosio.cpp' package.
The error message:
{}
        '''.format(eosio_cpp_version[1]))    


def current_config(contract_dir=None):
    '''Present the current configuration.

    The current configuration result from both the *config.json* file setting
    and default hard-codded setup. The *config.json* prevails.

    Args:
        contract_dir str(): If set

    Note:
        The current configuration can be seen with the bash command:

        *python3 -m eosfactory.core.config*
    '''
    map = {}
    
    map["CONFIG_FILE"] = config_file()
    try:
        map["EOS_FACTORY_DIR"] = eosf_dir()
    except:
        map["EOS_FACTORY_DIR"] = None
    try:
        map[node_address_[0]] = http_server_address()
    except:
        map[node_address_[0]] = None
    try:     
        map[key_private_[0]] = eosio_key_private()
    except:
        map[key_private_[0]] = None
    try:  
        map[key_public_[0]] = eosio_key_public()
    except:
        map[key_public_[0]] = None
    try:
        map[wsl_root_[0]] = wsl_root()
    except:
        map[wsl_root_[0]] = None
    try:
        map[wallet_address_[0]] = http_wallet_address() \
                if http_wallet_address() else http_server_address()
    except:
        map[wallet_address_[0]] = None
    try:
        map[chain_state_db_size_mb_[0]] = chain_state_db_size_mb()
    except:
        map[chain_state_db_size_mb_[0]] = None
    try:
        map[contract_workspace_[0]] = config_value_checked(contract_workspace_)
    except:
         map[contract_workspace_[0]] = None
    try:
        map[keosd_wallet_dir_[0]] = keosd_wallet_dir()   
    except:
        map[keosd_wallet_dir_[0]] = None
    try: 
        map[data_dir_[0]] = data_dir()
    except:
        map[data_dir_[0]] = None 
    try:    
        map[config_dir_[0]] = config_dir()
    except:
        map[config_dir_[0]] = None   
    try: 
        map[cli_exe_[0]] = cli_exe()
    except:
        map[cli_exe_[0]] = None 
    try: 
        map[keosd_exe_[0]] = keosd_exe()
    except:
        map[keosd_exe_[0]] = None 
    try: 
        map[node_exe_[0]] = node_exe()
    except:
        map[node_exe_[0]] = None
    try: 
        map[eosio_cpp_[0]] = eosio_cpp()
    except:
        map[eosio_cpp_[0]] = None
    try: 
        map[eosio_cpp_dir_[0]] = eosio_cpp_dir()
    except:
        map[eosio_cpp_dir_[0]] = None
    try: 
        map[eosio_cpp_includes_[0]] = eosio_cpp_includes()
    except:
        map[eosio_cpp_includes_[0]] = None        
                                      
    try:   
        map[genesis_json_[0]] = genesis_json()
    except:
        map[genesis_json_[0]] = None

    map[nodeos_stdout_[0]] = nodeos_stdout()
    
    if contract_dir:
        contract_dir = contract_dir(contract_dir)
        try:
            map["contract-dir"] = contract_dir
        except:
            map["contract-dir"] = None
        try:
            map["contract-wast"] = wast_file(contract_dir)
        except:
            map["contract-wast"] = None
        try:
            map["contract-wasm"] = wasm_file(contract_dir)
        except:
            map["contract-wasm"] = None
        try:
            map["contract-abi"] = abi_file(contract_dir)
        except:
            map["contract-abi"] = None

    return map        


def config():
    print('''
EOSFactory version {}.
Dependencies:
https://github.com/EOSIO/eos version {}
https://github.com/EOSIO/eosio.cdt version {}
Python version {}
    '''.format(VERSION, EOSIO_VERSION, EOSIO_CDT_VERSION, PYTHON_VERSION)
    )

    installation_dependencies()

    print('''
The current configuration of EOSFactory:
{}

You are free to overwrite the above settings with entries in the configuration 
file located here:
{}
'''.format(
        json.dumps(
            current_config(), sort_keys=True, indent=4), config_file())
    )

    not_defined_ = not_defined()
    if not_defined_:
        print('''
There are undefined setting:
{}
    '''.format(json.dumps(not_defined_, sort_keys=True, indent=4)))

    print('''
The current contents of the configuration file is:
{}
'''.format(
        json.dumps(config_map(), sort_keys=True, indent=4))
    )


def main():
    '''
    usage: config.py [-h] [--json]

    Show the configuration of EOSFactory.

    Args:
        --json: Print bare JSON only.
        -h: Show help message and exit.
    '''

    parser = argparse.ArgumentParser(description='''
    Show the configuration of EOSFactory.
    ''')
    parser.add_argument("--dependencies", action="store_true")
    parser.add_argument("--json", help="Bare JSON only.", action="store_true")
    args = parser.parse_args()
    if args.dependencies:
        installation_dependencies()
    elif args.json:
        print(json.dumps(
            current_config(), sort_keys=True, indent=4))
    else:
        config()    

if __name__ == '__main__':
    main()






