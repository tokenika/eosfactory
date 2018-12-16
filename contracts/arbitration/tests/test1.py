
import time
import os
import sys
import eosfactory.core.config as config
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])
CONTRACT_WORKSPACE = sys.path[0] + "/../"
reset() # clean local node started
create_master_account("eosio")

# eosio.token name is hard-codded in the source of the contract:
create_account("Bank", eosio, "eosio.token")
contract_bank = Contract(
    Bank, os.path.join(config.eosf_dir(), "contracts/02_eosio_token"))
contract_bank.build(force=False)
contract_bank.deploy()

create_account("LC", eosio)
contract_lc = Contract(LC, CONTRACT_WORKSPACE)
contract_lc.build(force=False)
contract_lc.deploy()

COMMENT('''
LC.set_account_permission
''')
LC.set_account_permission(Permission.ACTIVE,
    {
        "threshold": 1,
        "accounts": 
            [
                {
                    "permission": 
                        {
                            "actor": LC,
                            "permission": "eosio.code"
                        },
                    "weight":1
                }
            ]
    },
    Permission.OWNER
)

Bank.push_action(
    "create", 
    {
        "issuer": eosio, 
        "maximum_supply": "1000000000.0000 SYS"
    }, [eosio, Bank])

create_account("Alice", eosio)
create_account("Carol", eosio)

Bank.push_action(
    "issue", 
    {
        "to": Alice, 
        "quantity": "100.0000 SYS", 
        "memo": ""
    }, eosio)

Bank.table("accounts", Alice)
Bank.table("accounts", Carol)

COMMENT('''
LC.push_action("opendeposit"
''')
LC.push_action(
    "opendeposit", {"buyer": Alice, "seller": Carol}, Alice)

COMMENT('''
Bank.push_action("transfer"
''')
Bank.push_action(
    "transfer", 
    {
        "from": Alice, 
        "to": LC, 
        "quantity": "10.0000 SYS", 
        "memo": str(Carol)
    }, Alice)

COMMENT('''
After transfer:
''')
Bank.table("accounts", Alice)
Bank.table("accounts", Carol)

COMMENT('''
LC.push_action("claim"
''')
LC.push_action(
    "claim", 
    {"buyer": Alice, "seller": Carol}, 
    Carol)

COMMENT('''
After Carol's claim:
''')
Bank.table("accounts", Alice)
Bank.table("accounts", Carol)

COMMENT('''
The ``LC`` contract need a time delay to arrange verify the deal:
''')
time.sleep(5)

COMMENT('''
LC.push_action("refund"
''')
LC.push_action(
    "refund", {"buyer": Alice, "seller": Carol}, Carol)

COMMENT('''
After refund:
''')
Bank.table("accounts", Alice)
Bank.table("accounts", Carol)

stop()
