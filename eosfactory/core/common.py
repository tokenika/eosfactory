
import importlib

import eosfactory.core.setup as setup
import eosfactory.core.logger as logger
get_commands = importlib.import_module(".get", setup.light_full)


def get_block_trx_data(block_num):
    block = get_commands.GetBlock(block_num, is_verbose=False)
    trxs = block.json["transactions"]
    if not len(trxs):
        logger.OUT("No transactions in block {}.".format(block_num))
    else:
        for trx in trxs:
            logger.OUT(trx["trx"]["transaction"]["actions"][0]["data"])


def get_block_trx_count(block_num):
    block = get_commands.GetBlock(block_num, is_verbose=False)
    trxs = block.json["transactions"]
    if not len(trxs):
        logger.OUT("No transactions in block {}.".format(block_num))    
    return len(trxs)


def contract_is_built(contract_dir, wasm_file=None, abi_file=None):
    '''Check whether the given contract project has its ABI and WASM files.

    Args:
        contract_dir (str): A hint to the project root directory.
        wasm_file (str): If set, the WASM file.
        abi_file (str): If set, the ABI file.

    Returns:
        [<absolute contract dir>, <wasm file>, <abi file>]
    '''
    contract_path_absolute = config.contract_dir(contract_dir)
    if not contract_path_absolute:
        return []

    if wasm_file:
        if not os.path.isfile(os.path.join(contract_path_absolute, wasm_file)):
            return []
    else:
        wasm_file = config.wasm_file(contract_dir)
        if not wasm_file:
            return []

    if abi_file:        
        if not os.path.isfile(os.path.join(contract_path_absolute, abi_file)):
            return []
    else:
        abi_file = config.abi_file(contract_dir)
        if not abi_file:
            return []

    return [contract_path_absolute, wasm_file, abi_file]