import os
import setup
import eosf
import front_end
import eosf_account

class Testnet:
    def __init__(self, url, name, owner_key, active_key):
        self.url = url
        self.account_name = name
        self.owner_key = owner_key
        self.active_key = active_key

    def configure(self, prefix):
        setup.set_nodeos_address(self.url, prefix)

class GetTestnet(Testnet):
    def __init__(self, testnet):
        map = testnet_map()
        if testnet in map:
            Testnet.__init__(
            self, map[testnet]["url"], map[testnet]["name"],
            map[testnet]["owner_key"], map[testnet]["active_key"])
        else:
            if testnet == "cryptolion":
                return cryptolion
            if testnet == "kylin":
                return kylin

            front_end.Logger().ERROR('''
            Testnet ``{}`` is not defined in the testnet map.
            '''.format(testnet))

class LocalTestnet(Testnet):
    def __init__(self, reset=False):
        if reset:
            eosf.reset(verbosity=[front_end.Verbosity.ERROR])
        else:
            eosf.resume(verbosity=[front_end.Verbosity.ERROR])
        eosio = eosf_account.Eosio("account_master")

        setup.is_local_address = True
        Testnet.__init__(
            self, None, eosio.name,
            eosio.owner_key.key_private, eosio.active_key.key_private)


def add_to_map(url, name, owner_key, active_key, alias=None):
    map = testnet_map()
    testnet = {}
    testnet["url"] = url
    testnet["name"] = name
    testnet["owner_key"] = owner_key
    testnet["active_key"] = active_key
    if not alias:
        alias = setup.url_prefix(url)
    map[alias] = testnet
    save_testnet_map(map)


def remove_from_map(testnet):
    map = testnet_map()
    if testnet in map:
        del map[testnet]
        save_testnet_map(map)


cryptolion = Testnet(
    "http://88.99.97.30:38888",
    "dgxo1uyhoytn",
    "5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY",
    "5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA"
)

kylin = Testnet(
    "https://api.kylin-testnet.eospace.io",
    "dgxo1uyhoytn",
    "5K4rezbmuoDUyBUntM3PqxwutPU3rYKrNzgF4f3djQDjfXF3Q67",
    "5JCvLMJVR24WWvC6qD6VbLpdUMsjhiXmcrk4i7bdPfjDfNMNAeX"
)

# /mnt/c/Workspaces/EOS/eos/build/programs/cleos/cleos --url http://88.99.97.30:38888 get info

testnet_file = "testnet.json"
def testnet_map():
    return eosf.read_map(testnet_file)


def save_testnet_map(map):
    eosf.save_map(map, testnet_file)


def edit_testnet_map():
    eosf.edit_map(testnet_file)


def mapped():
    map = eosf.read_map(testnet_file)
    for pseudo, testnet in map.items():
        print("%20s: %13s @ %s" % (pseudo, testnet["name"], testnet["url"]))


{
    "cryptolion":
    {
        "url": "http://88.99.97.30:38888",
        "name": "dgxo1uyhoytn",
        "owner_key": "5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY",
        "active_key": "5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA"
    },
    "kylin":
    {
        "url": "https://api.kylin-testnet.eospace.io",
        "name": "dgxo1uyhoytn",
        "owner_key": "5K4rezbmuoDUyBUntM3PqxwutPU3rYKrNzgF4f3djQDjfXF3Q67",
        "active_key": "5JCvLMJVR24WWvC6qD6VbLpdUMsjhiXmcrk4i7bdPfjDfNMNAeX"     
    }
}
    


