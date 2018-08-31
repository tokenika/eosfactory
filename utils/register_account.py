from  eosfactory import *
import argparse

def register_account(
    testnode_url, account_object_name):

    set_nodeos_address(testnode_url)
    if not verify_testnet():
        return

    create_wallet(file=True)
    create_master_account(account_object_name)


parser = argparse.ArgumentParser(description='''
Given an url and the account object name, get registration data.
Apply the data to the registration form of the testnet.
Enter 'go' when ready.

Example:
    python3 register_to_testnode.py https://api.kylin-testnet.eospace.io master
''')

parser.add_argument("testnode_url")
parser.add_argument("account_object_name")

args = parser.parse_args()
register_account(
    args.testnode_url,
    args.account_object_name)
