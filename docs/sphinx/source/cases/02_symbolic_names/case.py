from  eosfactory import *

setup.is_translating = False

reset()
create_wallet()
create_master_account("master")
create_account("host", master)

contract = Contract(host, "02_eosio_token")
if not contract.is_built():
    contract.build()
contract.deploy()

host.push_action(
    "create", 
    {
        "issuer": master,
        "maximum_supply": "1000000000.0000 EOS",
        "can_freeze": "0",
        "can_recall": "0",
        "can_whitelist": "0"
    }, [master, host])

create_account("alice", master)
host.push_action(
    "issue",
    {
        "to": alice, "quantity": "100.0000 EOS", "memo": ""
    },
    master)

restart()
setup.is_translating = True

reset()
create_wallet()
create_master_account("master")
create_account("host", master)

contract = Contract(host, "02_eosio_token")
if not contract.is_built():
    contract.build()
contract.deploy()

host.push_action(
    "create", 
    {
        "issuer": master,
        "maximum_supply": "1000000000.0000 EOS",
        "can_freeze": "0",
        "can_recall": "0",
        "can_whitelist": "0"
    }, [master, host])

create_account("alice", master)
host.push_action(
    "issue",
    {
        "to": alice, "quantity": "100.0000 EOS", "memo": ""
    },
    master)

stop()