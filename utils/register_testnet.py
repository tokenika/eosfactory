from  eosfactory import *
import argparse

def register_testnet(
    url, alias, account_name, owner_key, active_key):

    setup.set_nodeos_address(url)
    eosf_control.verify_testnet_production()
    eosf_control.clear_testnet_cache()

    eosf_testnet.testnets()

    create_wallet(file=True)
    account_object_name = "account"
    create_master_account(
        account_object_name,
        account_name=account_name,
        owner_key=owner_key,
        active_key=active_key)

    if account_object_name in globals():
        eosf_testnet.add_to_mapping(
            url, account_name,
            owner_key if owner_key else account.owner_key.key_private, 
            active_key if active_key else account.active_key.key_private,
            alias)

    eosf_testnet.testnets()

parser = argparse.ArgumentParser(description='''
Given an url and an testnet alias (not obligatory), get registration data.
Apply the data to the registration form of the testnet.
Enter 'go' when ready.

Example:
    python3 register_testnet.py https://api.kylin-testnet.eospace.io

If additional arguments are given, denoted as ``--account``, then the given 
account is checked for existence, and then added as a testnet master account.
''')

parser.add_argument("url", help="An URL of a public node offering access to the testnet, e.g. http://88.99.97.30:38888")
parser.add_argument("alias", nargs="?", default=None, help="Testnet alias")
parser.add_argument("-a", "--account", nargs=3, help="<name> <owner key> <active key>")

args = parser.parse_args()

account_name = None
owner_key = None
active_key = None
if args.account: 
    account_name = args.account[0]
    owner_key = args.account[1]
    active_key = args.account[2]

register_testnet(
    args.url, args.alias, account_name, owner_key, active_key)

# python3 utils/register_testnet.py http://88.99.97.30:38888 jungle -a dgxo1uyhoytn 5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY 5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA
