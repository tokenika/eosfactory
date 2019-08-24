
import importlib

import eosfactory.core.setup as setup
import eosfactory.core.logger as logger
import eosfactory.core.errors as errors
import eosfactory.core.teos as teos
BASE_COMMANDS = importlib.import_module(".base", setup.light_full)
import eosfactory.core.manager as manager
import eosfactory.core.testnet as testnet_module
import eosfactory.core.interface as interface
import eosfactory.shell.wallet as wallet
import eosfactory.shell.account as account
import eosfactory.shell.contract as contract


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

CreateKey = BASE_COMMANDS.CreateKey
Permission = interface.Permission

create_wallet = wallet.create_wallet
get_wallet = wallet.get_wallet

Account = account.Account
Account = account.Account
create_account = account.create_account
new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

print_stats = account.print_stats

Contract = contract.Contract
ContractBuilder = contract.ContractBuilder
project_from_template = teos.project_from_template

reboot = manager.reboot
reset = manager.reset
resume = manager.resume
stop = manager.stop
info = manager.is_testnet_active

Testnet =  testnet_module.Testnet
get_testnet =  testnet_module.get_testnet
testnets =  testnet_module.testnets
