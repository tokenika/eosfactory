import sys
from  eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG]
_ = Logger()

CONTRACT_WORKSPACE = sys.path[0] + "/../"

def test():
    _.SCENARIO('''
    Execute simple actions, debug buffer and authority mismatch detection.
    ''')
    reset()
    create_wallet()
    create_master_account("account_master")

    _.COMMENT('''
    Build and deploy the contract:
    ''')
    create_account("account_host", account_master)
    contract = Contract(account_host, CONTRACT_WORKSPACE)
    contract.build(force=False)
    contract.deploy()

    _.COMMENT('''
    Create test accounts:
    ''')
    create_account("account_alice", account_master)
    create_account("account_carol", account_master)

    _.COMMENT('''
    Test an action for Alice, including the debug buffer:
    ''')
    account_host.push_action(
        "hi", {"user":account_alice}, account_alice)
    assert("account_alice" in account_host.debug_buffer)

    _.COMMENT('''
    Test an action for Carol, including the debug buffer:
    ''')
    account_host.push_action(
        "hi", {"user":account_carol}, account_carol)
    assert("account_carol" in account_host.debug_buffer)

    _.COMMENT('''
    WARNING: This action should fail due to authority mismatch!
    ''')
    set_is_testing_errors(True)
    action = account_host.push_action(
        "hi", {"user":account_carol})
    set_is_testing_errors(False)
    assert(account_host.action.error)

    stop()


if __name__ == "__main__":
    test()
