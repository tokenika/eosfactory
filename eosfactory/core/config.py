import os
import argparse

import json

import eosfactory.core.errors as errors
import eosfactory.core.logger as logger
import eosfactory.core.utils as utils

LOCALHOST_HTTP_ADDRESS = "127.0.0.1:8888"
contractsDir = "contracts"
DEFAULT_TEMPLATE = "01_hello_world"
FROM_HERE_TO_EOSF_DIR = "../../../"
CONFIG_JSON = "config.json"
EOSIO_CONTRACT_DIR = "build/contracts/"
CONTRACTS_DIR = "contracts/"

eosio_repository_dir_ = ("EOSIO_SOURCE_DIR", [None])
node_address_ = ("LOCAL_NODE_ADDRESS", [LOCALHOST_HTTP_ADDRESS])
wallet_address_ = ("WALLET_MANAGER_ADDRESS", [None])
genesis_json_ = ("EOSIO_GENESIS_JSON", ["localnode/genesis.json"])
data_dir_ = ("LOCAL_NODE_DATA_DIR", ["localnode"])
config_dir_ = ("LOCAL_NODE_CONFIG_DIR", ["localnode"])
workspaceEosio_ = ("EOSIO_WORKSPACE", [EOSIO_CONTRACT_DIR])
keosd_wallet_dir_ = ("KEOSD_WALLET_DIR", ["${HOME}/eosio-wallet/"])
chain_state_db_size_mb_ = ("EOSIO_SHARED_MEMORY_SIZE_MB", ["200"])
node_api_ = ("NODE_API", ["cleos"])
wsl_root_ = ("WSL_ROOT", [None])

cli_exe_ = (
    "EOSIO_CLI_EXECUTABLE", 
    ["build/programs/cleos/cleos", "/usr/local/eosio/bin/cleos"])
node_exe_ = (
    "LOCAL_NODE_EXECUTABLE", 
    ["build/programs/nodeos/nodeos", "/usr/local/eosio/bin/nodeos"])

# eosio_cpp_ = ("EOSIO_CPP", ["/usr/local/eosio.cdt/bin/eosio-cpp"])
# eosio_abigen_ = ("EOSIO_ABIGEN", ["/usr/local/eosio.cdt/bin/eosio-abigen"])

eosio_cpp_ = ("EOSIO_CPP", [None])
eosio_abigen_ = ("EOSIO_ABIGEN", [None])

key_private_ = (
    "EOSIO_KEY_PRIVATE", 
    ["5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"])
key_public_ = (
    "EOSIO_KEY_PUBLIC",
    ["EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"])
contract_workspace_ = (
    "EOSIO_CONTRACT_WORKSPACE", [CONTRACTS_DIR])
boost_include_dir_ = (
    "BOOST_INCLUDE_DIR", 
    ["${HOME}/opt/boost/include", "/usr/local/include/"])
wasm_clang_exe_ = (
    "WASM_CLANG_EXECUTABLE", 
    ["${HOME}/opt/wasm/bin/clang", "/usr/local/wasm/bin/clang"])
wasm_llvm_link_exe_ = (
    "WASM_LLVM_LINK_EXECUTABLE",
    ["${HOME}/opt/wasm/bin/llvm-link", "/usr/local/wasm/bin/llvm-link"])
wasm_llc_exe_ = (
    "WASM_LLC_EXECUTABLE",
    ["${HOME}/opt/wasm/bin/llc", "/usr/local/wasm/bin/llc"])
s2wasm_exe_ = ( ##/mnt/c/Workspaces/EOS/eos/
    "S2WASM_EXECUTABLE",
    ["build/externals/binaryen/bin/eosio-s2wasm",
        "/usr/local/bin/eosio-s2wasm", "/usr/local/eosio/bin/eosio-s2wasm"])
wast2wasm_exe_ = (
    "WAST2WASM_EXECUTABLE",
    ["build/libraries/wasm-jit/Source/Programs/eosio-wast2wasm",
        "/usr/local/bin/eosio-wast2wasm", 
        "/usr/local/eosio/bin/eosio-wast2wasm"])
abigen_exe_ = ( # used without eosio.cdt
    "ABIGEN_EXECUTABLE",
    ["build/programs/eosio-abigen/eosio-abigen",
        "/usr/local/bin/eosio-abigen","/usr/local/eosio/bin/eosio-abigen"])
is_nodeos_in_window_ = ("NODE_IN_WINDOW", [0])


def eosio_repository_dir():
    return config_value(eosio_repository_dir_)


def eosf_dir():
    path = os.path.realpath(os.path.join(__file__, FROM_HERE_TO_EOSF_DIR))
    if os.path.exists(path):
        return path

    raise errors.Error('''
        Cannot determine the root directory of the EOSFactory.
        It is attempted to be derived from the path of the configuration file
            '{}'.
        Therefore, this file has to remain in the original position.
        Currently, the result of the assertion is '{}'.
    '''.format(__file__, path))


def eosio_key_private():
    return config_value(key_private_)

def eosio_key_public():
    return config_value(key_public_)

def chain_state_db_size_mb():
    return config_value(chain_state_db_size_mb_)

def node_api():
    return config_value(node_api_)


def wsl_root():
    path = config_value(wsl_root_)
    return path.replace("\\", "/")


def is_nodeos_in_window():
    return config_value(is_nodeos_in_window_)


def http_server_address():
    return config_value(node_address_)


def http_wallet_address():
    return config_value(wallet_address_)


def boost_include_dir():
    return first_valid_path(boost_include_dir_, "boost/version.hpp")


def wasm_clang_exe():
    return first_valid_path(wasm_clang_exe_)


def wasm_llvm_link_exe():
    return first_valid_path(wasm_llvm_link_exe_)      


def s2wasm_exe():
    return first_valid_path(s2wasm_exe_)


def wast2wasm_exe():
    return first_valid_path(wast2wasm_exe_)

def wasm_llc_exe():
    return first_valid_path(wasm_llc_exe_) 


def node_exe():
    return first_valid_path(node_exe_) 


def cli_exe():
    return first_valid_path(cli_exe_)


def eosio_cpp():
    return first_valid_path(eosio_cpp_)


def eosio_abigen():
    return first_valid_path(eosio_abigen_)


def abigen_exe():
    return first_valid_path(abigen_exe_)


def keosd_wallet_dir():
    return first_valid_path(keosd_wallet_dir_)


def node_exe_name():
    '''Name of the local node executable, used for killing the process.
    '''
    path = node_exe()
    return os.path.splitext(os.path.basename(path))[0]


def data_dir():
    return first_valid_path(data_dir_)
    

def config_dir():
    return first_valid_path(config_dir_)


def genesis_json():
    return first_valid_path(genesis_json_)

def workspaceEosio():
    return first_valid_path(workspaceEosio_)


def config_file():
    file = os.path.join(eosf_dir(), CONFIG_JSON)
        
    if not os.path.exists(file):
        with open(file, "w") as output:
            output.write("{}")

            logger.INFO('''
        Cannot find the config json file. It is expected to be 
            '{}'.
        Creating an empty config file there.
            '''.format(file))

    return file


def config_map():
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
Cannot find the config json file.       
    ''')


def write_config_map(map):
    path = config_file()
    if os.path.exists(path):
        with open(path, "w+") as output:
            output.write(json.dumps(map, indent=4))
        return

    raise errors.Error('''
Cannot find the config json file.       
    ''')
    

def config_values(config_list):
    config_key = config_list[0]

    retval = []
    # First, configure file ...
    config_json = config_map()
    if config_key in config_json:
        retval.append(config_json[config_key])
        return retval        
      
    # ... next, environmental variable.
    if config_key in os.environ:
        value = os.environ[config_key]
        retval.append(value)
        return retval        

    # Finally, hard-codded values, if any.
    values = config_list[1]
    if values:
        return values          

    return retval


def config_value(config_list):
    retval = config_values(config_list) 
    return retval[0] if retval else None


def first_valid_path(config_list, findFile=None):
    '''Given a key to the config list, get a valid file system path.

    The key may map to a path either absolute, or relative either to the EOSIO 
    or EOSF repositories.
    
    Also, the path can be relative to the ``HOME`` environment variable.
    '''
    values = config_values(config_list)
    for path in values:

        if "${HOME}" in path: 
            home = None
            if "HOME" in os.environ:
                home = os.environ["HOME"]
                
            if home:
                path = path.replace("${HOME}", home)
                if findFile: 
                    if os.path.exists(os.path.join(path, findFile)):
                        return path
                else:
                    if os.path.exists(path):
                        return path

        if os.path.isabs(path):
            if findFile:
                if os.path.exists(os.path.join(path, findFile)):
                    return path
            else:
                if os.path.exists(path):
                    return path

        try: # We can do without any eosio repository.
            full_path = os.path.join(eosio_repository_dir(), path)
            if findFile:
                if os.path.exists(os.path.join(full_path, findFile)):
                    return full_path
            else:
                if os.path.exists(full_path):
                    return full_path
        except:
            pass

        full_path = os.path.join(eosf_dir(), path)
        if findFile:
            if os.path.exists(os.path.join(full_path, findFile)):
                return full_path
        else:
            if os.path.exists(full_path):
                return full_path        

    raise errors.Error('''
    Cannot find any path for '{}'.
    '''.format(config_list[0]))


def contract_dir(contract_dir_hint):
    '''Given a hint, determine the contract directory.
    The contract directory is the container for the project of a contract.
    The hint is probed to be one of the following pieces of information:
    the absolute path to a contract directory;
    the relative path to a contract directory, relative to the directory set with the ``contract_workspace_`` variable;
    the relative path to a contract directory, relative to the ``contracts`` directory in the repository of EOSFactory;
    the relative path to a contract directory, relative to the ``contracts`` directory in the repository of EOSIO.
    '''
    contract_dir_hint = utils.wslMapWindowsLinux(contract_dir_hint)

    # ? the absolute path to a contract directory
    trace = contract_dir_hint + "\n"
    if os.path.isfile(contract_dir_hint):
        contract_dir_hint = os.path.dirname(contract_dir_hint)
    if os.path.isabs(contract_dir_hint):
        return contract_dir_hint

    # ? the relative path to a contract directory, relative to the directory 
    # set with the 'contract_workspace_' variable
    contract_dir_ = os.path.join(
        config_value(contract_workspace_), contract_dir_hint)
    trace = trace + contract_dir_ + "\n"
    if os.path.isdir(contract_dir_):
        return contract_dir_

    # ? the relative path to a contract directory, relative to the 
    # ``contracts`` directory in the repository of EOSFactory
    contract_dir_ = os.path.join(
            eosf_dir(), 
            CONTRACTS_DIR, contract_dir_hint)
    trace = trace + contract_dir_ + "\n"
    if os.path.isdir(contract_dir_):
        return contract_dir_ 

    # ? the relative path to a contract directory, relative to the 
    # ``contracts`` directory in the repository of EOSIO
    contract_dir_ = os.path.join(
            config_value(eosio_repository_dir_),
            EOSIO_CONTRACT_DIR, contract_dir_hint)
    trace = trace + contract_dir_ + "\n"
    if os.path.isdir(contract_dir_):
        return contract_dir_ 
    
    raise errors.Error('''
        Cannot determine the contract directory.
        Tried path list:
        {}
    '''.format(trace))


def source_files(source_path):
    srcs = []
    extensions = [".cpp", ".cxx", ".c", ".abi"]
    files = os.listdir(source_path)
    for file in files:
        path = os.path.join(source_path, file)
        if os.path.splitext(file)[1] in extensions:
            if os.path.isfile(path):
                srcs.append(path)
    return srcs
    

def contract_source_files(contract_dir_hint):
    contract_dir_ = contract_dir(utils.wslMapWindowsLinux(contract_dir_hint))
    trace = contract_dir_ + "\n"

    source_path = contract_dir_
    srcs = source_files(source_path)
    if srcs:
        return (source_path, srcs)            

    source_path = os.path.join(contract_dir_, "src")
    trace = trace + source_path + "\n"
    srcs = source_files(source_path)
    if srcs:
        return (source_path, srcs)            

    raise errors.Error('''
        Cannot find any contract source directory.
        Tried path list:
        {}
    '''.format(trace))


def contract_file(contract_dir_hint, contract_file_hint):
    ''' Given contract dir and contract file hints, determine the file.

    Contract files are those extended with ``wast``, ``wasm`` and ``abi``.

    First, the ``contract_file_hint`` may be an absolute path.
    Next, it may be relative to the contract directory.

    The contract directory is the container for the project of a contract. This 
    directory is determined with the ``contract_dir`` function, basing on the 
    ``contract_dir_hint``.

    Any contract directory contains directories and files structured according 
    to few schemes:
    flat structure with all the files in this directory as in the ``eos/contracts/*`` contract directories in the EOS repository;
    structure with a directory named ``build`` as resulting from the EOSFactory templates;
    '''
    contract_dir_hint = utils.wslMapWindowsLinux(contract_dir_hint)
    contract_file_hint = utils.wslMapWindowsLinux(contract_file_hint)

    # ? ``contract_file_hint`` may be an absolute path to a file
    trace = contract_file_hint + "\n" 
    if os.path.isabs(contract_file_hint) \
                                    and os.path.isfile(contract_file_hint):
        return contract_file_hint

    # ? it may be relative to the contract directory.
    contract_dir_ = contract_dir(contract_dir_hint)

    # ? flat structure with all the files in this directory
    contract_file = os.path.join(contract_dir_, contract_file_hint)
    trace = trace + contract_file + "\n"
    if os.path.isfile(contract_file):
        return contract_file

    # ? structure with a directory named ``build``
    # and ``contract_file_hint`` is relative file
    contract_file = os.path.join(contract_dir_, "build", contract_file_hint)
    trace = trace + contract_file + "\n"
    if os.path.isfile(contract_file):
        return contract_file

    # ? structure with a directory named ``build``
    # and ``contract_file_hint`` is a file extension merely
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
    '''Return the absolute path to the contract workspace of the user.
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


def abi_file(contract_dir):
    '''Given the contract directory, return the ABI file path relative.
    '''
    return os.path.relpath(
        contract_file(contract_dir, ".abi"), contract_dir)


def wast_file(contract_dir):
    '''Given the contract directory, return the WAST file path relative.
    '''
    return os.path.relpath(
        contract_file(contract_dir, ".wast"), contract_dir)


def wasm_file(contract_dir):
    '''Given the contract directory, return the WASM file path relative.
    '''
    return os.path.relpath(
        contract_file(contract_dir, ".wasm"), contract_dir)


def not_defined():
    map = current_config()
    retval = {}
    for key, value in map.items():
        if value == None or value is None:
            retval[key] = value
    return retval


def current_config(contract_dir=None):
    map = {}
   
    map[node_address_[0]] = http_server_address()     
    map[key_private_[0]] = eosio_key_private()  
    map[key_public_[0]] = eosio_key_public()
    map[wsl_root_[0]] = wsl_root()
    map[wallet_address_[0]] = http_wallet_address() \
            if http_wallet_address() else http_server_address()
    map[chain_state_db_size_mb_[0]] = chain_state_db_size_mb()
    map[node_api_[0]] = node_api()
    map[is_nodeos_in_window_[0]] = is_nodeos_in_window()
    map[contract_workspace_[0]] = config_value(contract_workspace_)

    try:
        map[keosd_wallet_dir_[0]] = keosd_wallet_dir()   
    except:
        map[keosd_wallet_dir_[0]] = None
    try: 
        map[eosio_repository_dir_[0]] = eosio_repository_dir()
    except:
        map[eosio_repository_dir_[0]] = None 
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
        map[node_exe_[0]] = node_exe()
    except:
        map[node_exe_[0]] = None
    try: 
        map[eosio_cpp_[0]] = eosio_cpp()
    except:
        map[eosio_cpp_[0]] = None             
    try: 
        map[eosio_abigen_[0]] = eosio_abigen()
    except:
        map[eosio_abigen_[0]] = None             
    try:   
        map[genesis_json_[0]] = genesis_json()
    except:
        map[genesis_json_[0]] = None      
    try:
        map[wasm_clang_exe_[0]] = wasm_clang_exe()
    except:
        map[wasm_clang_exe_[0]] = None
    try:
        map[boost_include_dir_[0]] =  boost_include_dir()
    except:
        map[boost_include_dir_[0]] = None
    try:
        map[wasm_llvm_link_exe_[0]] = wasm_llvm_link_exe()
    except:
        map[wasm_llvm_link_exe_[0]] = None
    try:
        map[wasm_llc_exe_[0]] = wasm_llc_exe()
    except:
        map[wasm_llc_exe_[0]] = None
    try:
        map[s2wasm_exe_[0]] = s2wasm_exe()
    except:
        map[s2wasm_exe_[0]] = None
    try:
        map[wast2wasm_exe_[0]] = wast2wasm_exe()
    except:
        map[wast2wasm_exe_[0]] = None
    try:
        map[workspaceEosio_[0]] = workspaceEosio()
    except:
        map[workspaceEosio_[0]] = None
    try:
        map[abigen_exe_[0]] = abigen_exe()
    except:
        map[abigen_exe_[0]] = None
    
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

