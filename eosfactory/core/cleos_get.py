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

    Args:
        is_verbose: If ``False``, do not print.

    Attributes:
        head_block: The most recent block number.
        head_block_time: The time of the most recent block.
        last_irreversible_block_num: The number of the most recent irreversible
            block.
    '''
    result = cleos.Cleos([], "get", "info", is_verbose)
    result.head_block = result.json["head_block_num"]
    result.head_block_time = result.json["head_block_time"]
    result.last_irreversible_block_num \
        = result.json["last_irreversible_block_num"]
    result.printself()

    def __str__(self):
        return json.dumps(self.json, sort_keys=True, indent=4)

    result.__str__ = types.MethodType(__str__, result)
    
    return result