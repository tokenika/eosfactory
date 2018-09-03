from  eosfactory import *
import argparse

def register_testnet(
    url, alias, account_name, owner_key, active_key):

    setup.set_nodeos_address(url)
    eosf.verify_testnet_production()
    # eosf.clear_testnet_cache()

    testnet_data.testnets()

    create_wallet(file=True)
    account_object_name = "account"
    create_master_account(
        account_object_name,
        account_name=account_name,
        owner_key=owner_key,
        active_key=active_key)

    if account_object_name in globals():
        testnet_data.add_to_map(
            url, account_name, 
            owner_key if owner_key else account.owner_key.key_private, 
            active_key if active_key else account.active_key.key_private,
            alias)

    testnet_data.testnets()

parser = argparse.ArgumentParser(description='''
Given an url and an testnet pseudo (not obligatory), get registration data.
Apply the data to the registration form of the testnet.
Enter 'go' when ready.

Example:
    python3 register_testnet.py https://api.kylin-testnet.eospace.io

If additional, flagged ``--orphan``, arguments are given then the completely 
defined account is checked for existence, and possibly added as a testnet entry.
''')

parser.add_argument("url", help="An URL of a public node offering access to the testnet, e.g. http://88.99.97.30:38888")
parser.add_argument("-p", "--pseudo", default=None, help="Testnet pseudo")
parser.add_argument(
            "-o", "--orphan", nargs=3,
            help="<name> <owner key> <active key>")

args = parser.parse_args()

account_name = None
owner_key = None
active_key = None
if args.orphan: 
    account_name = args.orphan[0]
    owner_key = args.orphan[1]
    active_key = args.orphan[2]

register_testnet(
    args.url, args.pseudo, account_name, owner_key, active_key)

# python3 register_testnet.py https://api.kylin-testnet.eospace.io --pseudo kylin2 --orphan dgxo1uyhoytn 5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY 5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA
