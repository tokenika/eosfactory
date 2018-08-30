import setup
import front_end
import cleos
import eosf
import eosf_wallet
import eosf_account
import eosf_contract
import testnet_data

Permission = cleos.Permission
CreateKey = cleos.CreateKey
Logger = front_end.Logger
Verbosity = front_end.Verbosity

create_wallet = eosf_wallet.create_wallet
create_account = eosf_account.create_account
create_master_account = eosf_account.create_master_account

get_wallet = eosf_wallet.get_wallet


Contract = eosf_contract.Contract
ContractBuilder = eosf_contract.ContractBuilder
contract_workspace_from_template = \
     eosf_contract.contract_workspace_from_template

set_is_testing_errors = front_end.set_is_testing_errors
set_throw_error = front_end.set_throw_error

restart = eosf_account.restart

resume = eosf.resume
reset = eosf.reset
stop = eosf.stop

info = eosf.info
status = eosf.status

remove_testnet_files = eosf.remove_testnet_files
verify_testnet = eosf.verify_testnet

configure_testnet = setup.configure_testnet