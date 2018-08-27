import setup
import front_end
import cleos
import eosf
import eosf_wallet
import eosf_account
import eosf_contract

Permission = cleos.Permission
CreateKey = cleos.CreateKey

Logger = front_end.Logger
Verbosity = front_end.Verbosity
create_wallet = eosf_wallet.create_wallet

create_account = eosf_account.create_account
create_master_account = eosf_account.create_master_account
restart = eosf_account.restart

Contract = eosf_contract.Contract
ContractBuilder = eosf_contract.ContractBuilder
contract_workspace_from_template = \
     eosf_contract.contract_workspace_from_template

set_is_testing_errors = front_end.set_is_testing_errors
set_throw_error = front_end.set_throw_error

run = eosf.run
reset = eosf.reset
stop = eosf.stop
info = eosf.info
status = eosf.status
remove_files = eosf.remove_files
set_is_translating = eosf.set_is_translating
node_is_operative = eosf.node_is_operative

set_nodeos_address = setup.set_nodeos_address
is_local_address = setup.is_local_address