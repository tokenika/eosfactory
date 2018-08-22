from  eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT]
set_throw_error(False)
_ = Logger()

def test():

    _.SCENARIO('''
Set-up is that the local testnet is runnuning, after reseting, and it contains 
the "eosio_account" account that implements operations on tokens.

    ''')
    reset([Verbosity.INFO])
    wallet = Wallet()
    account_master_create("account_master")
    account_create("eosio_token", account_master)
    import sys
    contract = Contract(eosio_token, sys.path[0] + "/../")
    contract.build()
    contract.deploy()
    
    set_throw_error(False)
    set_is_testing_errors()         

    _.COMMENT('''
Create accounts "alice", "bob" and "carol":
    ''')

    account_create("alice", account_master)
    account_create("bob", account_master)
    account_create("carol", account_master)

    _.COMMENT('''
Initialize the contract and send some tokens to one of the accounts:
    ''')

    eosio_token.push_action(
        "create", 
        {
            "issuer": account_master,
            "maximum_supply": "1000000000.0000 EOS",
            "can_freeze": "0",
            "can_recall": "0",
            "can_whitelist": "0"
        }, [account_master, eosio_token])

    eosio_token.push_action(
        "issue",
        {
            "to": alice, "quantity": "100.0000 EOS", "memo": ""
        },
        account_master)

    _.COMMENT('''
    Execute a series of transfers between the accounts:
    ''')

    eosio_token.push_action(
        "transfer",
        {
            "from": alice, "to": carol,
            "quantity": "25.0000 EOS", "memo":""
        },
        alice)

    eosio_token.push_action(
        "transfer",
        {
            "from": carol, "to": bob, 
            "quantity": "11.0000 EOS", "memo": ""
        },
        carol)

    eosio_token.push_action(
        "transfer",
        {
            "from": carol, "to": bob, 
            "quantity": "2.0000 EOS", "memo": ""
        },
        carol)

    eosio_token.push_action(
        "transfer",
        {
            "from": bob, "to": alice, \
            "quantity": "2.0000 EOS", "memo":""
        },
        bob)

    _.COMMENT('''
    Verify the outcome:
    ''')

    table_alice = eosio_token.table("accounts", alice)
    table_bob = eosio_token.table("accounts", bob)
    table_carol = eosio_token.table("accounts", carol)

    stop()

if __name__ == "__main__":
    test()
