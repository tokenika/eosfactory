
from eosfactory.eosf import *

reset()

create_MASTER_account("MASTER")
create_account("HOST", MASTER)
create_account("ALICE", MASTER)
create_account("CAROL", MASTER)

contract = Contract(HOST, "eosio_token")
contract.build(force=False)
contract.deploy()

HOST.push_action(
    "create", 
    {
        "issuer": MASTER,
        "maximum_supply": "1000000000.0000 EOS"
    }, [MASTER, HOST])

setup.is_translating = False

HOST.push_action(
    "issue",
    {
        "to": ALICE, "quantity": "100.0000 EOS", "memo": ""
    },
    MASTER)

setup.is_translating = True

HOST.push_action(
    "issue",
    {
        "to": CAROL, "quantity": "100.0000 EOS", "memo": ""
    },
    MASTER)

stop()
