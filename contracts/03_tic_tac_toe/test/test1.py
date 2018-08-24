import sys
from  eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT]
_ = Logger()

CONTRACT_WORKSPACE = sys.path[0] + "/../"

def test():

    reset([Verbosity.INFO])

    create_wallet()
    create_master_account("account_master")
    create_account("croupier", account_master)
    create_account("alice", account_master)
    create_account("carol", account_master)
    contract = Contract(
        croupier, sys.path[0] + "/../")

    if not contract.is_built():
        contract.build()
    contract.deploy()        

    _.SCENARIO("""
Having created the ``croupier`` account that keeps the ``tic_tac_toe`` contract 
from the EOSIO distribution, and two players: ``alice`` and ``carol``, Run 
games.
    """)

    croupier.push_action(
        "create", 
        {
            "challenger": alice,
            "host": carol
        },
        carol)

    croupier.table("games", carol)

    croupier.push_action(
        "move", 
        {
            "challenger": alice,
            "host": carol,
            "by": carol, 
            "row": 0, "column": 0 
        }, 
        carol)

    croupier.push_action(
        "move", 
        {
            "challenger": alice, 
            "host": carol,
            "by": alice, 
            "row": 1, "column": 1 
        }, 
        alice)

    croupier.table("games", carol)

    croupier.push_action(
        "restart", 
        {
            "challenger": alice, 
            "host": carol,
            "by": carol
        }, 
        carol)

    t = croupier.table("games", carol)

    croupier.push_action(
        "close",
        {
            "challenger": alice,
            "host": carol
        }, 
        carol)

if __name__ == "__main__":
    test()