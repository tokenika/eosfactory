'''Issue set by patric-shih
'''
import sys, os
import eosfactory.core.config as config
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])

CONTRACT_WORKSPACE = os.path.join(config.eosf_dir(), "contracts/hello_world")

# Actors of the test:
MASTER = None
HOST = None
ALICE = None
CAROL = None

reset()
create_master_account("MASTER")

COMMENT('''
Build and deploy the contract:
''')
create_account("HOST", MASTER)
contract = Contract(HOST, CONTRACT_WORKSPACE)
contract.build(force=False)
contract.deploy()

COMMENT('''
Create test accounts:
''')
create_account("ALICE", MASTER)


# ALICE.set_account_permission(
#     Permission.ACTIVE, {
#         "threshold":
#             1,
#         "keys": [],
#         "accounts": [{
#             "permission": {
#                 "actor": str(ALICE),
#                 "permission": "active"
#             },
#             "weight": 1
#         }, {
#             "permission": {
#                 "actor": str(ALICE),
#                 "permission": "eosio.code"
#             },
#             "weight": 1
#         }]
#     }, Permission.OWNER, (ALICE, Permission.OWNER)) 

create_account("CAROL", MASTER)

COMMENT('''
Test an action for Alice:
''')
HOST.push_action(
    "hi", {"user":ALICE}, permission=(ALICE, Permission.ACTIVE))
assert("ALICE" in DEBUG())

COMMENT('''
Test an action for Carol:
''')
HOST.push_action(
    "hi", {"user":CAROL}, permission=(CAROL, Permission.ACTIVE))
assert("CAROL" in DEBUG())

stop()

