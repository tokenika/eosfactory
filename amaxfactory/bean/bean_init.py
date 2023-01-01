

import json
import os
from amaxfactory.core.account import CreateAccount
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
from amaxfactory.bean.bean_list import *

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


def amax_token_init(bean):

    amax = new_master_account()
    admin = new_account(amax,"admin")
    
    bean.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.00000000 AMAX"
        },
        permission=[(admin, Permission.ACTIVE), (bean, Permission.ACTIVE)])

    bean.push_action(
        "issue",
        {
            "to": admin, "quantity": "800000000.00000000 AMAX", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))


    table_admin = bean.table("accounts", admin)
    assert table_admin.json["rows"][0]["balance"] == '800000000.00000000 AMAX'
    bean.push_action(
        "transfer",
        {
            "from":admin, "to": amax, "quantity": "100000000.00000000 AMAX", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))
   
    return bean


def aplink_token_init(bean):

    amax = new_master_account()
    admin = new_account(amax,"admin")
    aplink_token = bean
    aplinknewbie = APLINK_NEWBIE()
    

    aplink_token.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.0000 APL"
        },
        permission=[(admin, Permission.ACTIVE), (aplink_token, Permission.ACTIVE)])

    aplink_token.push_action(
        "issue",
        {
            "to": admin, "quantity": "1000000000.0000 APL", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))


    table_admin = aplink_token.table("accounts", admin)
    assert table_admin.json["rows"][0]["balance"] == '1000000000.0000 APL'
    
    return bean


def amax_mtoken_init(bean):

    amax = new_master_account()
    admin = new_account(amax,"admin")

    amax_mtoken = bean

    amax_mtoken.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.00000000 MBTC"
        },
        permission=[(admin, Permission.ACTIVE), (amax_mtoken, Permission.ACTIVE)])

    amax_mtoken.push_action(
        "issue",
        {
            "to": admin, "quantity": "1000000000.00000000 MBTC", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))

    amax_mtoken.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.00000000 METH"
        },
        permission=[(admin, Permission.ACTIVE), (amax_mtoken, Permission.ACTIVE)])

    amax_mtoken.push_action(
        "issue",
        {
            "to": admin, "quantity": "1000000000.00000000 METH", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))

    amax_mtoken.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.00000000 MBNB"
        },
        permission=[(admin, Permission.ACTIVE), (amax_mtoken, Permission.ACTIVE)])

    amax_mtoken.push_action(
        "issue",
        {
            "to": admin, "quantity": "1000000000.00000000 MBNB", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))

    amax_mtoken.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.000000 MUSDT"
        },
        permission=[(admin, Permission.ACTIVE), (amax_mtoken, Permission.ACTIVE)])

    amax_mtoken.push_action(
        "issue",
        {
            "to": admin, "quantity": "1000000000.000000 MUSDT", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))

    amax_mtoken.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.000000 MUSDC"
        },
        permission=[(admin, Permission.ACTIVE), (amax_mtoken, Permission.ACTIVE)])

    amax_mtoken.push_action(
        "issue",
        {
            "to": admin, "quantity": "1000000000.000000 MUSDC", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))

    table_admin = amax_mtoken.table("accounts", admin)
    assert table_admin.json["rows"][0]["balance"] == '1000000000.00000000 MBNB'
    assert table_admin.json["rows"][1]["balance"] == '1000000000.00000000 MBTC'
    assert table_admin.json["rows"][2]["balance"] == '1000000000.00000000 METH'
    assert table_admin.json["rows"][3]["balance"] == '1000000000.000000 MUSDC'
    assert table_admin.json["rows"][4]["balance"] == '1000000000.000000 MUSDT'
    
    return bean

def amax_ntoken_init(bean):

    amax = new_master_account()
    admin = new_account(amax,"admin")
    amax_ntoken = bean

    amax_ntoken.pushaction(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "10000",
            "symbol":[1,0],
            "token_uri":"xx",
            "ipowner":admin
        },
        admin)

    amax_ntoken.push_action(
        "issue",
        {
            "to": admin, 
            "quantity": [10000,[1,0]],
            "memo": ""
        },
        admin)

    amax_ntoken.pushaction(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "10000",
            "symbol":[2,0],
            "token_uri":"xxx",
            "ipowner":admin
        },
        admin)

    amax_ntoken.push_action(
        "issue",
        {
            "to": admin, 
            "quantity": [10000,[2,0]],
            "memo": ""
        },
        admin)



    table_admin = amax_ntoken.table("accounts", admin)
    assert table_admin.json["rows"][0]["balance"]["amount"] == 10000
    
    return bean


def aplink_farm_init(bean):

    amax = new_master_account()
    admin = new_account(amax,"admin")

    aplink_farm = bean
    
    aplink_farm.pushaction(
        "init",
        {
            "landlord": admin,
            "jamfactory": admin,
            "last_lease_id":1,
            "last_allot_id":1
        },
        aplink_farm)
    return bean

