import sys
from pyteos.eosf import *

verbosity = [Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG]

CONTRACT_WORKSPACE = sys.path[0] + "/../"

def tests():
    SCENARIO('''
    Execute simple actions, debug buffer and authority mismatch detection.
    ''')
    reset()
    create_wallet()
    create_master_account("master")

    COMMENT('''
    Build and deploy the contract:
    ''')
    create_account("host", master)
    contract = Contract(host, CONTRACT_WORKSPACE)
    contract.build(force=False)
    contract.deploy()

    COMMENT('''
    Create tests accounts:
    ''')
    create_account("alice", master)
    create_account("carol", master)

    COMMENT('''
    Test an action for Alice, including the debug buffer:
    ''')
    host.push_action(
        "hi", {"user":alice}, permission=(alice, Permission.ACTIVE))
    assert("alice" in DEBUG())

    COMMENT('''
    Test an action for Carol, including the debug buffer:
    ''')
    host.push_action(
        "hi", {"user":carol}, permission=(carol, Permission.ACTIVE))
    assert("carol" in DEBUG())

    COMMENT('''
    WARNING: This action should fail due to authority mismatch!
    ''')
    try:
        host.push_action("hi", {"user":carol})
    except:
        pass

    stop()


if __name__ == "__main__":
    tests()
