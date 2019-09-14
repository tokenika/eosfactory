#!/usr/bin/env python3
"""Create an account on a remote public testnet
============================================
"""

import argparse
from argparse import RawTextHelpFormatter
import eosfactory.core.setup as setup
from eosfactory.eosf import *


def main():
    """
    usage::

        python3 -m eosfactory.register_testnet [-h] [-a ACCOUNT ACCOUNT ACCOUNT] url [alias]

    Given the url of a testnet, get registration data.
    The following example uses Jungle testnet. Jungle offers a list of testnet 
    endpoints::
    
        https://monitor.jungletestnet.io/#apiendpoints
    
    Let the endpoint (url) be::

        http://145.239.133.201:8888

    Also, Jungle has an account creation form::

        https://monitor.jungletestnet.io/#account
    
    The command line shown results with a definition of an account, 
    consisting of a name and pair of private keys. The user can feed 
    the account creation form with this definition::

        python3 -m eosfactory.register_testnet http://145.239.133.201:8888 JUNGLE1

    The last argument ``alias`` is the name of an entry added finally to the list 
    of EOSFactory testnets. After the process is concluded, the alias can be 
    used in any EOSFactory script, for example::

        manager.resume("JUNGLE1") # resume connection to the testnet
        create_master_account("MASTER", testnet="JUNGLE1")

    If additional arguments are given, denoted as ``--account`` (or ``-a``), 
    defining an existing account, then this account is verified, and possibly 
    added to the testnet cache, for example::

        python3 -m eosfactory.register_testnet http://145.239.133.201:8888 JUNGLE1 -a 5jejduh2w2cb 5KGVA3efMr4rZEWUxWQzD4k11sApFrjYwVYfsVqvBYge1AppHdh 5KAkkZLZVQbhJL6JnxodcBScgLi1LNv8yEX5LRXaWvXyoH87DK8

    Args:
        url: An URL of a public node offering access to the testnet.
        alias: The name of the entry created in the testnet cache.
        -h: show this help message and exit
        -a [ACCOUNT ACCOUNT ACCOUNT]: <account name> <owner key> <active key>
    """

    parser = argparse.ArgumentParser(description="""
Given the url of a testnet, get registration data. The following example 
uses Jungle testnet. It offers a list of testnet endpoints:
    https://monitor.jungletestnet.io/#apiendpoints

Let the endpoint (url) be
    http://145.239.133.201:8888

Also, Jungle has an account creation form:
    https://monitor.jungletestnet.io/#account

The command line shown results with a definition of an account, consisting 
of a name and pair of private keys. The user can feed the account creation 
form with this definition:
    python3 -m eosfactory.register_testnet http://145.239.133.201:8888 JUNGLE1

The last argument alias is the name of a final entry in the list 
of EOSFactory testnets. After the process is concluded, the alias can 
be used in any EOSFactory script, for example:

    manager.resume("JUNGLE1") # resume connection to the testnet
    create_master_account("MASTER", testnet="JUNGLE1")

If additional arguments are given, denoted as --account (or -a), 
defining an existing account, then this account is verified, and possibly 
added to the testnet cache, for example:
    python3 -m eosfactory.register_testnet http://145.239.133.201:8888 JUNGLE1 -a 5jejduh2w2cb 5KGVA3efMr4rZEWUxWQzD4k11sApFrjYwVYfsVqvBYge1AppHdh 5KAkkZLZVQbhJL6JnxodcBScgLi1LNv8yEX5LRXaWvXyoH87DK8
    """, formatter_class=RawTextHelpFormatter)

    parser.add_argument(
                "url",
                help="An URL of a public node offering access to the testnet")
    parser.add_argument(
                "alias", nargs="?", default=None, help="Testnet object name")
    parser.add_argument(
                        "name", default=None, 
                        help="Account name. It is random, if not set")
    parser.add_argument(
        "-a", "--account", nargs=3, help="<name> <owner key> <active key>")
    parser.add_argument(
                        "-p", "--private", action="store_true", 
                        help="If set, save private keys. Use with caution!")
    

    args = parser.parse_args()
    account_name = None
    owner_key = None
    active_key = None

    if args.name:
        account_name = args.name
    if args.account:
        account_name = args.account[0]
        owner_key = args.account[1]
        active_key = args.account[2]

    setup.set_nodeos_address(args.url)
    manager.is_testnet_active()
    import pdb; pdb.set_trace()
    master_account = create_master_account(
        None,
        account_name=account_name,
        owner_key_private=owner_key,
        active_key_private=active_key)

    if master_account:
        if args.private:
            testnet_module.add_to_mapping(
                master_account.name,
                master_account.owner_key.key_private, 
                master_account.active_key.key_private,
                args.url,
                args.alias)
        else:
            testnet_module.add_to_mapping(
                master_account.name,
                None,
                None,
                args.url,
                args.alias)

        testnet_module.testnets()

    # python3 -m eosfactory.register_testnet http://88.99.97.30:38888 jungle -a dgxo1uyhoytn 5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY 5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA


if __name__ == '__main__':
    main()


# JUNGLE1
# Account Name: 5jejduh2w2cb
# Owner Public Key: EOS6LkJUSLgfvzxzbY25L82dSBWobormyqnn1HLrZkGNZ2pWKysM7
# Active Public Key: EOS5NXvFfWqKyerzGUCjpQ7dmMDhKPsYQrGmSmihFebvXi8uAmVdv

# Owner Private Key: 5KGVA3efMr4rZEWUxWQzD4k11sApFrjYwVYfsVqvBYge1AppHdh
# Active Private Key: 5KAkkZLZVQbhJL6JnxodcBScgLi1LNv8yEX5LRXaWvXyoH87DK8