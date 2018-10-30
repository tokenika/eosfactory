import time
import subprocess
import json
import os

import eosfactory.core.errors as errors
import eosfactory.core.logger as logger
import eosfactory.core.setup as setup
import eosfactory.core.config as config
import eosfactory.core.cleos as cleos
import eosfactory.eosf as eosf

'''
python3 eosfactory/core/docker.py
'''

def is_docker():
    '''Detect the Docker, fitted properly.
    
    Proper fitting is nodeos, cleos, keosd, and -- wishfully -- eosio.cdt.
    '''
    return True


def cli_exe():
    '''Return a cleos executable.
    '''
    return config.cli_exe()


def url():
    '''Return the url of the local node.
    '''
    return "http://" + config.http_server_address()


def nodeos(args):
    '''Given the ``args``, reset or resume the local node asynchronously.
    '''
    args.insert(0, config.node_exe())
    # print(" ".join(args))

    subprocess.Popen(
        " ".join(args), 
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL, shell=True)

def stop():
    '''Stop the local node asynchronously.
    '''
    eosf.stop()


def abi(src_file, abi_file, options=[]):
    '''Given a source file and an output file path, make a corresponding abi file.
    '''
    cl = [config.eosio_abigen()]
    cl.extend(options)
    cl.extend(["--output", abi_file, src_file])
    # cl =  ['/usr/local/bin/eosio-abigen',
    # '--output',
    # abi_file,
    # src_file]       
    import eosfactory.core.teos as teos
    teos.process(cl)


def wasm(src_file, wasm_file, options=[]):
    '''Given a source file and an output file path, make a corresponding wasm file.
    '''
    cl = [config.eosio_cpp()]
    cl.extend(options)
    cl.extend(["-o", wasm_file, src_file])
    import eosfactory.core.teos as teos
    teos.process(cl)

###############################################################################
# test
###############################################################################

setup.set_nodeos_address(url())


def test():
    stop()
    nodeos([
        "--http-server-address", config.http_server_address(),
        "--data-dir", config.data_dir(),
        "--config-dir", config.config_dir(),
        "--chain-state-db-size-mb", config.chain_state_db_size_mb(),
        "--contracts-console",
        "--verbose-http-errors",
        "--enable-stale-production",
        "--producer-name eosio",
        "--signature-provider " + config.eosio_key_public() + "=KEY:" 
            + config.eosio_key_private(),
        "--plugin eosio::producer_plugin",
        "--plugin eosio::chain_api_plugin",
        "--plugin eosio::http_plugin",
        "--plugin eosio::history_api_plugin",
        "--genesis-json", config.genesis_json(),
        "--delete-all-blocks"
    ])
    node_probe()
    stop()
    if not node_probe():
        logger.TRACE("Confirmed, node is stopped.")

    nodeos([
        "--http-server-address", config.http_server_address(),
        "--data-dir", config.data_dir(),
        "--config-dir", config.config_dir(),
        "--chain-state-db-size-mb", config.chain_state_db_size_mb(),
        "--contracts-console",
        "--verbose-http-errors",
        "--enable-stale-production",
        "--producer-name eosio",
        "--signature-provider " + config.eosio_key_public() + "=KEY:" 
            + config.eosio_key_private(),
        "--plugin eosio::producer_plugin",
        "--plugin eosio::chain_api_plugin",
        "--plugin eosio::http_plugin",
        "--plugin eosio::history_api_plugin"
    ])
    node_probe()
    stop()

    src_file = os.path.join(
        config.eosf_dir(), "contracts/01_hello_world/src/hello_world.cpp")
        
        #"contracts/01_hello_world/src/hello_world.cpp")

    abi_file = os.path.join(
        config.eosf_dir(), "contracts/01_hello_world/build/hello_world.abi")
    abi(src_file, abi_file)
    
    wasm_file = os.path.join(
        config.eosf_dir(), "contracts/01_hello_world/build/hello_world.wasm")
    wasm(src_file, wasm_file)
        

def get_info():
    cl = [cli_exe(), "--url", url(), "get", "info"]
    process = subprocess.run(
        cl,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    err_msg = process.stderr.decode("utf-8")
    if err_msg:
        raise errors.Error(err_msg)
    _json = json.loads(process.stdout.decode("utf-8"))
    return _json["head_block_num"]    


def node_probe():
    count = 10
    num = 5
    block_num = None
    
    while True:
        time.sleep(1)
        
        try:
            count = count - 1
            head_block_num = int(get_info())
        except:
            head_block_num = 0
        finally:
            print(".", end="", flush=True)

        if block_num is None:
            block_num = head_block_num

        if head_block_num - block_num >= num:
            print()
            logger.INFO('''
            Local node is running. Block number is {}
            '''.format(head_block_num))
            return True      

        if count <= 0:
            return False


if __name__ == "__main__":
    test()