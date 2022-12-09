
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



def deploy_amax():

    amax = new_master_account()
    admin = new_account(amax,"admin")
    amax_token = new_account(amax,'amax.token')
    
    smart = Contract(amax_token, 
        wasm_file=CONTRACT_WASM_PATH + 'amax/amax.token/amax.token.wasm',
        abi_file=CONTRACT_WASM_PATH + "amax/amax.token/amax.token.abi")
    smart.deploy()

    amax_token.push_action(
        "create",
        {
            "issuer": admin,
            "maximum_supply": "1000000000.00000000 AMAX"
        },
        permission=[(admin, Permission.ACTIVE), (amax_token, Permission.ACTIVE)])

    amax_token.push_action(
        "issue",
        {
            "to": admin, "quantity": "1000000000.00000000 AMAX", "memo": ""
        },
        permission=(admin, Permission.ACTIVE))


    table_admin = amax_token.table("accounts", admin)
    assert table_admin.json["rows"][0]["balance"] == '1000000000.00000000 AMAX'
    
    return amax_token


def deploy_apl_newbie():

    amax = new_master_account()
    admin = new_account(amax,"admin")
    aplink_token = new_account(amax,'aplink.token')
    aplinknewbie = new_account(amax,'aplinknewbie')

    smart = Contract(aplink_token, 
        wasm_file=CONTRACT_WASM_PATH + 'aplink/aplink.token/aplink.token.wasm',
        abi_file=CONTRACT_WASM_PATH + "aplink/aplink.token/aplink.token.abi")
    smart.deploy()

    smart = Contract(aplinknewbie, 
        wasm_file=CONTRACT_WASM_PATH + 'aplink/aplink.newbie/aplink.newbie.wasm',
        abi_file=CONTRACT_WASM_PATH + "aplink/aplink.newbie/aplink.newbie.abi")
    smart.deploy()

    aplink_token.set_account_permission(add_code=True)
    aplinknewbie.set_account_permission(add_code=True)

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
    
    return aplink_token


def deploy_mtoken():

    amax = new_master_account()
    admin = new_account(amax,"admin")
    amax_mtoken = new_account(amax,'amax.mtoken')

    smart = Contract(amax_mtoken, 
        wasm_file=CONTRACT_WASM_PATH + 'xchain/amax.mtoken/amax.mtoken.wasm',
        abi_file=CONTRACT_WASM_PATH + "xchain/amax.mtoken/amax.mtoken.abi")
    smart.deploy()

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
    
    return amax_mtoken


def deploy_ntoken(name = "amax.ntoken"):

    amax = new_master_account()
    admin = new_account(amax,"admin")

    amax_ntoken = new_account(amax,name)
    
    smart = Contract(amax_ntoken, 
        wasm_file=CONTRACT_WASM_PATH + 'nftone/amax.ntoken/amax.ntoken.wasm',
        abi_file=CONTRACT_WASM_PATH + "nftone/amax.ntoken/amax.ntoken.abi")
    smart.deploy()

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
    
    return amax_ntoken


def deploy_farm():

    amax = new_master_account()
    admin = new_account(amax,"admin")

    aplink_farm = new_account(amax,'aplink.farm')
    
    smart = Contract(aplink_farm, 
        wasm_file=CONTRACT_WASM_PATH + 'aplink/aplink.farm/aplink.farm.wasm',
        abi_file=CONTRACT_WASM_PATH + "aplink/aplink.farm/aplink.farm.abi")
    smart.deploy()

    aplink_farm.set_account_permission(add_code=True)

    aplink_farm.pushaction(
        "init",
        {
            "landlord": admin,
            "jamfactory": admin,
            "last_lease_id":1,
            "last_allot_id":1
        },
        aplink_farm)

    return aplink_farm


def create_action_demo(file_name,contract_name,abi_file_path,dir):
        obj = json.load(open(abi_file_path))
        
        content = 'from amcli import runaction\nfrom base.baseClass import baseClass\n\n'
        demo = 'from amaxfactory.eosf import * \n\n'
        demo += f'def test_start():\n\treset()\n\tmaster = new_master_account()\n\t{file_name} = new_account("{contract_name}")\n'
        for action in obj['actions']:
            for struct in obj['structs']:
                struct_name = struct['name']
                if action['name'] == struct_name:
                    print(struct_name)
                    print(struct['fields'])
                    func = '\tdef ' + struct_name + '(self,'
                    body = f'''self.response = runaction(self.contract + f""" {struct_name} '['''
                    kv = ''
                    for key in struct['fields']:
                        key_type = key['type']
                        key_name = key['name']
                        value = ""
                        if key_type == 'name':
                            value = "'user1'"
                            body += '"{' + key_name + '}"' + ','
                        elif key_type == 'string':
                            value = "'x'"
                            body += '"{' + key_name + '}"' + ','
                        elif str(key_type).find('uint') >= 0:
                            value = 1
                            body += "{" + key_name + "}" + ','
                        elif key_type == 'symbol':
                            value = "'8,AMAX'"
                            body += '"{' + key_name + '}"' + ','
                        elif key_type == 'asset':
                            value = '"0.10000000 AMAX"'
                            body += '"{' + key_name + '}"' + ','
                        elif key_type == 'bool':
                            value = "'true'"
                            body += '"{' + key_name + '}"' + ','
                        else :
                            value = '1'
                            body += '"{' + key_name + '}"' + ','

                        kv += f'"{key_name}":{value},'
                    kv = "{"+kv+"},"
                    kv += "admin"
                    demo += f'\ndef test_{struct_name}():\n\t{file_name} = new_account("{contract_name}")\n\tadmin = new_account("admin")\n\t{file_name}.pushaction("{struct_name}",{kv}) \n'
                    func += kv
                    body = body[0:-1]
                    content += func + '):\n\t\t'
                    content += body + ''']' -p {suber}""") \n'''
                    content += '\t\treturn self\n\n'
        for table in obj['tables']:
            name = table['name']
            func = '\tdef ' + name + '(self,'
        # os.popen(f"mkdir {contract}case")
        # with open(f'/root/contracts/pythonProject1/{contract}case/{contract}.py', 'w', encoding='UTF-8') as file:
        #     file.write(content)
        
        print(dir)
        with open(f'{dir}/test_{file_name}demo.py', 'w', encoding='UTF-8') as file:
            file.write(demo)
