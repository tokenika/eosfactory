from urllib.request import Request, urlopen
import json
import argparse
import time
from eosf import *

CREATE_ACCOUNT_URL = "create_account"
GET_TOKEN_URL = "get_token"
HEADERS = {"User-Agent": "Mozilla/5.0"}
MAX_ATTEMPTS = 3
DELAY_IN_SECONDDS = 1

def register_testnet_kylin(
    faucet, url, alias):

    setup.set_nodeos_address(url)
    efman.verify_testnet_production()

    #efnet.testnets()
    account_name = cleos.account_name()

    registered = False
    path = faucet + "/" + CREATE_ACCOUNT_URL + "?" + account_name
    attempt = 1
    while not registered and attempt <= MAX_ATTEMPTS:
        efui.Logger().TRACE('''
        Registering account: {}
        '''.format(path))
        try:
            request = Request(path, headers=HEADERS)
            response = json.loads(urlopen(request).read())
            registered = True
        except:
            response = None
            attempt = attempt + 1
            account_name = cleos.account_name()
            path = faucet + "/" + CREATE_ACCOUNT_URL + "?" + account_name
            time.sleep(DELAY_IN_SECONDDS)

    if not response or response["msg"] != "succeeded":
        efui.Logger().ERROR('''
        Request failed: {}
        '''.format(path))

    if response["account"] != account_name:
        efui.Logger().ERROR('''
        Account names do not match: ``{}`` vs ``{}``
        '''.format(response["account"], account_name))

    owner_key = response["keys"]["owner_key"]["private"]
    active_key = response["keys"]["active_key"]["private"]

    efui.Logger().INFO('''
        Account ``{}`` successfully registered.
        '''.format(account_name))

    path = faucet + "/" + GET_TOKEN_URL + "?" + account_name
    attempt = 1
    while attempt <= MAX_ATTEMPTS:
        efui.Logger().TRACE('''
        Funding account: {}
        '''.format(path))
        try:
            request = Request(path, headers=HEADERS)
            response = json.loads(urlopen(request).read())
        except:
            response = None
        attempt = attempt + 1
        time.sleep(DELAY_IN_SECONDDS)

    if not response or response["msg"] != "succeeded":
        efui.Logger().ERROR('''
        Request failed: {}
        '''.format(path))

    efui.Logger().INFO('''
        Account ``{}`` successfully funded.
        '''.format(account_name))

    efnet.add_to_mapping(
        url, account_name, owner_key, active_key, alias)

    efnet.testnets()


parser = argparse.ArgumentParser()

parser.add_argument("faucet", help="An URL of a public faucet for the testnet, e.g. http://faucet.cryptokylin.io")
parser.add_argument("url", help="An URL of a public node offering access to the testnet, e.g. https://api.kylin.alohaeos.com")
parser.add_argument("alias", nargs="?", default=None, help="Testnet alias")

args = parser.parse_args()

register_testnet_kylin(
    args.faucet, args.url, args.alias)

# python3 utils/register_testnet_kylin.py http://faucet.cryptokylin.io https://api.kylin.alohaeos.com kylin