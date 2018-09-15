import eosf.setup
import eosf.core.cleos
import eosf.core.manager
import eosf.core.logger
import eosf.core.testnet
import eosf.interface
import eosf.wallet
import eosf.account
import eosf.contract

set_is_testing_errors = eosf.core.logger.set_is_testing_errors
verbosity = eosf.core.logger.verbosity
Verbosity = eosf.core.logger.Verbosity
SCENARIO = eosf.core.logger.SCENARIO
COMMENT = eosf.core.logger.COMMENT
TRACE = eosf.core.logger.TRACE
INFO = eosf.core.logger.INFO
OUT = eosf.core.logger.OUT
DEBUG = eosf.core.logger.DEBUG


CreateKey = eosf.core.cleos.CreateKey
Permission = eosf.interface.Permission

create_wallet = eosf.wallet.create_wallet
get_wallet = eosf.wallet.get_wallet

create_account = eosf.account.create_account
create_master_account = eosf.account.create_master_account
reboot = eosf.account.reboot

Contract = eosf.contract.Contract
ContractBuilder = eosf.contract.ContractBuilder
project_from_template = eosf.contract.project_from_template

reboot = eosf.account.reboot

reset = eosf.core.manager.reset
resume = eosf.core.manager.resume
stop = eosf.core.manager.stop

info = eosf.core.manager.info
status = eosf.core.manager.status

Testnet = eosf.core.testnet.Testnet
get_testnet = eosf.core.testnet.get_testnet
testnets = eosf.core.testnet.testnets
