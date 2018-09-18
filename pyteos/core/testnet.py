import shell.setup as setup
import core.manager as manager
import core.logger as logger


class Testnet:
    def __init__(
            self, url=None, 
            account_name=None, owner_key=None, active_key=None, 
            reset=False):

        if not url:
            if reset:
                manager.reset(verbosity=[logger.Verbosity.ERROR])
            else:
                manager.resume(verbosity=[logger.Verbosity.ERROR])
            import shell.account as account
            eosio = account.Eosio("account_master")
            setup.is_local_address = True
            account_name = eosio.name
            owner_key = eosio.owner_key.key_private
            active_key = eosio.active_key.key_private

        if not account_name or not owner_key or not active_key:
            logger.ERROR('''
        If the ``url`` is set, the ``account_name`` and keys have to be set, as well.
            ''')
        self.url = url
        self.account_name = account_name
        self.owner_key = owner_key
        self.active_key = active_key

    def configure(self, prefix=None):
        setup.set_nodeos_address(self.url, prefix)

    def verify_production(self):
        return manager.verify_testnet_production()

    def clear_cache(self):
        manager.clear_testnet_cache()

    def is_local(self):
        return manager.is_local_testnet()


def get_testnet(alias, testnet=None, reset=False):
    if not alias and not testnet:
        return Testnet(reset=reset)

    if alias:
        mapping = get_mapping()
        if alias in mapping:
            return Testnet(
                mapping[alias]["url"], mapping[alias]["account_name"],
                mapping[alias]["owner_key"], mapping[alias]["active_key"])
        elif alias == "JUNGLE":
            return JUNGLE
        elif alias == "KYLIN":
            return KYLIN
        else:
            logger.ERROR('''
            Testnet ``{}`` is not defined in the testnet mapping.
            '''.format(alias))
    elif testnet:
        return Testnet(testnet[0], testnet[1], testnet[2], testnet[3])

    logger.ERROR('''
        Cannot determine testnet.
        ''')


TESTNET_FILE = "testnet.json"

def get_mapping():
    return manager.read_map(TESTNET_FILE)

def save_mapping(mapping):
    manager.save_map(mapping, TESTNET_FILE)

def edit_mapping():
    manager.edit_map(TESTNET_FILE)

def add_to_mapping(url, account_name, owner_key, active_key, alias=None):
    mapping = get_mapping()
    testnet = {}
    testnet["url"] = url
    testnet["account_name"] = account_name
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
        logger.INFO('''
        Testnet mapping is empty.
        ''')
        return
    for alias, testnet in mapping.items():
        print("%25s: %13s @ %s" % (alias, testnet["account_name"], testnet["url"]))


JUNGLE = Testnet(
    "http://88.99.97.30:38888",
    "dgxo1uyhoytn",
    "5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY",
    "5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA"
)

KYLIN = Testnet(
    "https://api.kylin.alohaeos.com",
    "xlg3pao3idlq",
    "5JBbCwe3t6j63yerYmguRVWg7ZVDY3nKXzGYMwkR9y5w4appKhk",
    "5JYZU9xPS54NhnJrmgQWzVXxZCWpzsVUPS3SBZVZnsPUBFtV5YK"
)

# /mnt/c/Workspaces/EOS/eos/build/programs/cleos/cleos --url http://88.99.97.30:38888 get info
