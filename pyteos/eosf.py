import core.cleos as cleos
import core.manager as manager
import core.logger as logger
import core.testnet as testnet
import core.errors as errors
import shell.setup as setup
import shell.interface as interface
import shell.wallet as wallet
import shell.account as account
import shell.contract as contract


verbosity =  logger.verbosity
Verbosity =  logger.Verbosity

SCENARIO =  logger.SCENARIO
COMMENT =  logger.COMMENT
TRACE =  logger.TRACE
INFO =  logger.INFO
OUT =  logger.OUT
DEBUG =  logger.DEBUG

Error = errors.Error
LowRamError = errors.LowRamError
MissingRequiredAuthorityError = errors.MissingRequiredAuthorityError
DuplicateTransactionError = errors.DuplicateTransactionError

CreateKey = cleos.CreateKey
Permission = interface.Permission

create_wallet = wallet.create_wallet
get_wallet = wallet.get_wallet

create_account = account.create_account
create_master_account = account.create_master_account

reboot = account.reboot
print_stats = account.print_stats

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
