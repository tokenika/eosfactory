

def add_account(
    testnode_url, account_object_name,
    account_name, owner_key, active_key):

    import setup
    import front_end
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
    account_master_create(
        account_object_name,
        account_name,
        owner_key,
        active_key)

import argparse

parser = argparse.ArgumentParser(description='''
Given an testnet url, the account object name, account name, private owner and 
active keys, create an account object, and put it into the wallet that is 
associated with the url.

Example:
    python3 add_account.py https://api.kylin-testnet.eospace.io \
    account_master dgxo1uyhoytn \
    5K4rezbmuoDUyBUntM3PqxwutPU3rYKrNzgF4f3djQDjfXF3Q67 \
    5JCvLMJVR24WWvC6qD6VbLpdUMsjhiXmcrk4i7bdPfjDfNMNAeX
''')

parser.add_argument("testnode_url")
parser.add_argument("account_object_name")
parser.add_argument("account_name")
parser.add_argument("owner_key")
parser.add_argument("active_key")

args = parser.parse_args()
add_account(
    args.testnode_url, args.account_object_name,
    args.account_name, 
    args.owner_key, args.active_key
    )
