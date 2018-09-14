import ef.setup
import ef.core.cleos
import ef.core.manager
import ef.core.logger
import ef.core.testnet
import ef.interface
import ef.wallet
import ef.account
import ef.contract

set_is_testing_errors = ef.core.logger.set_is_testing_errors
verbosity = ef.core.logger.verbosity
Verbosity = ef.core.logger.Verbosity
SCENARIO = ef.core.logger.SCENARIO
COMMENT = ef.core.logger.COMMENT
TRACE = ef.core.logger.TRACE
INFO = ef.core.logger.INFO
OUT = ef.core.logger.OUT
DEBUG = ef.core.logger.DEBUG


CreateKey = ef.core.cleos.CreateKey
Permission = ef.interface.Permission

create_wallet = ef.wallet.create_wallet
get_wallet = ef.wallet.get_wallet

create_account = ef.account.create_account
create_master_account = ef.account.create_master_account
reboot = ef.account.reboot

Contract = ef.contract.Contract
ContractBuilder = ef.contract.ContractBuilder
project_from_template = ef.contract.project_from_template

reboot = ef.account.reboot

reset = ef.core.manager.reset
resume = ef.core.manager.resume
stop = ef.core.manager.stop

info = ef.core.manager.info
status = ef.core.manager.status

Testnet = ef.core.testnet.Testnet
get_testnet = ef.core.testnet.get_testnet
testnets = ef.core.testnet.testnets
