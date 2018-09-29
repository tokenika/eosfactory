import os
import json
import core.errors as errors
import shell.setup as setup
import core.logger as logger
import core.utils as utils

templContractsDir = "templates/contracts"
contractsDir = "contracts"
TEMPLATE_TOKEN = "CONTRACT_NAME"
DEFAULT_TEMPLATE = "01_hello_world"

map = {
    "EOSIO_SOURCE_DIR": [None],
    "EOSIO_DAEMON_ADDRESS": [setup.LOCALHOST_HTTP_ADDRESS],
    "EOSIO_WALLET_ADDRESS": [None],
        # genesis-json: relative to EOSIO_SOURCE_DIR:
    "EOSIO_GENESIS_JSON": ["genesis.json"],
    "EOSIO_DATA_DIR": ["build/daemon/data-dir/"],
    "EOSIO_CONFIG_DIR": ["build/daemon/data-dir/"],
    "EOSIO_DAEMON_NAME": ["nodeos"],
    "EOSIO_EOSFACTORY_DIR": [None],
    "EOSIO_CLI_NAME": ["cleos"],
    "EOSIO_KEY_PRIVATE": [
        "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"],
    "EOSIO_KEY_PUBLIC": [
        "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"],
        # relative to EOSIO_EOSFACTORY_DIR:
    "EOSIO_CONTRACT_WORKSPACE": [setup.CONTRACTS_DIR],
    "EOSIO_BOOST_INCLUDE_DIR": [
        "${U_HOME}/opt/boost/include", "/usr/local/include/"],
    "EOSIO_SHARED_MEMORY_SIZE_MB": ["200"],
        # EOSIO_WASM_CLANG: relative to U_HOME dir
    "EOSIO_WASM_CLANG": [
        "${U_HOME}/opt/wasm/bin/clang", "/usr/local/wasm/bin/clang"],
    "EOSIO_WASM_LLVM_LINK": [
        "${U_HOME}/opt/wasm/bin/llvm-link", 
        "/usr/local/wasm/bin/llvm-link"],
    "EOSIO_WASM_LLC": [
        "${U_HOME}/opt/wasm/bin/llc", "/usr/local/wasm/bin/llc"],
        "EOSIO_S2WASM": [
            "/usr/local/bin/eosio-s2wasm", 
            "/usr/local/eosio/bin/eosio-s2wasm"],
    "EOSIO_WAST2WASM": [
        "/usr/local/bin/eosio-wast2wasm", 
        "/usr/local/eosio/bin/eosio-wast2wasm"],
    "EOSIO_ABIGEN":[
        "build/programs/eosio-abigen/eosio-abigen",
        "/usr/local/bin/eosio-abigen",
        "/usr/local/eosio/bin/eosio-abigen"
    ],
    "NODEOS_IN_WINDOW": [0]
}


def config_file():
    trace = "Environment variable EOSIO_EOSFACTORY_DIR + setup.CONFIG_DIR:\n"
    trace = "os.environ"
    if "EOSIO_EOSFACTORY_DIR" in os.environ:
        env = os.environ["EOSIO_EOSFACTORY_DIR"]
        trace = trace + env if env else "EOSIO_EOSFACTORY_DIR not defined"
        file = os.path.join(env, setup.CONFIG_DIR, setup.CONFIG_JSON)
        trace = trace + file + "\n\n"

    if os.path.exists(file):
        return file

    setup_dir = os.path.dirname(setup.__file__)
    file = os.path.join(setup_dir, setup.CONFIG_JSON)
    trace = trace + file + "\n"

    if os.path.exists(file):
        return file

    setup_dir = os.path.dirname(setup_dir)
    file = os.path.join(setup_dir, setup.CONFIG_JSON)
    trace = trace + file + "\n"

    if os.path.exists(file):
        return file                

    setup_dir = os.path.dirname(setup_dir)
    file = os.path.join(setup_dir, setup.CONFIG_JSON)
    trace = trace + file + "\n"

    if os.path.exists(file):
        return file
    else:
        with open(file, "w") as output:
            output.write("{}")

        logger.INFO('''
Cannot find the config json file. It is expected in any of the following 
locations:
{}
-- searched in the same order.

Creating an empty config file:
{}
        '''.format(file, trace))

    return file


def config_map():
    path = config_file()
    if os.path.exists(path):
        with open(path, "r") as input:
            return json.load(input)

    raise errors.Error('''
Cannot find the config json file.       
    ''')


def config_values(config_key):
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

    # Finally, hard-codded value, if any.
    value = map[config_key]
    if value:
        return value          

    return retval


def config_value(config_key):
    retval = config_values(config_key) 
    return retval[0] if retval else None


def valid_path(config_key, findFile=None):
    '''Given a key to the config map, get a valid file system path.

    The key may map to a path either absolute or relative to the EOS 
    repository. Also, the path can be relative to the ``HOME`` environment
    variable.
    '''
    values = config_values(config_key)
    for path in values:

        if "${U_HOME}" in path: 
            home = None
            if "U_HOME" in os.environ:
                home = os.environ["U_HOME"]
            elif "HOME" in os.environ:
                home = os.environ["HOME"]
                
            if home:
                path = path.replace("${U_HOME}", home)
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
        else:
            path = os.path.join(eosio_repository_dir(), path)
            if findFile:
                if os.path.exists(os.path.join(path, findFile)):
                    return path
            else:
                if os.path.exists(path):
                    return path

    return None


def eosf_dir():
    path = config_value("EOSIO_EOSFACTORY_DIR")
    if path:
        return path

    raise errors.Error('''
        Cannot determine the context directory.
    ''')


def eosio_repository_dir():
    path = config_value("EOSIO_SOURCE_DIR")
    if path:
        return path

    raise errors.Error('''
        Cannot determine the EOSIO source directory.
    ''')


def genesis_json():
    path = config_value("EOSIO_GENESIS_JSON")
    if not os.path.isabs(path):
        path = os.path.join(config_dir(), path)
    if os.path.isfile(path):
        return path

    raise errors.Error('''
        Cannot determine the genesis file. 
        Tried path is
        {}
    '''.format(path))


def contract_dir(contract_dir_hint):
    ''' Given a hint, determine the contract directory.
    The contract directory is the container for the project of a contract. The 
    hint is probed to be one of the following pieces of information:
    the absolute path to a contract directory;
    the relative path to a contract directory, relative to the directory 
        set with the EOSIO_CONTRACT_WORKSPACE variable;
    the relative path to a contract directory, relative to the ``contracts`` 
        directory in the repository of EOSFactory;
    the relative path to a contract directory, relative to the ``contracts`` 
        directory in the repository of EOSIO.
    ''' 
    contract_dir_hint = utils.wslMapWindowsLinux(contract_dir_hint)

    # ? the absolute path to a contract directory
    trace = contract_dir_hint + "\n"
    if os.path.isfile(contract_dir_hint):
        contract_dir_hint = os.path.dirname(contract_dir_hint)
    if os.path.isabs(contract_dir_hint):
        return contract_dir_hint

    # ? the relative path to a contract directory, relative to the directory 
    # set with the EOSIO_CONTRACT_WORKSPACE variable
    contract_dir_ = os.path.join(
        config_value("EOSIO_CONTRACT_WORKSPACE"), contract_dir_hint)
    trace = trace + contract_dir_ + "\n"
    if os.path.isdir(contract_dir_):
        return contract_dir_

    # ? the relative path to a contract directory, relative to the 
    # ``contracts`` directory in the repository of EOSFactory
    contract_dir_ = os.path.join(
            config_value("EOSIO_EOSFACTORY_DIR"), 
            setup.CONTRACTS_DIR, contract_dir_hint)
    trace = trace + contract_dir_ + "\n"
    if os.path.isdir(contract_dir_):
        return contract_dir_ 

    # ? the relative path to a contract directory, relative to the 
    # ``contracts`` directory in the repository of EOSIO
    contract_dir_ = os.path.join(
            config_value("EOSIO_SOURCE_DIR"),
            setup.EOSIO_CONTRACT_DIR, contract_dir_hint)
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

    srcs = source_files(contract_dir_)
    if srcs:
        return srcs            

    source_path = os.path.join(contract_dir_, "src")
    trace = trace + source_path + "\n"
    srcs = source_files(source_path)
    if srcs:
        return srcs            

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
    workspacePath = config_value("EOSIO_CONTRACT_WORKSPACE")
    trace = workspacePath + "\n"

    if not os.path.isabs(workspacePath):
        workspacePath = os.path.join(
            configValue("EOSIO_EOSFACTORY_DIR"), workspacePath)
        trace = trace + workspacePath + "\n"
    if os.path.exists(workspacePath):
        return workspacePath

    raise errors.Error('''
        Cannot determine the contract workspace.
        Tried path list:
        {}
    '''.format(trace))    


def getEosioKeyPrivate():
    return configValue("EOSIO_KEY_PRIVATE")
def eosio_key_private():
    return config_value("EOSIO_KEY_PRIVATE")


def eosio_key_public():
    return config_value("EOSIO_KEY_PUBLIC")


def chain_state_db_size_mb():
    return config_value("EOSIO_SHARED_MEMORY_SIZE_MB")


def is_nodeos_in_window():
    return config_value("NODEOS_IN_WINDOW")


def http_server_address():
    return config_value("EOSIO_DAEMON_ADDRESS")


def http_wallet_address():
    return config_value("EOSIO_WALLET_ADDRESS")


def cleos_exe():
    path = os.path.join(
        eosio_repository_dir(), "build/programs/", config_value("EOSIO_CLI_NAME"), 
        config_value("EOSIO_CLI_NAME"))

    trace = path + "\n"
    if os.path.exists(path):
        return path       

    path = os.path.join("/usr/local/bin", config_value("EOSIO_CLI_NAME"))
    trace = trace + path + "\n"
    if os.path.exists(path):
        return path.string() 

    raise errors.Error('''
        Cannot determine the EOS cli executable file. 
        Tried path list:
        {}
    '''.format(trace))


def data_dir():
    path = config_value("EOSIO_DATA_DIR")

    if not os.path.isabs(path):
        contextDir = config_value("EOSIO_EOSFACTORY_DIR")
        if contextDir:
            path = os.path.join(contextDir, path)

    if os.path.isdir(path):
        return path

    raise errors.Error('''
        Cannot determine the 'data-dir' directory. 
        Tried path is
        {}
    '''.format(path))      


def config_dir():
    path = config_value("EOSIO_CONFIG_DIR")
    if not os.path.isabs(path):
        contextDir = config_value("EOSIO_EOSFACTORY_DIR")
        if contextDir:
            path = os.path.join(contextDir, path)

    if os.path.isdir(path):
        return path

    raise errors.Error('''
        Cannot find the 'config-dir' directory. 
        Tried path is
        {}
    '''.format(path))         


def keosd_wallet_dir():
    if "U_HOME" in os.environ:
        home = os.environ["U_HOME"]
        return home + "/eosio-wallet/"
    return None


def nodeos_exe():
    path = os.path.join(
            eosio_repository_dir(), "build/programs/", 
            config_value("EOSIO_DAEMON_NAME"), 
            config_value("EOSIO_DAEMON_NAME"))
    trace = path + "\n"
    if os.path.exists(path):
        return path


def nodeos_name():
    return config_value("EOSIO_DAEMON_NAME")


def boost_include_dir():
    return valid_path("EOSIO_BOOST_INCLUDE_DIR", "boost/version.hpp")


def wasm_clang_exe():
    return valid_path("EOSIO_WASM_CLANG")


def wasm_llvm_link_exe():
    return valid_path("EOSIO_WASM_LLVM_LINK")      


def s2wasm_exe():
    return valid_path("EOSIO_S2WASM")


def wast2wasm_exe():
    return valid_path("EOSIO_WAST2WASM")

def abigen_exe():
    return valid_path("EOSIO_ABIGEN")


def wasm_llc_exe():
    return valid_path("EOSIO_WASM_LLC")       


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


def current_config(contract_dir=None):
    map = {}
    try: 
        map["EOSIO_SOURCE_DIR"] = eosio_repository_dir()
    except:
        map["EOSIO_SOURCE_DIR"] = "NOT DEFINED"

    try:
        map["EOSIO_EOSFACTORY_DIR"] = eosf_dir()
    except:
        map["EOSIO_EOSFACTORY_DIR"] = "NOT DEFINED"   

    try: 
        map["EOSIO_DATA_DIR"] = data_dir()
    except:
        map["EOSIO_DATA_DIR"] = "NOT DEFINED" 

    try:    
        map["EOSIO_CONFIG_DIR"] = config_dir()
    except:
        map["EOSIO_CONFIG_DIR"] = "NOT DEFINED"   
    
    map["KEOSD_WALLET_DIR"] = keosd_wallet_dir()   

    try: 
        map["cleosExe"] = cleos_exe()
    except:
        map["cleosExe"] = "NOT DEFINED" 

    try:   
        map["genesisJson"] = genesis_json()
    except:
        map["genesisJson"] = "NOT DEFINED"   
   
    map["EOSIO_DAEMON_ADDRESS"] = http_server_address()     

    map["EOSIO_KEY_PRIVATE"] = eosio_key_private()  

    map["EOSIO_KEY_PUBLIC"] = eosio_key_public()

    map["EOSIO_WALLET_ADDRESS"] = http_wallet_address() \
            if http_wallet_address() else http_server_address()

    map["EOSIO_DAEMON_NAME"] = nodeos_name()

    try:
        map["EOSIO_WASM_CLANG"] = wasm_clang_exe()
    except:
        map["EOSIO_WASM_CLANG"] = "NOT DEFINED"

    try:
        map["EOSIO_BOOST_INCLUDE_DIR"] =  boost_include_dir()
    except:
        map["EOSIO_BOOST_INCLUDE_DIR"] = "NOT DEFINED"

    try:
        map["EOSIO_WASM_LLVM_LINK"] = wasm_llvm_link_exe()
    except:
        map["EOSIO_WASM_LLVM_LINK"] = "NOT DEFINED"

    try:
        map["EOSIO_WASM_LLC"] = wasm_llc_exe()
    except:
        map["EOSIO_WASM_LLC"] = "NOT DEFINED"

    try:
        map["EOSIO_S2WASM"] = s2wasm_exe()
    except:
        map["EOSIO_S2WASM"] = "NOT DEFINED"

    try:
        map["EOSIO_WAST2WASM"] = wast2wasm_exe()
    except:
        map["EOSIO_WAST2WASM"] = "NOT DEFINED"

    map["sharedMemory"] = chain_state_db_size_mb()
    map["NODEOS_IN_WINDOW"] = is_nodeos_in_window()

    map["contractWorkspace"] = config_value("EOSIO_CONTRACT_WORKSPACE")
    
    try:
        map["workspaceEosio"] = os.path.join(
                                    eosio_repository_dir(), setup.EOSIO_CONTRACT_DIR)
    except:
        map["workspaceEosio"] = "NOT DEFINED"

    try:
        map["EOSIO_ABIGEN"] = abigen_exe()
    except:
        map["EOSIO_ABIGEN"] = "NOT DEFINED"
    
    if contract_dir:
        contract_dir = contract_dir(contract_dir)
        try:
            map["contract-dir"] = contract_dir
        except:
            map["contract-dir"] = "NOT DEFINED"

        try:
            map["contract-wast"] = wast_file(contract_dir)
        except:
            map["contract-wast"] = "NOT DEFINED"

        try:
            map["contract-wasm"] = wasm_file(contract_dir)
        except:
            map["contract-wasm"] = "NOT DEFINED"

        try:
            map["contract-abi"] = abi_file(contract_dir)
        except:
            map["contract-abi"] = "NOT DEFINED"

    return map        

