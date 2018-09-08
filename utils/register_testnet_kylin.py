from urllib.request import Request, urlopen
import json
import argparse
import time
from eosf import *

CREATE_ACCOUNT_URL = "http://faucet.cryptokylin.io/create_account"
GET_TOKEN_URL = "http://faucet.cryptokylin.io/get_token"
HEADERS = {"User-Agent": "Mozilla/5.0"}
MAX_ATTEMPTS = 3
DELAY_IN_SECONDDS = 1

parser = argparse.ArgumentParser()

parser.add_argument("url", help="An URL of a public node offering access to the testnet, e.g. https://api.kylin.alohaeos.com")
parser.add_argument("alias", nargs="?", default=None, help="Testnet alias")

args = parser.parse_args()

account_name = cleos.account_name()

registered = False
url = CREATE_ACCOUNT_URL + "?" + account_name
attempt = 1
while not registered and attempt <= MAX_ATTEMPTS:
    efui.Logger().TRACE('''
    Registering account: {}
    '''.format(url))
    try:
        request = Request(url, headers=HEADERS)
        response = json.loads(urlopen(request).read())
        registered = True
    except:
        response = None
        attempt = attempt + 1
        account_name = cleos.account_name()
        url = CREATE_ACCOUNT_URL + "?" + account_name
        time.sleep(DELAY_IN_SECONDDS)

if not response or response["msg"] != "succeeded":
    efui.Logger().ERROR('''
    Request failed: {}
    '''.format(url))

if response["account"] != account_name:
    efui.Logger().ERROR('''
    Account names do not match: ``{}`` vs ``{}``
    '''.format(response["account"], account_name))

owner_key = response["keys"]["owner_key"]["private"]
active_key = response["keys"]["active_key"]["private"]

efui.Logger().INFO('''
    Account ``{}`` successfully registered.
    '''.format(account_name))

url = GET_TOKEN_URL + "?" + account_name
attempt = 1
while attempt <= MAX_ATTEMPTS:
    efui.Logger().TRACE('''
    Funding account: {}
    '''.format(url))
    try:
        request = Request(url, headers=HEADERS)
        response = json.loads(urlopen(request).read())
    except:
        response = None
    attempt = attempt + 1
    time.sleep(DELAY_IN_SECONDDS)

if not response or response["msg"] != "succeeded":
    efui.Logger().ERROR('''
    Request failed: {}
    '''.format(url))

efui.Logger().INFO('''
    Account ``{}`` successfully funded.
    '''.format(account_name))

efnet.add_to_mapping(
    args.url, account_name, owner_key, active_key, args.alias)

efnet.testnets()
