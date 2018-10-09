import sys
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])

CONTRACT_WORKSPACE = sys.path[0] + "/../"

def test():
    SCENARIO('''
    Execute simple actions.
    ''')
    reset()
    create_master_account("master")

    COMMENT('''
    Build and deploy the contract:
    ''')
    create_account("host", master)
    contract = Contract(host, CONTRACT_WORKSPACE)
    contract.build(force=False)
    contract.deploy()

    COMMENT('''
    Create test accounts:
    ''')
    create_account("alice", master)
    create_account("carol", master)

    COMMENT('''
    Test an action for Alice:
    ''')
    host.push_action(
        "hi", {"user":alice}, permission=(alice, Permission.ACTIVE))
    assert("alice" in DEBUG())

    COMMENT('''
    Test an action for Carol:
    ''')
    host.push_action(
        "hi", {"user":carol}, permission=(carol, Permission.ACTIVE))
    assert("carol" in DEBUG())

    stop()


if __name__ == "__main__":
    test()
