from  eosfactory import *
import testnet_data
import argparse

def register_account(testnode_url, alias=None):

    set_nodeos_address(testnode_url)
    if not verify_testnet():
        return

    testnet_data.mapped()

    create_wallet(file=True)
    account_object_name = "account_master"
    create_master_account(account_object_name)

    if account_object_name in globals():
        testnet_data.add_to_map(
            testnode_url, account_master.name, 
            account_master.owner_key.key_private,
            account_master.active_key.key_private, alias)

    testnet_data.mapped()

parser = argparse.ArgumentParser(description='''
Given an url and an testnet pseudo (not obligatory), get registration data.
Apply the data to the registration form of the testnet.
Enter 'go' when ready.

Example:
    python3 register_to_testnode.py https://api.kylin-testnet.eospace.io master
''')

parser.add_argument("testnode_url", help="An URL of a public node offering access to the testnet, e.g. http://88.99.97.30:38888")
parser.add_argument("-p", "--pseudo", default=None, help="Testnet pseudo")

args = parser.parse_args()
register_account(args.testnode_url, args.pseudo)
