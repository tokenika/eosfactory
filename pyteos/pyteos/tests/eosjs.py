import pyteos.setup as setup
import pyteos.core.teos as teos
from pyteos.core.eosjs import *
import pyteos.core.logger as logger

teos.node_start(True)
logger.INFO("node started")
logger.INFO("get info:")
get_info = GetInfo()
logger.INFO("get block:")
get_block = GetBlock(2)
logger.INFO("get last block:")
get_last_block()
logger.INFO("get block transaction data:")
get_block_trx_data(3)
logger.INFO("get block transaction count:")
get_block_trx_count(3)
