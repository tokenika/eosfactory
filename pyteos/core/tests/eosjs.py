
import shell.setup as setup
setup.node_api = "eosjs"
import core.eosjs as eosjs
import core.cleos as cleos
import core.manager as manager
from eosf import *
import shell.wallet as wallet

reset()
# setup.is_print_command_line = True
create_master_account("master")
get_wallet().stop()


# setup.is_print_command_line = True
# reset()
# eosjs.WalletCreate("vvvv")
# create_wallet()
# create_master_account("account_master")
# get_wallet().keys()
# eosjs.GetInfo()
# eosjs.CreateKey("owner")
# exit()
# setup.is_print_command_line = True
# eosjs.GetAccount(account_master)
# eosjs.GetBlock(3)

# create_account("account_alice", account_master)
# create_account("account_carol", account_master)
# eosjs.GetAccount(account_carol)
# eosjs.GetAccounts(account_carol)

# # eosjs.GetAccount(str(account_alice))
# setup.is_print_command_line = True
# # eosjs.GetAccounts(account_carol.owner_key.key_public)
# owner_key = cleos.CreateKey("owner")
# eosjs.CreateAccount(account_master, None, owner_key)