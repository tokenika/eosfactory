import pyteos.setup as setup
import pyteos.core.cleos as cleos
import pyteos.core.manager as manager
import pyteos.core.logger as logger
import pyteos.core.testnet as testnet
import pyteos.interface as interface
import pyteos.wallet as wallet
import pyteos.account as account
import pyteos.contract as contract
import pyteos.core.errors as errors

set_is_testing_errors =  logger.set_is_testing_errors
verbosity =  logger.verbosity
Verbosity =  logger.Verbosity
SCENARIO =  logger.SCENARIO

COMMENT =  logger.COMMENT
TRACE =  logger.TRACE
INFO =  logger.INFO
OUT =  logger.OUT
DEBUG =  logger.DEBUG

Error = errors.Error

CreateKey = cleos.CreateKey
Permission = interface.Permission

create_wallet = wallet.create_wallet
get_wallet = wallet.get_wallet

create_account = account.create_account
create_master_account = account.create_master_account
reboot = account.reboot
stats = account.stats

Contract = contract.Contract
ContractBuilder = contract.ContractBuilder
project_from_template = contract.project_from_template

reset = manager.reset
resume = manager.resume
stop = manager.stop

info = manager.info
status = manager.status

Testnet =  testnet.Testnet
get_testnet =  testnet.get_testnet
testnets =  testnet.testnets
