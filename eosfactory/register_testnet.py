import argparse
import eosfactory.core.setup as setup
from eosfactory.eosf import *


def register_testnet_(url, alias, account_name, owner_key, active_key):
    setup.set_nodeos_address(url)
    manager.verify_testnet_production()

    #testnet.testnets()
    account = create_master_account(
        None,
        account_name=account_name,
        owner_key=owner_key,
        active_key=active_key)

    if account:
        testnet.add_to_mapping(
            account_name if account_name else account.name,
            owner_key if owner_key else account.owner_key.key_private, 
            active_key if active_key else account.active_key.key_private,
            url, 
            alias)

        testnet.testnets()


def main():
    '''
    usage: python3 -m eosfactory.register_testnet [-h] \
    [-a ACCOUNT ACCOUNT ACCOUNT] url [alias]

    Given an url and an testnet alias (not obligatory), get registration data.
    Apply the data to the registration form of the testnet. Enter 'go' when ready.
    
    Example using the jungle testnet https://monitor.jungletestnet.io/: 
    
    python3 -m eosfactory.register_testnet http://jungle2.cryptolions.io:80 jungle 
    
    If additional arguments are given, denoted as ``--account``, then the given
    account is checked for existence, and then added as a testnet master 
    account, for example:

    python3 -m eosfactory.register_testnet http://jungle2.cryptolions.io:80 jungle -a
    dgxo1uyhoytn 5K4rezbmuoDUyBUntM3PqxwutPU3rYKrNzgF4f3djQDjfXF3Q67
    5JCvLMJVR24WWvC6qD6VbLpdUMsjhiXmcrk4i7bdPfjDfNMNAeX

    Args:
        url: An URL of a public node offering access to the
                                testnet, e.g. http://jungle2.cryptolions.io:80
        alias: Testnet alias
        -h: show this help message and exit
        -a (ACCOUNT ACCOUNT ACCOUNT): <name> <owner key> <active key>
    '''
    parser = argparse.ArgumentParser(description='''
    Given an url and an testnet alias (not obligatory), get registration data.
    Apply the data to the registration form of the testnet.
    Enter 'go' when ready.

    Example:
        python3 -m eosfactory.register_testnet.py http://jungle2.cryptolions.io:80 jungle

    If additional arguments are given, denoted as ``--account``, then the given 
    account is checked for existence, and then added as a testnet master account.

        python3 -m eosfactory.register_testnet.py http://jungle2.cryptolions.io:80 jungle \
        -a dgxo1uyhoytn \
        5K4rezbmuoDUyBUntM3PqxwutPU3rYKrNzgF4f3djQDjfXF3Q67 \
        5JCvLMJVR24WWvC6qD6VbLpdUMsjhiXmcrk4i7bdPfjDfNMNAeX
    ''')

    parser.add_argument(
        "url", 
        help="An URL of a public node offering access to the testnet, e.g."                         "http://88.99.97.30:38888")
    parser.add_argument("alias", nargs="?", default=None, help="Testnet alias")
    parser.add_argument(
        "-a", "--account", nargs=3, help="<name> <owner key> <active key>")

    args = parser.parse_args()

    account_name = None
    owner_key = None
    active_key = None
    if args.account: 
        account_name = args.account[0]
        owner_key = args.account[1]
        active_key = args.account[2]

    register_testnet_(args.url, args.alias, account_name, owner_key, active_key)

    # python3 eosfactory.register_testnet http://88.99.97.30:38888 jungle -a dgxo1uyhoytn 5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY 5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA


if __name__ == '__main__':
    main()