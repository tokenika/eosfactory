import os
import stat
import argparse
import json
import re
import subprocess

import eosfactory
import eosfactory.core.errors as errors
import eosfactory.core.logger as logger
import eosfactory.core.utils as utils


VERSION = "3.1.1"
EOSIO_VERSION = "1.7.1"
EOSIO_CDT_VERSION = "1.6.1"
PYTHON_VERSION = "3.5 or higher"
EOSFACTORY_DIR = "eosfactory/"
TMP = "/tmp/eosfactory/"
SETUPTOOLS_NAME = "eosfactory_tokenika"
VERSION_PATTERN = r".+/eosio\.cdt/(\d\.\d\.\d)/.*$"

LOCALHOST_HTTP_ADDRESS = "127.0.0.1:8888"
DEFAULT_TEMPLATE = "hello_world"
FROM_HERE_TO_EOSF_DIR = "../../../"
CONFIG_DIR = "config"
CONFIG_JSON = "config.json"
CONTRACTS_DIR = "contracts/"
TEMPLATE_DIR = ("TEMPLATE_DIR", "templates/contracts")

eosfactory_data_ = ("EOSFACTORY_DATA_DIR", 
            [os.path.expandvars("${HOME}/.local/" + EOSFACTORY_DIR),\
                "/usr/local/" + EOSFACTORY_DIR,],
            [])
node_address_ = ("LOCAL_NODE_ADDRESS", [LOCALHOST_HTTP_ADDRESS])
wallet_address_ = ("WALLET_MANAGER_ADDRESS", [LOCALHOST_HTTP_ADDRESS])
genesis_json_ = ("EOSIO_GENESIS_JSON", 
                ["/home/cartman/.local/share/eosio/nodeos/config/genesis.json"])
data_dir_ = ("LOCAL_NODE_DATA_DIR", 
                            ["/home/cartman/.local/share/eosio/nodeos/data/"])
config_dir_ = ("LOCAL_NODE_CONFIG_DIR", [None])
# config_dir_ = ("LOCAL_NODE_CONFIG_DIR", 
#                         ["/home/cartman/.local/share/eosio/nodeos/config/"])
keosd_wallet_dir_ = ("KEOSD_WALLET_DIR", ["${HOME}/eosio-wallet/"])
chain_state_db_size_mb_ = ("EOSIO_SHARED_MEMORY_SIZE_MB", ["300"])

wsl_root_ = ("WSL_ROOT", [None])
nodeos_stdout_ = ("NODEOS_STDOUT", [None])
includes_ = ("INCLUDE", "includes")
libs_ = ("LIBS", "libs")


cli_exe_ = ("EOSIO_CLI_EXECUTABLE", 
                        ["cleos", "/usr/bin/cleos", "/usr/local/bin/cleos"])
keosd_exe_ = ("KEOSD_EXECUTABLE", 
                        ["keosd","/usr/bin/keosd", "/usr/local/bin/keosd"])
node_exe_ = ("LOCAL_NODE_EXECUTABLE", 
                        ["nodeos","/usr/bin/nodeos", "/usr/local/bin/nodeos"])
eosio_cpp_ = ("EOSIO_CPP", 
            ["eosio-cpp", "/usr/bin/eosio-cpp", "/usr/local/bin/eosio-cpp"])
eosio_cdt_root_ = ("EOSIO_CDT_ROOT", 
    ["/usr/opt/eosio.cdt/0.0.0/", "/usr/local/Cellar/eosio.cdt/0.0.0/opt/eosio.cdt/"])
eosio_cpp_includes_ = (
    "EOSIO_CPP_INCLUDES", 
    [["include", "include/libcxx", "include/eosiolib/core", \
                                                "include/eosiolib/contracts"]])

key_private_ = (
    "EOSIO_KEY_PRIVATE", 
    ["5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"])
key_public_ = (
    "EOSIO_KEY_PUBLIC",
    ["EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"])
contract_workspace_dir_ = (
    "EOSIO_CONTRACT_WORKSPACE", [CONTRACTS_DIR])


def eosfactory_data():
    '''Data directory.

    For developer's installation, data is in the root of the installation.
    .: wsl_root.sh
    config: config.ini, config.json, genesis.json, ...
    contracts: eosio_token, hello_world, tic_tac_toe, ...
    templates: contracts, ...
    includes: eoside, ...
    libs: ...
    '''
    tested = []
    is_not_linked = is_site_package()

    if not is_not_linked:
        path = eosf_dir()
        tested.append(path)
        if os.path.exists(os.path.join(path, "config", "config.ini")):
            return path
    elif is_not_linked == 1:
        for path in eosfactory_data_[1]:
            tested.append(path)
            if os.path.exists(os.path.join(path, "config", "config.ini")):
                return path
    elif is_not_linked == 2:
        for path in eosfactory_data_[2]:
            tested.append(path)
            if os.path.exists(os.path.join(path, "config", "config.ini")):
                return path

    msg = "Cannot determine the directory of application data. Tried:"
    for path in tested:
        msg = '''{}
    {}
        '''.format(msg, path)

    raise errors.Error(msg, translate=False)


def is_site_package():
    is_local_or_system = -1
    eosfactory_path = eosfactory.__path__
    for item in eosfactory_path:
        if "site-packages" in item:
            if "local" in item:
                is_local_or_system = 1
            else:
                is_local_or_system = 2

            break
        
        if "eosfactory/eosfactory" in item:
            is_local_or_system = 0

# No EOSFactory:
# import eosfactory
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# ModuleNotFoundError: No module named 'eosfactory'

# developer's installation:
# >>> import eosfactory
# >>> print(eosfactory.__path__)
# ['/mnt/c/Workspaces/EOS/eosfactory/eosfactory']

    if is_local_or_system == -1:
        raise errors.Error('''
Cannot determine the configuration directory. 'eosfactory.__path__' is
    {}
        '''.format(eosfactory_path), translate=False)

    return is_local_or_system


def set_contract_workspace_dir(contract_workspace_dir=None, is_set=False):
    from termcolor import cprint, colored
    import pathlib

    def tilde(tilde_path):
        return tilde_path.replace("~", str(pathlib.Path.home()))

    def set(contract_workspace_dir):
        if contract_workspace_dir:
            path = utils.wslMapWindowsLinux(contract_workspace_dir)
            if os.path.exists(path) and os.path.isdir(path):
                map = config_map()
                map[contract_workspace_dir_[0]] = path
                write_config_map(map)
                return True

        return False

    if set(contract_workspace_dir):
        return

    current_path_color = "green"
    error_path_color = "red"

    while True:
        map = config_map()
        contract_workspace_dir = None

        if contract_workspace_dir_[0] in map:
            contract_workspace_dir = map[contract_workspace_dir_[0]]
        else:
            contract_workspace_dir = os.path.join(TMP, CONTRACTS_DIR)
            
        new_dir = tilde(input(utils.heredoc('''
Where do you prefer to keep your smart-contract projects?
The current location of the is:
    {}
Otherwise, input another existing directory path, or nothing to 
keep the current one:
            '''.format(
                colored(contract_workspace_dir, current_path_color)
                )
            ) + "\n"))

        if not new_dir:
            new_dir = contract_workspace_dir
        
        if set(new_dir):
            print("OK")
            break
        else:        
            print("\n" + utils.heredoc('''
The path you entered:
    {}
doesn't seem to exist!
            ''').format(colored(new_dir, error_path_color)) + "\n")


def config_dir():
    path = os.path.join(eosfactory_data(), CONFIG_DIR)
    if not os.path.exists(path):
        raise errors.Error('''
Cannot find the configuration directory
{}
        '''.format(path), translate=False)
    return path


def template_dir():
    path = os.path.join(eosfactory_data(), TEMPLATE_DIR[1])
    if not os.path.exists(path):
        raise errors.Error('''
Cannot find the template directory
{}
        '''.format(path), translate=False)
    return path


def eoside_includes_dir():
    '''The directory for contract definition includes.

    It may be set with 
    *INCLUDE* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    path = includes_[1]
    if not os.path.isabs(path):
        path = os.path.join(eosfactory_data(), includes_[1])
    if not os.path.exists(path):
        path = None
    return path    


def eoside_libs_dir():
    '''The directory for contract links.

    It may be set with 
    *LIBS* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    path = libs_[1]
    if not os.path.isabs(path):
        path = os.path.join(eosfactory_data(), libs_[1])
    if not os.path.exists(path):
        path = None
    return path    


def contract_workspace_dir(dont_set_workspace=False):
    '''The absolute path to the contract workspace.

    The contract workspace is a directory where automatically created projects
    are placed by default. It is set while EOSFactory is installed. 

    If not set, the projects are stored in the `.config.CONTRACTS_DIR` 
    subdirectory (typically *contracts/*) of the EOSFActory installation, if 
    EOSFactory is installed from its GitHub repository, otherwise, they go to 
    a directory specified as 
    `join(.config.TMP, .config.CONTRACTS_DIR)`. 

    The setting may be changed with 
    *EOSIO_CONTRACT_WORKSPACE* entry in the *config.json* file, 
    see :func:`.current_config`.

    Args:
        dont_set_workspace (bool): If set., do not query for empty workspace 
            directory.
    '''
    if dont_set_workspace:
        return config_map()[contract_workspace_dir_[0]]

    if not contract_workspace_dir_[0] in config_map():
        set_contract_workspace_dir()
    
    workspace_dir = config_value(contract_workspace_dir_)
    path = utils.wslMapWindowsLinux(workspace_dir)

    if os.path.isabs(path):
        if os.path.exists(path):
            return path
        else:
            raise errors.Error('''
The path
'{}',
set as the contract workspace directory, does not exist.
            '''.format(path), translate=False)
    else:
        if not is_site_package():
            path = os.path.join(eosf_dir(), path)
        else:
            path = os.path.join(TMP, path)
            if not os.path.exists(path):
                os.makedirs(path)

        if os.path.exists(path):
            return path
        else:
            raise errors.Error('''
The path
'{}'
resolved as the contract workspace directory directory does not exist.
            '''.format(workspace_dir, translate=False)
            )
    return path


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


def eosf_dir():
    '''The absolute directory of the EOSFactory installation.
    '''
    path = os.path.realpath(os.path.join(
                            os.path.realpath(__file__), FROM_HERE_TO_EOSF_DIR))
    
    if os.path.exists(path):
        return path

    raise errors.Error('''
Cannot determine the root directory of the EOSFactory installation.
The path to the file 'config.py' is
    '{}'.
The expected installation path, which is 
    '{}',
is reported as non-existent.
    '''.format(__file__, path), translate=False)


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
    

def nodeos_config_dir():
    '''Directory containing configuration files such as config.ini.

    It may be changed with 
    *LOCAL_NODE_CONFIG_DIR* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    path = first_valid_path(config_dir_, raise_error=False)
    if path:
        return path

    return config_dir()


def genesis_json():
    '''File to read Genesis State from.

    It may be changed with 
    *EOSIO_GENESIS_JSON* entry in the *config.json* file, 
    see :func:`.current_config`.    
    '''
    path = first_valid_path(genesis_json_, raise_error=False)
    if not path:
        path = os.path.join(config_dir(), "genesis.json")
    if not os.path.exists(path):
        raise errors.Error('''
Cannot find any path for '{}'.
Tried:
{}
        '''.format(genesis_json_[0], genesis_json_[1]), translate=False)

    return path


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
    if not utils.is_windows_ubuntu():
        return ""

    wsl_root_sh = "wsl_root.sh"
    wsl_root_sh = os.path.join(eosfactory_data(), wsl_root_sh)

    if wsl_root_[1][0] is None:
        path = ""
        path, error = utils.spawn(
            [wsl_root_sh, path], raise_exception=False)
        if error:
            while True:
                if not os.path.exists(wsl_root_sh):
                    path = ""
                    logger.ERROR('''
Cannot find the bash command:
'{}'
The intelisense feature of Visual Studio Code will be disabled. 
                    '''.format(wsl_root_sh), translate=False)
                    break                   

                path = input(logger.error('''
Error message is
{}

Cannot find the root of the WSL file system which was tried to be
'{}'
Please, find the path in your computer and enter it. Enter nothing, if you do
not care about having efficient the intelisense of Visual Studio Code.
                '''.format(error, path), translate=False) + "\n<<< ")
                if not path:
                    break

                path, error = utils.spawn(
                    [wsl_root_sh, path], raise_exception=False)
                if not error:
                    break
        
        wsl_root_[1][0] = path.replace("\\", "/")

    return wsl_root_[1][0]


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
    return first_valid_which(node_exe_) 


def cli_exe():
    '''The path to the *cleos* executable.
    
    The setting may be changed with 
    *EOSIO_CLI_EXECUTABLE* entry in the *config.json* file, 
    see :func:`.current_config`.    
    '''
    return first_valid_which(cli_exe_)


def keosd_exe():
    '''The path to the *keosd* executable.
    
    The setting may be changed with 
    *KEOSD_EXECUTABLE* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    return first_valid_which(keosd_exe_)


def eosio_cpp():
    '''The path to the *eosio-cpp* executable.
    
    The setting may be changed with 
    *EOSIO_CPP* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    return first_valid_which(eosio_cpp_)


def eosio_version():
    try:
        version = subprocess.check_output(
            "echo $({} --version)".format(node_exe()), shell=True, 
                    timeout=10).decode("ISO-8859-1").strip().replace("v", "")
        retval = [version]
        if not version.split(".")[:2] == EOSIO_VERSION.split(".")[:2]:
            retval.append(EOSIO_VERSION)
        return retval

    except Exception as e:
        return ["", EOSIO_VERSION]


def eosio_cpp_version():
    try:
        version = subprocess.check_output(
            [eosio_cpp(), "-version"], timeout=5).decode("ISO-8859-1").strip().replace("eosio-cpp version ", "")
        retval = [version]
        if not version.split(".")[:2] == EOSIO_CDT_VERSION.split(".")[:2]:
            retval.append(EOSIO_CDT_VERSION)
        return retval

    except Exception as e:
        return ["", EOSIO_CDT_VERSION]


def eosio_cdt_root():
    '''The path to the *eosio-cpp* installation directory.
    
    The setting may be changed with 
    *EOSIO_CPP* entry in the *config.json* file, 
    see :func:`.current_config`.
    '''
    # find /usr -wholename "*/eosio.cdt/1.6.1"
    config_json = config_map()
    if eosio_cdt_root_[0] in config_json and config_json[eosio_cdt_root_[0]]:
        return config_json[eosio_cdt_root_[0]]

    eosio_cpp_version_ = eosio_cpp_version()
    if not eosio_cpp_version_:
        raise errors.Error(
            '''
            'eosio-cpp' does not response.
            ''')        

    version_pattern = re.compile(VERSION_PATTERN)
    tested = []
    for path in eosio_cdt_root_[1]:
        tested.append(path)
        if version_pattern.match(path):
            path = path.replace(
                re.findall(version_pattern, path)[0], eosio_cpp_version_[0])
            if(os.path.exists(path)):
                return path

    msg = "Cannot determine the installation directory of 'eosio-cdt. Tried:"
    for path in tested:
        msg = '''{}
    {}
        '''.format(msg, path)
    msg = '''{}
Define it in the config file
{} 
    '''.format(msg, config_file())
    raise errors.Error(msg, translate=False) 


def eosio_cpp_includes():
    '''The list of eosio-cpp includes.
    
    The setting may be changed with *EOSIO_CPP* entry in the *config.json* 
    file, see :func:`.current_config`.
    '''
    list = []
    path = eosio_cdt_root()
    for include in eosio_cpp_includes_[1][0]:
        list.append(path + include)
    return list


def keosd_wallet_dir(raise_error=True):
    '''The path to the local wallet directory.

    The path is hard-coded in the *keosd* wallet manager.

    Args:
        raise_error (bool): If set, rise an error if the path is invalid.

    Raises:
        .core.errors.Error: If the directory does not exist.
    '''
    path = first_valid_path(keosd_wallet_dir_, raise_error=False)
    if not path:
        from eosfactory.core.cleos import WalletList
        WalletList()
        path = first_valid_path(keosd_wallet_dir_, raise_error=False)
        if not path:
            if raise_error:
                raise errors.Error('''
Cannot find any path for '{}'.
Tried:
{}
                '''.format(keosd_wallet_dir_[0], keosd_wallet_dir_[1]), 
                                                            translate=False)

    return path


def config_file():
    '''The path to the *config.json* file.
    '''
    file = os.path.join(config_dir(), CONFIG_JSON)

    if not os.path.exists(file):
        try:
            with open(file, "w+") as f:
                f.write("{}")
        except Exception as e:
            raise errors.Error(str(e), translate=False)
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
            raise errors.Error(str(e), translate=False)

    raise errors.Error('''
Cannot find the config file.       
    ''', translate=False)


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
    ''', translate=False)
    

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
Tried:
{}
Define it in the config file
{}       
    '''.format(config_list[0], config_list[1], config_file()), translate=False)


def first_valid_which(config_list, find_file=None, raise_error=True):
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
    if values[0]:
        for path in values:
            if os.path.isabs(path):
                if find_file:
                    if os.path.exists(os.path.join(path, find_file)):
                        return path
            else:
                if utils.which(path):
                    return path

    if raise_error:
        config_values(config_list)
        raise errors.Error('''
Cannot find any path for '{}'.
Tried:
{}
        '''.format(config_list[0], config_list[1]), translate=False)
    else:
        return None


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
    if values[0]:
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

    if raise_error:
        raise errors.Error('''
Cannot find any path for '{}'.
Tried:
{}
        '''.format(config_list[0], config_list[1]), translate=False)
    else:
        return None


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
        return os.path.realpath(contract_dir_hint)

    # ? the relative path to a contract directory, relative to the directory 
    # set with the 'contract_workspace_dir()' function
    contract_dir_ = os.path.join(
        contract_workspace_dir(), contract_dir_hint)
    trace = trace + contract_dir_ + "\n"
    if os.path.isdir(contract_dir_):
        return os.path.realpath(contract_dir_)

    # ? the relative path to a contract directory, relative to 
    # 'eosfactory_data()/contracts'
    contract_dir_ =  os.path.join(
                eosfactory_data(), CONTRACTS_DIR, contract_dir_hint)

    trace = trace + contract_dir_ + "\n"
    if os.path.isdir(contract_dir_):
        return os.path.realpath(contract_dir_)
    
    raise errors.Error('''
Cannot determine the contract directory.
Tried:
{}
    '''.format(trace), translate=False)


def source_files(search_dir):
    '''List files CPP/C and ABI files from the given directory
    '''
    srcs = []
    extensions = [".cpp", ".cxx", ".c", ".abi"]
    files = os.listdir(search_dir)
    for file in files:
        path = os.path.join(search_dir, file)
        if os.path.isfile(path):
            if os.path.splitext(file)[1] in extensions:
                srcs.append(os.path.realpath(path))
        else:
            srcs.extend(source_files(path))
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

    search_dir = contract_dir_
    srcs = source_files(search_dir)
    if srcs:
        return (search_dir, srcs)            

    search_dir = os.path.join(contract_dir_, "src")
    trace = trace + search_dir + "\n"
    srcs = source_files(search_dir)
    if srcs:
        return (search_dir, srcs)            

    raise errors.Error('''
Cannot find any contract source directory.
Tried:
{}
    '''.format(trace), translate=False)


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
Tried:
{}
    '''.format(contract_dir_hint, contract_file_hint, trace), translate=False)  


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


def update_eosio_cpp_includes(c_cpp_properties_path):
    c_cpp_properties_path = utils.wslMapWindowsLinux(c_cpp_properties_path)
    with open(c_cpp_properties_path) as f:
        c_cpp_properties = f.read()
        
    version_pattern = re.compile(VERSION_PATTERN)

    if re.findall(version_pattern, c_cpp_properties):
        new = c_cpp_properties.replace(
                re.findall(version_pattern, c_cpp_properties)[0], eosio_cpp_version()[0])

        if not new == c_cpp_properties:
            with open(c_cpp_properties_path,'w') as f:
                f.write(new)


def not_defined(config_map):
    retval = {}
    for key, value in config_map.items():
        if value == None or value is None:
            retval[key] = value
    return retval


def installation_dependencies(config_map):
    '''Verify whether 'eosio' and 'eosio.cpp' packages are properly installed.
    '''
    eosio_version_ = config_map["EOSIO_VERSION"]
    if eosio_version_ and eosio_version_[0]:
        if len(eosio_version_) > 1:
            print('''NOTE!
The version of the installed 'eosio' package is {} while EOSFactory was tested
with version {}
            '''.format(
                eosio_version_[0], eosio_version_[1]))
    else:
        print('''Cannot determine the version of the installed 'eosio' package as 'nodeos' does not response.
        ''')

    eosio_cpp_version_ = config_map["EOSIO_CDT_VERSION"]
    if eosio_cpp_version_:
        if len(eosio_cpp_version_) > 1:
            print('''NOTE!
The version of the installed 'eosio.cdt' package is {} while EOSFactory was tested with version {}
            '''.format(eosio_cpp_version_[0], eosio_cpp_version_[1]))
    else:
        print('''Cannot determine the version of the installed 'eosio.cdt' package as 'eosio-cpp' does not response.
        ''')        


def current_config(contract_dir=None, dont_set_workspace=False):
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
    if not is_site_package():
        try:
            map["EOSFACTORY_DIR"] = eosf_dir()
        except:
            map["EOSFACTORY_DIR"] = None
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
        map[contract_workspace_dir_[0]] = contract_workspace_dir(
                                                            dont_set_workspace)
    except:
         map[contract_workspace_dir_[0]] = None
    try:
        map[keosd_wallet_dir_[0]] = keosd_wallet_dir()   
    except:
        map[keosd_wallet_dir_[0]] = None
    try: 
        map[data_dir_[0]] = data_dir()
    except:
        map[data_dir_[0]] = None 
    try:    
        map[config_dir_[0]] = nodeos_config_dir()
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
        map[eosio_cdt_root_[0]] = eosio_cdt_root()
    except:
        map[eosio_cdt_root_[0]] = None
    try: 
        map[eosio_cpp_includes_[0]] = eosio_cpp_includes()
    except:
        map[eosio_cpp_includes_[0]] = None        
    try:   
        map[genesis_json_[0]] = genesis_json()
    except:
        map[genesis_json_[0]] = None
    try:   
        map[includes_[0]] = eoside_includes_dir()
    except:
        map[libs_[0]] = None
    try:   
        map[libs_[0]] = eoside_libs_dir()
    except:
        map[libs_[0]] = None
    try:   
        map[eosfactory_data_[0]] = eosfactory_data()
    except:
        map[eosfactory_data_[0]] = None
    try:   
        map[TEMPLATE_DIR[0]] = template_dir()
    except:
        map[TEMPLATE_DIR[0]] = None
        

    map["EOSIO_VERSION"] = eosio_version()
    map["EOSIO_CDT_VERSION"] = eosio_cpp_version()

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
    is_not_linked = is_site_package()
    if not is_not_linked:
        print(
    '''EOSFactory package is installed as a link to the directory:
    '{}'
    '''.format(os.path.join(eosf_dir(), EOSFACTORY_DIR))
        )
    elif is_not_linked == 1:
        print(
    '''EOSFactory is installed as a site package locally.
    '''            
        )
    elif is_not_linked == 2:
        print(
    '''EOSFactory is installed as a site package globally.
    '''            
        )

    config_map = current_config()
    installation_dependencies(config_map)

    print('''
The current configuration of EOSFactory:
{}

You can overwrite the above settings with entries in the configuration 
file located here:
{}
'''.format(
        json.dumps(
            config_map, sort_keys=True, indent=4), config_file())
    )

    not_defined_ = not_defined(config_map)
    if not_defined_:
        print('''
There are undefined setting:
{}
    '''.format(json.dumps(not_defined_, sort_keys=True, indent=4)))

def main():
    '''
    usage: config.py [-h] [--wsl_root] [--dependencies] [--json]
                    [--workspace WORKSPACE]

    Show the configuration of EOSFactory or set contract workspace.

    Args:
        -h, --help              Show this help message and exit
        --wsl_root              Show set the root of the WSL and exit.
        --dependencies          List dependencies of EOSFactory and exit.
        --dont_set_workspace    Ignore empty workspace directory.
        --json                  Bare config JSON and exit.
        --workspace WORKSPACE   Set contract workspace and exit.
    '''

    parser = argparse.ArgumentParser(description='''
    Show the configuration of EOSFactory or set contract workspace.
    ''')
    parser.add_argument(
        "--wsl_root",  help="Show set the root of the WSL and exit.", 
        action="store_true")
    parser.add_argument(
        "--dependencies", help="List dependencies of EOSFactory and exit.",
        action="store_true")
    parser.add_argument(
        "--dont_set_workspace", help="Ignore empty workspace directory.", 
        action="store_true")    
    parser.add_argument(
        "--json", help="Bare config JSON and exit.", 
        action="store_true")
    parser.add_argument(
        "--workspace", help="Set contract workspace and exit.",
        action="store_true")

    args = parser.parse_args()
    if args.dependencies:
        installation_dependencies(current_config())
    elif args.json:
        print(json.dumps(
            current_config(dont_set_workspace=args.dont_set_workspace), 
            sort_keys=True, indent=4))
    elif args.wsl_root:
        wsl_root()
    elif args.workspace:
        set_contract_workspace_dir()
    else:
        config()

if __name__ == '__main__':
    main()
