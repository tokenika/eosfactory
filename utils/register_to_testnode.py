

def register(testnode_url, account_object_name):

    import setup
    import logger
    import eosf
    import eosf_account
    import testnet_data

    from logger import Verbosity
    from eosf_wallet import Wallet
    from eosf_account import account_master_create

    _ = logger.Logger([Verbosity.TRACE, Verbosity.OUT])
    logger.set_is_testing_errors(False)
    logger.set_throw_error(True)
    setup.set_nodeos_address(testnode_url)

    if not eosf.is_running():
        print(
            "This test needs the testnode {} running, but it does not answer." \
                .format(testnode_url))
        return

    wallet = Wallet(file=True)
    account_master_create(account_object_name)

import argparse

parser = argparse.ArgumentParser(description='''
Given an url and the account object name, get registration data.
Apply the data to the registration form of the testnet.
Enter 'go' when ready.

Example:
    python3 register_to_testnode.py https://api.kylin-testnet.eospace.io account_master
''')
parser.add_argument("testnode_url")
parser.add_argument("account_object_name")

args = parser.parse_args()
register(args.testnode_url, args.account_object_name)
