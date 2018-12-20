'''
.. module:: eosfactory.core.cleos_get
    :platform: Unix, Darwin
    :synopsis: eosio cleos get commands.

.. moduleauthor:: Tokenika
'''

import types

import eosfactory.core.logger as logger
import eosfactory.core.interface as interface
import eosfactory.core.cleos as cleos


def get_info(is_verbose=1):
    '''Get current blockchain information.

    :param bool is_verbose: If ``False``, print a message. Default is ``True``.

    :return: A :class:`eosfactory.core.cleos.Cleos` object, extended with the 
        following items:

    :var str head_block_time: The time of the most recent block.
    :var int head_block: The most recent block number.
    :var int last_irreversible_block_num: The number of the most recent irreversible
        block.
    '''
    result = cleos.Cleos([], "get", "info", is_verbose)
    result.head_block = int(result.json["head_block_num"])
    result.head_block_time = result.json["head_block_time"]
    result.last_irreversible_block_num \
                            = int(result.json["last_irreversible_block_num"])
    result.printself()

    def __str__(self):
        return json.dumps(self.json, sort_keys=True, indent=4)

    result.__str__ = types.MethodType(__str__, result)
    
    return result


def get_block(block_number, block_id=None, is_verbose=True):
    '''Retrieve a full block from the blockchain.

    :param int block_number: The number of the block to retrieve.
    :param str block_id: The ID of the block to retrieve, if set, defaults to "".   
    :param bool is_verbose: If ``False``, print a message. Default is ``True``.
        
    :return: A :class:`eosfactory.core.cleos.Cleos` object.
    '''
    
    result = cleos.Cleos([block_id] if block_id else [str(block_number)], 
            "get", "block", is_verbose)

    def __str__(self):
        return json.dumps(self.json, sort_keys=True, indent=4)

    result.__str__ = types.MethodType(__str__, result)

    result.printself()

    return result


def get_block_trx_data(block_num):
    block = get_block(block_num, is_verbose=False)
    trxs = block.json["transactions"]
    if not len(trxs):
        logger.OUT("No transactions in block {}.".format(block_num))
    else:
        for trx in trxs:
            logger.OUT(trx["trx"]["transaction"]["actions"][0]["data"])


def get_block_trx_count(block_num):
    block = get_block(block_num, is_verbose=False)
    trxs = block.json["transactions"]
    if not len(trxs):
        logger.OUT("No transactions in block {}.".format(block_num))    
    return len(trxs)



