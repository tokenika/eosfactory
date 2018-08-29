from  eosfactory import *

reset() 
create_wallet()
create_master_account("master")

create_account("alice", master)
create_account("bob", str(master))


set_throw_error(False)
create_account("charlie", CreateKey("xxx", is_verbose=0))
set_throw_error(True)


create_account(
    "carol", master, 
    permission=[
        (master, Permission.OWNER), 
        (master, Permission.ACTIVE)])

set_throw_error(False)
create_account(
    "eve", master, 
    permission=CreateKey("xxx", is_verbose=0))
set_throw_error(True)


create_account("host", master)
contract = Contract(host, "02_eosio_token")
contract.deploy()


host.push_action(
    "create",
    {
        "issuer": master,
        "maximum_supply": "1000000000.0000 EOS",
        "can_freeze": "0", 
        "can_recall": "0", 
        "can_whitelist": "0"
    }, 
    [master, host]) 

host.push_action(
    "issue",
    {
        "to": alice, "quantity": "100.0000 EOS", "memo": ""
    }, 
    permission=master)



host.push_action(
    "transfer",
    {
        "from": alice, "to": carol,
        "quantity": "5.0000 EOS", "memo":""
    },
    permission=alice)

host.push_action(
    "transfer",
    '''{
        "from": alice, "to": carol,
        "quantity": "5.1000 EOS", "memo":""
    }''',
    permission=alice)

host.push_action(
    "transfer",
    '{' 
        + '"from":' + str(alice) 
        + ', "to": ' + str(carol)
        + ', "quantity": "5.2000 EOS", "memo":""'
        + '}',
    permission=alice)