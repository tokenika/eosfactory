import setup
import cleos
import eosf_ui
import eosf_control
import eosf_wallet
import eosf_account
import eosf_contract
import eosf_testnet


Logger = eosf_ui.Logger
Verbosity = eosf_ui.Verbosity

CreateKey = cleos.CreateKey
Permission = cleos.Permission

create_wallet = eosf_wallet.create_wallet
create_account = eosf_account.create_account
create_master_account = eosf_account.create_master_account

get_wallet = eosf_wallet.get_wallet

Contract = eosf_contract.Contract
ContractBuilder = eosf_contract.ContractBuilder
workspace_from_template = \
     eosf_contract.workspace_from_template

set_is_testing_errors = eosf_ui.set_is_testing_errors
set_is_throwing_errors = eosf_ui.set_is_throwing_errors

reboot = eosf_account.reboot

reset = eosf_control.reset
resume = eosf_control.resume
stop = eosf_control.stop

info = eosf_control.info
status = eosf_control.status

Testnet = eosf_testnet.Testnet
get_testnet = eosf_testnet.get_testnet
testnets = eosf_testnet.testnets
