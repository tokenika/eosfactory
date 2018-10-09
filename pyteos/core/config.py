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
    if not "EOSIO_EOSFACTORY_DIR" in os.environ:
        raise errors.Error('''
        EOSIO_EOSFACTORY_DIR not defined
        ''')

    file = os.path.join(os.environ["EOSIO_EOSFACTORY_DIR"], setup.CONFIG_JSON)

    if os.path.exists(file):
        return file
    
    with open(file, "w") as output:
        output.write("{}")
    logger.INFO('''Creating an empty config file: {}'''.format(file))
    return file


def config_map():
    path = config_file()
    if os.path.exists(path):
        with open(path, "r") as input:
            return json.load(input)

    raise errors.Error('''
    Cannot find the config json file.       
    ''')


def configValues(config_key):
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


def configValue(config_key):
    retval = configValues(config_key) 
    return retval[0] if retval else None


def getValidPath(config_key, findFile=None):
    '''Given a key to the config map, get a valid file system path.

    The key may map to a path either absolute or relative to the EOS 
    repository. Also, the path can be relative to the ``HOME`` environment
    variable.
    '''
    values = configValues(config_key)
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
            path = os.path.join(getSourceDir(), path)
            if findFile:
                if os.path.exists(os.path.join(path, findFile)):
                    return path
            else:
                if os.path.exists(path):
                    return path

    return None


def getEosFactoryDir():
    config_value = configValue("EOSIO_EOSFACTORY_DIR")
    if config_value:
        return config_value

    raise errors.Error('''
        Cannot determine the context directory.
    ''')


def getSourceDir():
    config_value = configValue("EOSIO_SOURCE_DIR")
    if config_value:
        return config_value

    raise errors.Error('''
        Cannot determine the EOSIO source directory.
    ''')


def getGenesisJson():
    path = configValue("EOSIO_GENESIS_JSON")
    if not os.path.isabs(path):
        path = os.path.join(getConfigDir(), path)
    if os.path.isfile(path):
        return path

    raise errors.Error('''
        Cannot determine the genesis file. 
        Tried path is
        {}
    '''.format(path))


def getContractDir(contract_dir_hint):
    ''' Given a hint, determine the contract directory.
    The contract directory is the container for the project of a contract. The 
    hint is probed to be one of the following pieces of information:
    the absolute path to a contract directory;
    the relative path to a contract directory, relative to the directory set with the EOSIO_CONTRACT_WORKSPACE variable;
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
    # set with the EOSIO_CONTRACT_WORKSPACE variable
    contract_dir = os.path.join(
        configValue("EOSIO_CONTRACT_WORKSPACE"), contract_dir_hint)
    trace = trace + contract_dir + "\n"
    if os.path.isdir(contract_dir):
        return contract_dir

    # ? the relative path to a contract directory, relative to the 
    # ``contracts`` directory in the repository of EOSFactory
    contract_dir = os.path.join(
            configValue("EOSIO_EOSFACTORY_DIR"), 
            setup.CONTRACTS_DIR, contract_dir_hint)
    trace = trace + contract_dir + "\n"
    if os.path.isdir(contract_dir):
        return contract_dir 

    # ? the relative path to a contract directory, relative to the 
    # ``contracts`` directory in the repository of EOSIO
    contract_dir = os.path.join(
            configValue("EOSIO_SOURCE_DIR"),
            setup.EOSIO_CONTRACT_DIR, contract_dir_hint)
    trace = trace + contract_dir + "\n"
    if os.path.isdir(contract_dir):
        return contract_dir 
    
    raise errors.Error('''
        Cannot determine the contract directory.
        Tried path list:
        {}
    '''.format(trace))


def getSourceFiles(source_path):
    srcs = []
    extensions = [".cpp", ".cxx", ".c", ".abi"]
    files = os.listdir(source_path)
    for file in files:
        path = os.path.join(source_path, file)
        if os.path.splitext(file)[1] in extensions:
            if os.path.isfile(path):
                srcs.append(path)
    return srcs
    

def getContractSourceFiles(contract_dir_hint):
    contract_dir = getContractDir(utils.wslMapWindowsLinux(contract_dir_hint))
    trace = contract_dir + "\n"

    srcs = getSourceFiles(contract_dir)
    if srcs:
        return srcs            

    source_path = os.path.join(contract_dir, "src")
    trace = trace + source_path + "\n"
    srcs = getSourceFiles(source_path)
    if srcs:
        return srcs            

    raise errors.Error('''
        Cannot find any contract source directory.
        Tried path list:
        {}
    '''.format(trace))


def getContractFile(contract_dir_hint, contract_file_hint):
    ''' Given contract dir and contract file hints, determine the file.

    Contract files are those extended with ``wast``, ``wasm`` and ``abi``.

    First, the ``contract_file_hint`` may be an absolute path.
    Next, it may be relative to the contract directory.

    The contract directory is the container for the project of a contract. This 
    directory is determined with the ``getContractDir`` function, basing on the 
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
    contract_dir = getContractDir(contract_dir_hint)

    # ? flat structure with all the files in this directory
    contract_file = os.path.join(contract_dir, contract_file_hint)
    trace = trace + contract_file + "\n"
    if os.path.isfile(contract_file):
        return contract_file

    # ? structure with a directory named ``build``
    # and ``contract_file_hint`` is relative file
    contract_file = os.path.join(contract_dir, "build", contract_file_hint)
    trace = trace + contract_file + "\n"
    if os.path.isfile(contract_file):
        return contract_file

    # ? structure with a directory named ``build``
    # and ``contract_file_hint`` is a file extension merely
    build_dir = os.path.join(contract_dir, "build")
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


def getContractWorkspace():
    '''Return the absolute path to the contract workspace of the user.
    '''
    workspacePath = configValue("EOSIO_CONTRACT_WORKSPACE")
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


def getEosioKeyPublic():
    return configValue("EOSIO_KEY_PUBLIC")


def getMemorySizeMb():
    return configValue("EOSIO_SHARED_MEMORY_SIZE_MB")


def is_nodeos_in_window():
    return configValue("NODEOS_IN_WINDOW")


def getHttpServerAddress():
    return configValue("EOSIO_DAEMON_ADDRESS")


def getHttpWalletAddress():
    return configValue("EOSIO_WALLET_ADDRESS")
    

def getDaemonExe():
    path = os.path.join(
            getSourceDir(), "build/programs/", configValue("EOSIO_DAEMON_NAME"),
            configValue("EOSIO_DAEMON_NAME"))
    trace = path + "\n"
    if os.path.exists(path):
        return path
 
    path = os.path.join(
        "/usr/local/bin", configValue("EOSIO_DAEMON_NAME"))
    trace = trace + path + "\n"
    if os.path.exists(path):
        return path

    raise errors.Error('''
        Cannot determine the EOS test node executable file. 
        Tried path list:
        {}
    '''.format(trace))


def getCleosExe():
    path = os.path.join(
        getSourceDir(), "build/programs/", configValue("EOSIO_CLI_NAME"), 
        configValue("EOSIO_CLI_NAME"))

    trace = path + "\n"
    if os.path.exists(path):
        return path       

    path = os.path.join("/usr/local/bin", configValue("EOSIO_CLI_NAME"))
    trace = trace + path + "\n"
    if os.path.exists(path):
        return path.string() 

    raise errors.Error('''
        Cannot determine the EOS cli executable file. 
        Tried path list:
        {}
    '''.format(trace))


def getDataDir():
    path = configValue("EOSIO_DATA_DIR")

    if not os.path.isabs(path):
        contextDir = configValue("EOSIO_EOSFACTORY_DIR")
        if contextDir:
            path = os.path.join(contextDir, path)

    if os.path.isdir(path):
        return path

    raise errors.Error('''
        Cannot determine the 'data-dir' directory. 
        Tried path is
        {}
    '''.format(path))      


def getConfigDir():
    path = configValue("EOSIO_CONFIG_DIR")
    if not os.path.isabs(path):
        contextDir = configValue("EOSIO_EOSFACTORY_DIR")
        if contextDir:
            path = os.path.join(contextDir, path)

    if os.path.isdir(path):
        return path

    raise errors.Error('''
        Cannot find the 'config-dir' directory. 
        Tried path is
        {}
    '''.format(path))         


def getKeosdWalletDir():
    if "U_HOME" in os.environ:
        home = os.environ["U_HOME"]
        return home + "/eosio-wallet/"
    return None


def getTeosDir():
    path = configValue("EOSIO_TEOS_DIR")

    if not os.path.isabs(path):        
        path = os.path.join(configValue(EOSIO_EOSFACTORY_DIR), path)
    
    if os.path.isdir(path):
        return path

    raise errors.Error('''
        Cannot find the teos directory. 
        Tried path is
        {}
    '''.format(path)) 


def getDaemonName():
    return configValue("EOSIO_DAEMON_NAME")


def getEOSIO_BOOST_INCLUDE_DIR():
    return getValidPath("EOSIO_BOOST_INCLUDE_DIR", "boost/version.hpp")


def getEOSIO_WASM_CLANG():
    return getValidPath("EOSIO_WASM_CLANG")


def getEOSIO_WASM_LLVM_LINK():
    return getValidPath("EOSIO_WASM_LLVM_LINK")      


def getEOSIO_S2WASM():
    return getValidPath("EOSIO_S2WASM")


def getEOSIO_WAST2WASM():
    return getValidPath("EOSIO_WAST2WASM")

def get_eosio_abigen():
    return getValidPath("EOSIO_ABIGEN")


def getEOSIO_WASM_LLC():
    return getValidPath("EOSIO_WASM_LLC")       


def get_abi_file(contract_dir):
    '''Given the contract directory, return the ABI file path relative.
    '''
    return os.path.relpath(
        getContractFile(contract_dir, ".abi"), contract_dir)


def get_wast_file(contract_dir):
    '''Given the contract directory, return the WAST file path relative.
    '''
    return os.path.relpath(
        getContractFile(contract_dir, ".wast"), contract_dir)


def get_wasm_file(contract_dir):
    '''Given the contract directory, return the WASM file path relative.
    '''
    return os.path.relpath(
        getContractFile(contract_dir, ".wasm"), contract_dir)


def current_config(contract_dir=None):
    map = {}
    try: 
        map["EOSIO_SOURCE_DIR"] = getSourceDir()
    except:
        map["EOSIO_SOURCE_DIR"] = "NOT DEFINED"

    try:
        map["EOSIO_EOSFACTORY_DIR"] = getEosFactoryDir()
    except:
        map["EOSIO_EOSFACTORY_DIR"] = "NOT DEFINED"   

    try: 
        map["EOSIO_DATA_DIR"] = getDataDir()
    except:
        map["EOSIO_DATA_DIR"] = "NOT DEFINED" 

    try:    
        map["EOSIO_CONFIG_DIR"] = getConfigDir()
    except:
        map["EOSIO_CONFIG_DIR"] = "NOT DEFINED"   

    try:    
        map["KEOSD_WALLET_DIR"] = getKeosdWalletDir()
    except:
        map["KEOSD_WALLET_DIR"] = "NOT DEFINED"   

    try:
        map["nodeExe"] = getDaemonExe()
    except:
        map["nodeExe"] = "NOT DEFINED"    

    try: 
        map["cleosExe"] = getCleosExe()
    except:
        map["cleosExe"] = "NOT DEFINED" 

    try:   
        map["genesisJson"] = getGenesisJson()
    except:
        map["genesisJson"] = "NOT DEFINED"   

    try:    
        map["EOSIO_DAEMON_ADDRESS"] = getHttpServerAddress() 
    except:
        map["EOSIO_DAEMON_ADDRESS"] = "NOT DEFINED"    

    try:
        map["EOSIO_KEY_PRIVATE"] = getEosioKeyPrivate()
    except:
        map["EOSIO_KEY_PRIVATE"] = "NOT DEFINED"    

    try:
        map["EOSIO_KEY_PUBLIC"] = getEosioKeyPublic()
    except:
        map["EOSIO_KEY_PUBLIC"] = "NOT DEFINED"

    try:
        map["EOSIO_WALLET_ADDRESS"] = getHttpWalletAddress() \
            if getHttpWalletAddress() else getHttpServerAddress()
    except:
        map["EOSIO_WALLET_ADDRESS"] = "NOT DEFINED"

    try:
        map["EOSIO_DAEMON_NAME"] = getDaemonName()
    except:
        map["EOSIO_DAEMON_NAME"] = "NOT DEFINED"

    try:
        map["EOSIO_WASM_CLANG"] = getEOSIO_WASM_CLANG()
    except:
        map["EOSIO_WASM_CLANG"] = "NOT DEFINED"

    try:
        map["EOSIO_BOOST_INCLUDE_DIR"] =  getEOSIO_BOOST_INCLUDE_DIR()
    except:
        map["EOSIO_BOOST_INCLUDE_DIR"] = "NOT DEFINED"

    try:
        map["EOSIO_WASM_LLVM_LINK"] = getEOSIO_WASM_LLVM_LINK()
    except:
        map["EOSIO_WASM_LLVM_LINK"] = "NOT DEFINED"

    try:
        map["EOSIO_WASM_LLC"] = getEOSIO_WASM_LLC()
    except:
        map["EOSIO_WASM_LLC"] = "NOT DEFINED"

    try:
        map["EOSIO_S2WASM"] = getEOSIO_S2WASM()
    except:
        map["EOSIO_S2WASM"] = "NOT DEFINED"

    try:
        map["EOSIO_WAST2WASM"] = getEOSIO_WAST2WASM()
    except:
        map["EOSIO_WAST2WASM"] = "NOT DEFINED"

    map["sharedMemory"] = getMemorySizeMb()
    map["NODEOS_IN_WINDOW"] = is_nodeos_in_window()

    try:
        map["contractWorkspace"] = configValue("EOSIO_CONTRACT_WORKSPACE")
    except:
        map["contractWorkspace"] = "NOT DEFINED"
    
    try:
        map["workspaceEosio"] = os.path.join(
                                    getSourceDir(), setup.EOSIO_CONTRACT_DIR)
    except:
        map["workspaceEosio"] = "NOT DEFINED"

    try:
        map["EOSIO_ABIGEN"] = get_eosio_abigen()
    except:
        map["EOSIO_ABIGEN"] = "NOT DEFINED"
    
    if contract_dir:
        contract_dir = getContractDir(contract_dir)
        try:
            map["contract-dir"] = contract_dir
        except:
            map["contract-dir"] = "NOT DEFINED"

        try:
            map["contract-wast"] = get_wast_file(contract_dir)
        except:
            map["contract-wast"] = "NOT DEFINED"

        try:
            map["contract-wasm"] = get_wasm_file(contract_dir)
        except:
            map["contract-wasm"] = "NOT DEFINED"

        try:
            map["contract-abi"] = get_abi_file(contract_dir)
        except:
            map["contract-abi"] = "NOT DEFINED"

    return map        

