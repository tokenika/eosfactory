import sys
from  eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG]
_ = Logger()

CONTRACT_WORKSPACE = sys.path[0] + "/../"

def test():
    _.SCENARIO('''
    Initialize the token and run a couple of transfers between different accounts.
    ''')
    reset()
    create_wallet()
    create_master_account("account_master")

    _.COMMENT('''
    Build & deploy the contract:
    ''')
    create_account("account_host", account_master)
    contract = Contract(account_host, CONTRACT_WORKSPACE)
    contract.build(force=False)
    contract.deploy()

    _.COMMENT('''
    Create test accounts:
    ''')
    create_account("account_alice", account_master)
    create_account("account_bob", account_master)
    create_account("account_carol", account_master)

    _.COMMENT('''
    Initialize the token and send some tokens to one of the accounts:
    ''')

    account_host.push_action(
        "create",
        {
            "issuer": account_master,
            "maximum_supply": "1000000000.0000 EOS",
            "can_freeze": "0",
            "can_recall": "0",
            "can_whitelist": "0"
        }, [account_master, account_host])

    account_host.push_action(
        "issue",
        {
            "to": account_alice, "quantity": "100.0000 EOS", "memo": ""
        },
        account_master)

    _.COMMENT('''
    Execute a series of transfers between the accounts:
    ''')

    account_host.push_action(
        "transfer",
        {
            "from": account_alice, "to": account_carol,
            "quantity": "25.0000 EOS", "memo":""
        },
        account_alice)
    assert("250000" in account_host.debug_buffer)

    account_host.push_action(
        "transfer",
        {
            "from": account_carol, "to": account_bob, 
            "quantity": "11.0000 EOS", "memo": ""
        },
        account_carol)
    assert("110000" in account_host.debug_buffer)

    account_host.push_action(
        "transfer",
        {
            "from": account_carol, "to": account_bob, 
            "quantity": "2.0000 EOS", "memo": ""
        },
        account_carol)
    assert("20000" in account_host.debug_buffer)

    account_host.push_action(
        "transfer",
        {
            "from": account_bob, "to": account_alice, \
            "quantity": "2.0000 EOS", "memo":""
        },
        account_bob)
    assert("20000" in account_host.debug_buffer)

    _.COMMENT('''
    Verify the outcome:
    ''')

    table_alice = account_host.table("accounts", account_alice)
    table_bob = account_host.table("accounts", account_bob)
    table_carol = account_host.table("accounts", account_carol)

    assert(table_alice.json["rows"][0]["balance"] == '77.0000 EOS')
    assert(table_bob.json["rows"][0]["balance"] == '11.0000 EOS')
    assert(table_carol.json["rows"][0]["balance"] == '12.0000 EOS')

    stop()


if __name__ == "__main__":
    test()
