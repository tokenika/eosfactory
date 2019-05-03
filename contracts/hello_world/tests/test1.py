import sys
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])

CONTRACT_WORKSPACE = sys.path[0] + "/../"

# Actors of the test:
MASTER = MasterAccount()
HOST = Account()
ALICE = Account()
CAROL = Account()

def test():
    SCENARIO('''
    Execute simple actions.
    ''')
    reset()
    create_master_account("MASTER")

    COMMENT('''
    Build and deploy the contract:
    ''')
    create_account("HOST", MASTER)
    smart = Contract(HOST, CONTRACT_WORKSPACE)
    smart.build(force=False)
    smart.deploy()

    COMMENT('''
    Create test accounts:
    ''')
    create_account("ALICE", MASTER)
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


if __name__ == "__main__":
    test()
