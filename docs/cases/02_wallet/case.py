from eosfactory.eosf import *

reset()
info()

create_wallet()
create_master_account("master")
create_account("alice", master)
create_account("carol", master)
get_wallet().keys()

reboot()

resume()
info()

create_wallet()
get_wallet().keys()

reboot()

reset()
info()

create_wallet()
get_wallet().keys()

reboot()

create_wallet()
get_wallet().index()
get_wallet().open()
get_wallet().unlock()
get_wallet().import_key(config.eosio_key_private())
get_wallet().keys()
get_wallet().lock()
