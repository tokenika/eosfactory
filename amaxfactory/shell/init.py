
import os
import amaxfactory.core.logger as logger
import amaxfactory.core.errors as errors
import amaxfactory.core.teos as teos
import amaxfactory.core.cleos as cleos
import amaxfactory.core.manager as manager
import amaxfactory.core.testnet as testnet
import amaxfactory.core.interface as interface
import amaxfactory.shell.wallet as wallet
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract


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

Account = account.Account
MasterAccount = account.MasterAccount
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

info = manager.info
status = manager.status

Testnet =  testnet.Testnet
get_testnet =  testnet.get_testnet
testnets =  testnet.testnets

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_WORKSPACE = "_wslqwjvacdyugodewiyd"

FACTORY_DIR = os.getenv("FACTORY_DIR")

CONTRACT_WASM_PATH = FACTORY_DIR + "/templates/wasm/"



def deploy_amax(admin):

    amax = new_master_account()
    amaxtoken = new_account(amax,'amax.token')
    
    smart = Contract(amaxtoken, 
        wasm_file=CONTRACT_WASM_PATH + 'amax/amax.token/amax.token.wasm',
        abi_file=CONTRACT_WASM_PATH + "amax/amax.token/amax.token.abi")
    smart.deploy()

    amaxtoken.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.00000000 AMAX"
        },
        permission=[(admin, Permission.ACTIVE), (amaxtoken, Permission.ACTIVE)])

    amaxtoken.push_action(
        "issue",
        {
            "to": admin, "quantity": "1000000000.00000000 AMAX", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))


    table_admin = amaxtoken.table("accounts", admin)
    assert table_admin.json["rows"][0]["balance"] == '1000000000.00000000 AMAX'


def deploy_apl_newbie(admin):

    amax = new_master_account()
    aplinktoken = new_account(amax,'aplink.token')
    aplinknewbie = new_account(amax,'aplinknewbie')

    smart = Contract(aplinktoken, 
        wasm_file=CONTRACT_WASM_PATH + 'aplink/aplink.token/aplink.token.wasm',
        abi_file=CONTRACT_WASM_PATH + "aplink/aplink.token/aplink.token.abi")
    smart.deploy()

    smart = Contract(aplinknewbie, 
        wasm_file=CONTRACT_WASM_PATH + 'aplink/aplink.newbie/aplink.newbie.wasm',
        abi_file=CONTRACT_WASM_PATH + "aplink/aplink.newbie/aplink.newbie.abi")
    smart.deploy()

    aplinktoken.set_account_permission(add_code=True)
    aplinknewbie.set_account_permission(add_code=True)

    aplinktoken.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.0000 APL"
        },
        permission=[(admin, Permission.ACTIVE), (aplinktoken, Permission.ACTIVE)])

    aplinktoken.push_action(
        "issue",
        {
            "to": admin, "quantity": "1000000000.0000 APL", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))


    table_admin = aplinktoken.table("accounts", admin)
    assert table_admin.json["rows"][0]["balance"] == '1000000000.0000 APL'


def deploy_mtoken(admin):

    amax = new_master_account()
    amaxmtoken = new_account(amax,'amax.mtoken')

    smart = Contract(amaxmtoken, 
        wasm_file=CONTRACT_WASM_PATH + 'xchain/amax.mtoken/amax.mtoken.wasm',
        abi_file=CONTRACT_WASM_PATH + "xchain/amax.mtoken/amax.mtoken.abi")
    smart.deploy()

    amaxmtoken.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.00000000 MBTC"
        },
        permission=[(admin, Permission.ACTIVE), (amaxmtoken, Permission.ACTIVE)])

    amaxmtoken.push_action(
        "issue",
        {
            "to": admin, "quantity": "1000000000.00000000 MBTC", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))

    amaxmtoken.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.00000000 METH"
        },
        permission=[(admin, Permission.ACTIVE), (amaxmtoken, Permission.ACTIVE)])

    amaxmtoken.push_action(
        "issue",
        {
            "to": admin, "quantity": "1000000000.00000000 METH", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))

    amaxmtoken.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.00000000 MBNB"
        },
        permission=[(admin, Permission.ACTIVE), (amaxmtoken, Permission.ACTIVE)])

    amaxmtoken.push_action(
        "issue",
        {
            "to": admin, "quantity": "1000000000.00000000 MBNB", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))

    amaxmtoken.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.000000 MUSDT"
        },
        permission=[(admin, Permission.ACTIVE), (amaxmtoken, Permission.ACTIVE)])

    amaxmtoken.push_action(
        "issue",
        {
            "to": admin, "quantity": "1000000000.000000 MUSDT", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))

    amaxmtoken.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.000000 MUSDC"
        },
        permission=[(admin, Permission.ACTIVE), (amaxmtoken, Permission.ACTIVE)])

    amaxmtoken.push_action(
        "issue",
        {
            "to": admin, "quantity": "1000000000.000000 MUSDC", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))

    table_admin = amaxmtoken.table("accounts", admin)
    assert table_admin.json["rows"][0]["balance"] == '1000000000.00000000 MBNB'
    assert table_admin.json["rows"][1]["balance"] == '1000000000.00000000 MBTC'
    assert table_admin.json["rows"][2]["balance"] == '1000000000.00000000 METH'
    assert table_admin.json["rows"][3]["balance"] == '1000000000.000000 MUSDC'
    assert table_admin.json["rows"][4]["balance"] == '1000000000.000000 MUSDT'
