import amaxfactory.core.config as config
from amaxfactory.eosf import *

if __name__ == '__main__':
    stored = config.chain_state_db_size_mb_[1][0]
    config.chain_state_db_size_mb_[1][0] = "xxx"    
    reset()
    stop()
    config.chain_state_db_size_mb_[1][0] = stored
    