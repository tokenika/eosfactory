from  eosfactory import *

Logger.verbosity = [Verbosity.TRACE, Verbosity.OUT, Verbosity.DEBUG]
set_throw_error(False)

_ = Logger()

def test():

    restart()
    set_is_testing_errors(False)
    set_throw_error(True)

    reset([Verbosity.INFO]) 
    wallet = Wallet()
    account_master_create("account_master")
    set_throw_error(False)
    set_is_testing_errors()

        ######################################################################        

    _.SCENARIO('''
With the master account, create four accounts: ``account_alice``, 
``account_bob``, account_carol`` and ``account_eosio_token``. Add the 
``eosio.token`` contract to the last account.
        ''')

    account_create("account_alice", account_master)
    account_create("account_bob", account_master)
    account_create("account_carol", account_master)
    account_create("account_eosio_token", account_master)
    
    import sys
    contract_eosio_token = Contract(account_eosio_token, sys.path[0] + "/../")
    deploy = contract_eosio_token.deploy()

    _.COMMENT('''
    Execute actions on the contract account:
        * let eosio deposit an amount of 1000000000.0000 EOS there;
        * transfer some EOS to the ``alice`` account.
    ''')

    account_eosio_token.push_action(
        "create", 
        '{"issuer":"' 
            + str(account_master) 
            + '", "maximum_supply":"1000000000.0000 EOS", \
            "can_freeze":0, "can_recall":0, "can_whitelist":0}')

    account_eosio_token.push_action(
        "issue",
        '{"to":"' + str(account_alice)
            + '", "quantity":"100.0000 EOS", '
            + '"memo":"issue 100.0000 EOS from eosio to alice"}',
        permission=account_master)

    _.COMMENT('''
    Execute a series of transfers between accounts:
    ''')

    account_eosio_token.push_action(
        "transfer",
        '{"from":"' + str(account_alice)
            + '", "to":"' + str(account_carol)
            + '", "quantity":"25.0000 EOS", '
            + '"memo":"transfer 25.0000 EOS from alice to carol"}',
        permission=account_alice)

    account_eosio_token.push_action(
        "transfer",
        '{"from":"' + str(account_carol)
            + '", "to":"' + str(account_bob)
            + '", "quantity":"11.0000 EOS", '
            + '"memo":"transfer 11.0000 EOS from carol to bob"}',
        permission=account_carol)

    account_eosio_token.push_action(
        "transfer",
        '{"from":"' + str(account_carol)
            + '", "to":"' + str(account_bob)
            + '", "quantity":"2.0000 EOS", '
            + '"memo":"transfer 2.0000 EOS from carol to bob"}',
        permission=account_carol)

    account_eosio_token.push_action(
        "transfer",
        '{"from":"' + str(account_bob)
            + '", "to":"' + str(account_alice)
            + '", "quantity":"2.0000 EOS", '
            + '"memo":"transfer 2.0000 EOS from bob to alice"}',
        permission=account_bob)                

    _.COMMENT('''
    See the records of the account:
    ''')

    table_alice = account_eosio_token.table("accounts", account_alice)
    table_bob = account_eosio_token.table("accounts", account_bob)
    table_carol = account_eosio_token.table("accounts", account_carol)

if __name__ == "__main__":
    test()
