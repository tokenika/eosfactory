from eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])

reset()
create_master_account("master")

create_account("host", master)
create_account("alice", master)
create_account("bob", master)
create_account("carol", master)

contract = Contract(host, "02_eosio_token")
if not contract.is_built():
    contract.build()
contract.deploy()

contract.push_action(
    "create", 
    {
        "issuer": master,
        "maximum_supply": "1000000000.0000 EOS",
        "can_freeze": "0",
        "can_recall": "0",
        "can_whitelist": "0"
    }, [master, host])
    
contract.push_action(
    "issue",
    {
        "to": alice, "quantity": "100.0000 EOS", "memo": ""
    },
    master)

contract.push_action(
    "transfer",
    {
        "from": alice, "to": carol,
        "quantity": "25.0000 EOS", "memo":""
    },
    alice)

contract.push_action(
    "transfer",
    {
        "from": carol, "to": bob, 
        "quantity": "11.0000 EOS", "memo": ""
    },
    carol)

contract.push_action(
    "transfer",
    {
        "from": carol, "to": bob, 
        "quantity": "2.0000 EOS", "memo": ""
    },
    carol)

contract.push_action(
    "transfer",
    {
        "from": bob, "to": alice, \
        "quantity": "2.0000 EOS", "memo":""
    },
    bob)

table_alice = host.table("accounts", alice)
table_bob = host.table("accounts", bob)
table_carol = host.table("accounts", carol)