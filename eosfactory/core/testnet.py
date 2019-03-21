import eosfactory.core.config as config
import eosfactory.core.setup as setup
import eosfactory.core.manager as manager
import eosfactory.core.errors as errors
import eosfactory.core.logger as logger


class Testnet:
    '''Testing *nodeos* node.

    Args:
        account_name (str): If set, the name of the *account*, otherwise the 
            node is considered local, and its name is *eosio*.
        owner_key (str): If set, the public owner key of the *account*.
        active_key (str): If set, the public active key of the *account*.
        url (str): If set, the URL of a remote *nodeos*, otherwise 
            a localhost URL.
        name (str): The name of the testnet. If  not set, the name is 
            synthesized from the argument *url*.
        reset (bool): If set and if local node, reset the node.

    Attributes:
        account_name (str): The name of the *account*.
        owner_key (str): The public owner key of the *account*.
        active_key (str): The public active key of the *account*.
        url (str): The URL of the *nodeos*.        
        name (str): The name of the testnet
    '''
    def __init__(
            self,  
            account_name, owner_key, active_key,
            url=None,
            name=None,
            reset=False):

        if not url:
            if reset:
                manager.reset()
            else:
                if not self.verify_production(throw_error=False):
                    manager.resume()
            setup.is_local_address = True

        self.account_name = account_name
        self.owner_key = owner_key
        self.active_key = active_key
        self.url = url
        self.name = name

    def __str__(self):
        return "{} {} {}".format(self.name, self.account_name, self.url)

    def configure(self, prefix=None):
        '''Set the testnet to be the listener to EOSFactory.
        '''
        setup.set_nodeos_address(self.url, prefix)

    def verify_production(self, throw_error=True):
        '''Check whether the node is active.

        Returns:
            bool: Whether the node is active.
        '''
        return manager.verify_testnet_production(throw_error)

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


def get_testnet(name=None, testnet=None, reset=False, raise_exception=True):
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
        return Testnet(None, None, None, reset=reset)

    if name:
        mapping = manager.read_map(TESTNET_FILE)
        if name in mapping:
            return Testnet(
                mapping[name]["account_name"],
                mapping[name]["owner_key"], mapping[name]["active_key"],
                mapping[name]["url"],
                mapping[name]["name"])
        elif name == "JUNGLE":
            return JUNGLE
        elif name == "KYLIN":
            return KYLIN
        else:
            if raise_exception:
                raise errors.Error('''
                Testnet *{}* is not defined in the testnet mapping.
                '''.format(name))
            else:
                return
    elif testnet:
        return Testnet(testnet[0], testnet[1], testnet[2], testnet[3])

    if raise_exception:
        raise errors.Error('''
            Cannot determine testnet.
            ''')


TESTNET_FILE = "testnet.json"


def add_testnet_to_mapping(testnet, name=None):
    '''Save the given :class:`.Testnet` object.

    Args:
        testnet (.Testnet): The object to be saved.
    '''
    add_to_mapping(
        testnet.account_name, 
        testnet.owner_key, testnet.active_key, testnet.url, name)
    

def add_to_mapping(account_name, owner_key, active_key, url, name=None):
    '''Save a :class:`.Testnet` object.

    Args:
        account_name (str): If set, the account name, otherwise the node is
            considered local, and the name is *eosio*.
        owner_key (str): If set, the public owner key of the *account*.
        active_key (str): If set, the public active key of the *account*.
        url (str): If set, the URL of a remote *nodeos*, otherwise 
            a localhost URL.
        name (str): If set, the name of the testnet.
    '''
    mapping = manager.read_map(TESTNET_FILE)
    testnet = {}
    testnet["account_name"] = account_name
    testnet["owner_key"] = owner_key
    testnet["active_key"] = active_key
    testnet["url"] = url
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


def LOCAL():
    return Testnet(
    "eosio",
    config.eosio_key_private(),
    config.eosio_key_public(),
    None,
    "LOCAL")


#: Testnet http;//145.239.133.201;8888
JUNGLE = Testnet(
    "nukjygmgkn3x",
    "5KXxczFPdcsLrCYpRRREfd4e2xVDTZZqBpZWmvxLZYxUbPzqrWL",
    "5KJLMupynNYFiM9gZWtDnDX55hbaF18EsWpFr8UvyJeADqbwN7A",
    "http://145.239.133.201:8888",
    "JUNGLE"
)


#: Testnet http;//145.239.133.201;9999
KYLIN = Testnet(
    "xlg3pao3idlq",
    "5JBbCwe3t6j63yerYmguRVWg7ZVDY3nKXzGYMwkR9y5w4appKhk",
    "5JYZU9xPS54NhnJrmgQWzVXxZCWpzsVUPS3SBZVZnsPUBFtV5YK",
    "http://145.239.133.201:9999",
    "KYLIN"
)

