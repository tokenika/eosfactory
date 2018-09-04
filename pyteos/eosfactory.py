import setup
import front_end
import cleos
import eosf
import eosf_wallet
import eosf_account
import eosf_contract
import eosf_testnet


Logger = front_end.Logger
Verbosity = front_end.Verbosity

CreateKey = cleos.CreateKey
Permission = cleos.Permission

create_wallet = eosf_wallet.create_wallet
create_account = eosf_account.create_account
create_master_account = eosf_account.create_master_account

get_wallet = eosf_wallet.get_wallet

Contract = eosf_contract.Contract
ContractBuilder = eosf_contract.ContractBuilder
contract_workspace_from_template = \
     eosf_contract.contract_workspace_from_template

set_is_testing_errors = front_end.set_is_testing_errors
set_is_throwing_errors = front_end.set_is_throwing_errors

restart = eosf_account.restart

reset = eosf.reset
resume = eosf.resume
stop = eosf.stop

info = eosf.info
status = eosf.status

Testnet = eosf_testnet.Testnet
LocalTestnet = eosf_testnet.LocalTestnet
GetTestnet = eosf_testnet.GetTestnet
testnets = eosf_testnet.testnets

save_code = setup.save_code