
import eosfactory.core.logger as logger
import eosfactory.core.errors as errors
import eosfactory.core.setup as setup
if setup.node_api == "cleos":
    import eosfactory.core.cleos as cleos
elif setup.node_api == "eosjs":
    import eosfactory.core.eosjs as cleos
import eosfactory.core.manager as manager
import eosfactory.core.testnet as testnet
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

CreateKey = cleos.CreateKey
Permission = interface.Permission

create_wallet = wallet.create_wallet
get_wallet = wallet.get_wallet

create_account = account.create_account
create_master_account = account.create_master_account

print_stats = account.print_stats

Contract = contract.Contract
ContractBuilder = contract.ContractBuilder
project_from_template = contract.project_from_template

reboot = manager.reboot
reset = manager.reset
resume = manager.resume
stop = manager.stop

info = manager.info
status = manager.status

Testnet =  testnet.Testnet
get_testnet =  testnet.get_testnet
testnets =  testnet.testnets
