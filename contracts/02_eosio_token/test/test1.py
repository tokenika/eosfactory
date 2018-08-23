import sys
from  eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT]
_ = Logger()

CONTRACT_WORKSPACE = sys.path[0] + "/../"

def test():
    _.SCENARIO('''
    First we create a series of accounts and delpoy the ``eosio.token`` contract
    to one of them. Then we initialize the token, and run a couple of transfers
    between those accounts.
    ''')
    reset([Verbosity.INFO])
    create_wallet()
    create_master_account("account_master")

    _.COMMENT('''
    Create a contract's hosting account, then build & deploy the contract:
    ''')
    create_account("account_host", account_master)
    contract = Contract(account_host, CONTRACT_WORKSPACE)
    contract.build()
    contract.deploy()

    _.COMMENT('''
    Create accounts "alice", "bob" and "carol":
    ''')
    create_account("alice", account_master)
    create_account("bob", account_master)
    create_account("carol", account_master)

    _.COMMENT('''
    Initialize the contract and send some tokens to one of the accounts:
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
            "to": alice, "quantity": "100.0000 EOS", "memo": ""
        },
        account_master)

    _.COMMENT('''
    Execute a series of transfers between the accounts:
    ''')

    account_host.push_action(
        "transfer",
        {
            "from": alice, "to": carol,
            "quantity": "25.0000 EOS", "memo":""
        },
        alice)

    account_host.push_action(
        "transfer",
        {
            "from": carol, "to": bob, 
            "quantity": "11.0000 EOS", "memo": ""
        },
        carol)

    account_host.push_action(
        "transfer",
        {
            "from": carol, "to": bob, 
            "quantity": "2.0000 EOS", "memo": ""
        },
        carol)

    account_host.push_action(
        "transfer",
        {
            "from": bob, "to": alice, \
            "quantity": "2.0000 EOS", "memo":""
        },
        bob)

    _.COMMENT('''
    Verify the outcome:
    ''')

    table_alice = account_host.table("accounts", alice)
    table_bob = account_host.table("accounts", bob)
    table_carol = account_host.table("accounts", carol)

    assert(table_alice.json["rows"][0]["balance"] == '77.0000 EOS')
    assert(table_bob.json["rows"][0]["balance"] == '11.0000 EOS')
    assert(table_carol.json["rows"][0]["balance"] == '12.0000 EOS')

    stop()


if __name__ == "__main__":
    test()
