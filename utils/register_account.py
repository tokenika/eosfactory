from eosf import *
import argparse

def register_account(
    url, account_object_name,
    account_name, owner_key, active_key):

    setup.set_nodeos_address(url)
    manager.verify_testnet_production()

    create_wallet(file=True)
    create_master_account(
        account_object_name,
        account_name,
        owner_key,
        active_key)


parser = argparse.ArgumentParser(description='''
Given a testnet url, the account object name, account name, private owner and 
active keys, create an account object and put it into the wallet associated 
with the url.

Example:
    python3 utils/register_account.py \
    http://88.99.97.30:38888 master uzpile1lv52y \
    5JxJPub9btDSnfk5iZd1QeuceYdigbyCUbmTMyEgbRbPNBa4Tgp \
    5JjrLM8LrBNVgmN9vQhgzVJn79UiShY9uw5ze6VwEygCeNWLKpR
''')

parser.add_argument("url")
parser.add_argument("account_object_name")
parser.add_argument("account_name")
parser.add_argument("owner_key")
parser.add_argument("active_key")

args = parser.parse_args()
register_account(
    args.url,
    args.account_object_name,
    args.account_name,
    args.owner_key, args.active_key)

# python3 utils/register_account.py http://88.99.97.30:38888 master uzpile1lv52y 5JxJPub9btDSnfk5iZd1QeuceYdigbyCUbmTMyEgbRbPNBa4Tgp 5JjrLM8LrBNVgmN9vQhgzVJn79UiShY9uw5ze6VwEygCeNWLKpR