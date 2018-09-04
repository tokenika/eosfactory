import setup
import eosf
import front_end
import eosf_account


class Testnet:
    def __init__(
            self, url=None, 
            name=None, owner_key=None, active_key=None, 
            reset=False):

        if not url:
            if reset:
                eosf.reset(verbosity=[front_end.Verbosity.ERROR])
            else:
                eosf.resume(verbosity=[front_end.Verbosity.ERROR])
            eosio = eosf_account.Eosio("account_master")
            setup.is_local_address = True
            name = eosio.name
            owner_key = eosio.owner_key.key_private
            active_key = eosio.active_key.key_private

        if not name or not owner_key or not active_key:
            front_end.Logger().ERROR('''
        If the ``url`` is set, the ``name`` and keys have to be set, as well.
            ''')
        self.url = url
        self.account_name = name
        self.owner_key = owner_key
        self.active_key = active_key

    def configure(self, prefix=None):
        setup.set_nodeos_address(self.url, prefix)

    def verify_production(self):
        return eosf.verify_testnet_production()

    def clear_cache(self):
        eosf.clear_testnet_cache()


class GetTestnet(Testnet):
    def __init__(self, testnet):
        mapping = get_mapping()
        if testnet in mapping:
            Testnet.__init__(
            self, mapping[testnet]["url"], mapping[testnet]["name"],
            mapping[testnet]["owner_key"], mapping[testnet]["active_key"])
        else:
            if testnet == "cryptolion":
                return cryptolion
            if testnet == "kylin":
                return kylin

            front_end.Logger().ERROR('''
            Testnet ``{}`` is not defined in the testnet mapping.
            '''.format(testnet))


class LocalTestnet(Testnet):
    def __init__(self, reset=False):
        Testnet.__init__( self, reset=reset)


TESTNET_FILE = "testnet.json"

def get_mapping():
    return eosf.read_map(TESTNET_FILE)

def save_mapping(mapping):
    eosf.save_map(mapping, TESTNET_FILE)

def edit_mapping():
    eosf.edit_map(TESTNET_FILE)

def add_to_mapping(url, name, owner_key, active_key, alias=None):
    mapping = get_mapping()
    testnet = {}
    testnet["url"] = url
    testnet["name"] = name
    testnet["owner_key"] = owner_key
    testnet["active_key"] = active_key
    if not alias:
        alias = setup.url_prefix(url)
    mapping[alias] = testnet
    save_mapping(mapping)

def remove_from_mapping(testnet):
    mapping = get_mapping()
    if testnet in mapping:
        del mapping[testnet]
        save_mapping(mapping)

def testnets():
    mapping = get_mapping()
    if not mapping:
        front_end.Logger().INFO('''
        List is empty.
        ''')
        return
    for pseudo, testnet in mapping.items():
        print("%20s: %13s @ %s" % (pseudo, testnet["name"], testnet["url"]))

def get_testnet(alias):
    item = get_mapping()[alias]
    return Testnet(item["url"], item["name"], item["owner_key"], item["active_key"])


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
