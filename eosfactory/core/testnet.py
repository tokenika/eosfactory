import eosfactory.core.setup as setup
import eosfactory.core.manager as manager
import eosfactory.core.logger as logger


class Testnet:
    '''Testing *nodeos* node.

    Args:
        url (str): If set, the URL of a remote *nodeos*, otherwise 
            a localhost URL.
        account_name (str): If set, the name of the *account*, otherwise the 
            node is considered local, and its name is *eosio*.
        owner_key (str): If set, the public owner key of the *account*.
        active_key (str): If set, the public active key of the *account*.
        name (str): The name of the testnet. If  not set, the name is 
            synthesized from the argument *url*.
        reset (bool): If set and if local node, reset the node.

    Attributes:
        url (str): The URL of the *nodeos*.
        account_name (str): The name of the *account*.
        owner_key (str): The public owner key of the *account*.
        active_key (str): The public active key of the *account*.
        name (str): The name of the testnet
    '''
    def __init__(
            self, url=None, 
            account_name=None, owner_key=None, active_key=None,
            name=None,
            reset=False):

        if not url:
            if reset:
                manager.reset(verbosity=[logger.Verbosity.ERROR])
            else:
                manager.resume(verbosity=[logger.Verbosity.ERROR])
            import eosfactory.core.account as account
            eosio = account.Eosio("account_master")
            setup.is_local_address = True
            account_name = eosio.name
            owner_key = eosio.owner_key.key_private
            active_key = eosio.active_key.key_private

        if not account_name or not owner_key or not active_key:
            logger.ERROR('''
        If the *url* is set, the *account_name* and keys have to be set, as well.
            ''')
        self.url = url
        self.account_name = account_name
        self.owner_key = owner_key
        self.active_key = active_key
        self.name = name

    def configure(self, prefix=None):
        '''Set the testnet to be the listener to EOSFactory.
        '''
        setup.set_nodeos_address(self.url, prefix)

    def verify_production(self):
        '''Check whether the node is active.

        Returns:
            bool: Whether the node is active.
        '''
        return manager.verify_testnet_production()

    def clear_cache(self):
        '''Remove all the saved interaction with the testnet.

        Remove wallets ascribed to the testnet, its account map and password 
        map.
        '''
        manager.clear_testnet_cache()

    def is_local(self):
        '''Check whether EOSFactory is connected to the local testnet.

        Returns: 
            bool: Whether EOSFactory is connected to the local testnet.
        '''        
        return manager.is_local_testnet()


def get_testnet(name=None, testnet=None, reset=False):
    '''Return a testnet.

    Args:
        name (str): If set, the testnet name, otherwise the local testnet
            is returned.
        testnet (tuple): The tuple (<url> <name> <owner key> <active key>)
            representing a :class:`.Testnet` object, returned if the 
            *name* argument is not set.
        reset (bool): If both the *name* and *testnet* arguments are not 
            set, determine whether the local node is to be reset.

    Returns:
        :class:`.Testnet`: a testnet
    '''
    if not name and not testnet:
        return Testnet(reset=reset)

    if name:
        mapping = manager.read_map(TESTNET_FILE)
        if name in mapping:
            return Testnet(
                mapping[name]["url"], mapping[name]["account_name"],
                mapping[name]["owner_key"], mapping[name]["active_key"],
                mapping[name]["name"])
        elif name == "JUNGLE":
            return JUNGLE
        elif name == "KYLIN":
            return KYLIN
        else:
            logger.ERROR('''
            Testnet *{}* is not defined in the testnet mapping.
            '''.format(name))
    elif testnet:
        return Testnet(testnet[0], testnet[1], testnet[2], testnet[3])

    logger.ERROR('''
        Cannot determine testnet.
        ''')


TESTNET_FILE = "testnet.json"


def add_testnet_to_mapping(testnet, name=None):
    '''Save the given :class:`.Testnet` object.

    Args:
        testnet (.Testnet): The object to be saved.
    '''
    add_to_mapping(
        testnet.url, testnet.account_name, 
        testnet.owner_key, testnet.active_key, name)
    

def add_to_mapping(url, account_name, owner_key, active_key, name=None):
    '''Save a :class:`.Testnet` object.

    Args:
        url (str): If set, the URL of a remote *nodeos*, otherwise 
            a localhost URL.
        account_name (str): If set, the account name, otherwise the node is
            considered local, and the name is *eosio*.
        owner_key (str): If set, the public owner key of the *account*.
        active_key (str): If set, the public active key of the *account*.
        name (str): If set, the name of the testnet.
    '''
    mapping = manager.read_map(TESTNET_FILE)
    testnet = {}
    testnet["url"] = url
    testnet["account_name"] = account_name
    testnet["owner_key"] = owner_key
    testnet["active_key"] = active_key
    if not name:
        name = setup.url_prefix(url)
    testnet["name"] = name
    mapping[name] = testnet
    manager.save_map(mapping, TESTNET_FILE)


def remove_from_mapping(name):
    '''Remove from the record a testnet of the given name.

    The name of a testnet is set with the argument *name* argument of the 
    function :func:`.add_to_mapping`. If the argument is not set, the name is 
    synthesized from the argument *url*.

    Args:
        name (str): The name of the testnet to be removed.
    '''    
    mapping = manager.read_map(TESTNET_FILE)
    if name in mapping:
        del mapping[name]
        manager.save_map(mapping, TESTNET_FILE)


def testnets():
    '''Print recorded :class:`.Testnet` objects.
    '''
    mapping = manager.read_map(TESTNET_FILE)

    if not mapping:
        logger.INFO('''
        Testnet mapping is empty.
        ''')
        return
    for name, testnet in mapping.items():       
        print("%25s: %13s @ %s" % (name, testnet["account_name"], testnet["url"]))


#: Testnet http;//145.239.133.201;8888
JUNGLE = Testnet(
    "http://145.239.133.201:8888",
    "dgxo1uyhoytn",
    "5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY",
    "5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA",
    "JUNGLE"
)


#: Testnet http;//145.239.133.201;9999
KYLIN = Testnet(
    "http://145.239.133.201:9999",
    "xlg3pao3idlq",
    "5JBbCwe3t6j63yerYmguRVWg7ZVDY3nKXzGYMwkR9y5w4appKhk",
    "5JYZU9xPS54NhnJrmgQWzVXxZCWpzsVUPS3SBZVZnsPUBFtV5YK",
    "KYLIN"
)

