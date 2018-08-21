import setup
import logger
import eosf
import eosf_wallet
import eosf_account
import eosf_contract

Logger = logger.Logger
Verbosity = logger.Verbosity
Wallet = eosf_wallet.Wallet
account_create = eosf_account.account_create
account_master_create = eosf_account.account_master_create
Contract = eosf_contract.Contract
contract_workspace_from_template = \
     eosf_contract.contract_workspace_from_template

set_is_testing_errors = logger.set_is_testing_errors
set_throw_error = logger.set_throw_error

restart = eosf.restart
reset = eosf.reset
stop = eosf.stop
remove_files = eosf.remove_files

set_nodeos_address = setup.set_nodeos_address