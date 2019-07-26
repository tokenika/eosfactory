
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