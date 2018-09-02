from  eosfactory import *
import argparse

def add_account(
    testnode_url, account_object_name,
    account_name, owner_key, active_key):

    set_nodeos_address(testnode_url)
    if not verify_testnet_production():
        return

    create_wallet(file=True)
    create_master_account(
        account_object_name,
        account_name,
        owner_key,
        active_key)


parser = argparse.ArgumentParser(description='''
Given a testnet url, the account object name, account name, private owner and 
active keys, create an account object, and put it into the wallet that is 
associated with the url.

Example:
    python3 add_account.py https://api.kylin-testnet.eospace.io \
    master \
    dgxo1uyhoytn \
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
    args.testnode_url,
    args.account_object_name,
    args.account_name,
    args.owner_key, args.active_key)
