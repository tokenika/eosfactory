"""Testnet definition"""

import eosfactory.core.config as config
import eosfactory.core.setup as setup
import eosfactory.core.errors as errors
import eosfactory.core.logger as logger


class Testnet:
    """Testnet definition.

    Remote public testnets provide environmet that mimic production conditions
    much better than the local testnode can do. An access to such a testnet
    can be done with an account registered with it.
    
    The class implements a definition of a remote testnet. First, it keeps the
    account name and the endpoint (url) of a testnet node. Additionally, the
    definition can include its name that can be used with operations involving
    a :class:`.core.testnet.Testnet` object.
    
    Also, the definition can include private keys owned by the account.
    Obviously, private key should be kept ciphered in wallets, however, with
    testing conditions it may be convenient to have them saved openly.

    Args:
        account_name (str): If set, the name of the account, otherwise the
            node is considered local, and its name is ``eosio``.
        owner_key_private (str): If set, the private owner key of the account.
        active_key_private (str): If set, the private active key of the account.
        url (str): If set, the URL of a remote ``nodeos``, otherwise
            a localhost URL.
        name (str): The name of the testnet. If  not set, the name is
            synthesized from the argument ``url``.

    Attributes:
        account_name (str): The name of the account.
        owner_key_private (str): The private owner key of the account.
        active_key_private (str): The private active key of the account.
        url (str): The URL of the ``nodeos``.
        name (str): The name of the testnet
    """
    def __init__(
            self,
            account_name, owner_key_private, active_key_private,
            url=None,
            name=None):

        if not url:
            setup.IS_LOCAL_ADDRESS = True

        self.account_name = account_name
        self.owner_key_private = owner_key_private
        self.active_key_private = active_key_private
        self.url = url
        self.name = name


    def __str__(self):
        return """name: {}
account_name: {}
url: {}
owner_key_private: {}
active_key_private: {}""".format(
            self.name, self.account_name, self.url, 
            self.owner_key_private, self.active_key_private)

        
def get_testnet(name=None, testnet=None, raise_exception=True):
    """Return a testnet.

    Args:
        name (str): If set, the testnet name, otherwise the local testnet
            is returned.
        testnet (tuple): The tuple (<url> <name> <owner key> <active key>)
            representing a :class:`.Testnet` object, returned if ``name`` is
            not set.

    Returns:
        :class:`.Testnet`: a testnet object.
    """
    if not name and not testnet:
        return Testnet(None, None, None)

    if name:
        mapping = setup.read_map(TESTNET_FILE)
        if name in mapping:
            return Testnet(
                mapping[name]["account_name"],
                mapping[name]["owner_key_private"], 
                mapping[name]["active_key_private"],
                mapping[name]["url"],
                mapping[name]["name"])
        elif name == "JUNGLE":
            return JUNGLE
        elif name == "KYLIN":
            return KYLIN
        else:
            if raise_exception:
                raise errors.Error("""
                Testnet ``{}`` is not defined in the testnet mapping.
                """.format(name))
            else:
                return
    elif testnet:
        return Testnet(testnet[0], testnet[1], testnet[2], testnet[3])

    if raise_exception:
        raise errors.Error("""
            Cannot determine testnet.
            """)


TESTNET_FILE = "testnet.json"


def LOCAL():
    return Testnet(
    "eosio",
    config.eosio_key_private(),
    config.eosio_key_private(),
    None,
    "LOCAL")


#: Testnet http;//145.239.133.201;8888
JUNGLE = Testnet(
    "hhidd2ekxrye",
    "5HxP3reTghfzLsUJ2o8JhiRz6qxcKLTDZtdVVHftfLDugNEEdpN",
    "5Jf8KWpgAkS6xg3PiPVimjZsrjKiBvjgGr3FiL3BTXqQkr6776Z",
# EOS7APzTZifdU1Ry5iS5SDm1cLVHtbMUGjRwD4XAT4VeHYBiCp4iw
# EOS5sAgrYj6vQSN9hXRaHstGSGpeUstmUAKvhFRsp5Qn8a2m533X5
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


def testnets():
    """Print recorded :class:`.Testnet` objects.
    """
    mapping = setup.read_map(TESTNET_FILE)

    if not mapping:
        logger.INFO("""
        Testnet mapping is empty.
        """)
        return
    print("%25s: %13s @ %s" % ("testnet name", "account_name", "url"))
    print("%25s: %13s @ %s" % ("=" * 25, "=" * 13, "=" * 25))
    global JUNGLE # pylint: disable=global-statement
    print("%25s: %13s @ %s" % (
                        JUNGLE.name, JUNGLE.account_name, JUNGLE.url))
    global KYLIN # pylint: disable=global-statement
    print("%25s: %13s @ %s" % (
                        KYLIN.name, KYLIN.account_name, KYLIN.url))
    for name, testnet in mapping.items():
        print("%25s: %13s @ %s" % (
                                name, testnet["account_name"], testnet["url"]))

    


def add_to_mapping(
    account_name, owner_key_private, active_key_private, url, name=None):
    """Save a :class:`.Testnet` object.

    Args:
        account_name (str): If set, the account name, otherwise the node is
            considered local, and the name is *eosio*.
        owner_key_private (str): If set, the private owner key of the account.
        active_key_private (str): If set, the private active key of the account.
        url (str): If set, the URL of a remote *nodeos*, otherwise 
            a localhost URL.
        name (str): If set, the name of the testnet.
    """
    mapping = setup.read_map(TESTNET_FILE)
    testnet = {}
    testnet["account_name"] = account_name
    testnet["owner_key_private"] = owner_key_private
    testnet["active_key_private"] = active_key_private
    testnet["url"] = url
    if not name:
        name = setup.url_prefix(url)
    testnet["name"] = name
    mapping[name] = testnet
    setup.save_map(mapping, TESTNET_FILE)


def add_testnet_to_mapping(testnet, name=None):
    """Save the given :class:`.Testnet` object.

    Args:
        testnet (.Testnet): The object to be saved.
    """
    add_to_mapping(
        testnet.account_name, 
        testnet.owner_key_private, testnet.active_key_private, testnet.url, name)


def remove_from_mapping(name):
    """Remove from the record a testnet of the given name.

    The name of a testnet is set with the argument *name* argument of the 
    function :func:`.add_to_mapping`. If the argument is not set, the name is 
    synthesized from the argument ``url``.

    Args:
        name (str): The name of the testnet to be removed.
    """    
    mapping = setup.read_map(TESTNET_FILE)
    if name in mapping:
        del mapping[name]
        setup.save_map(mapping, TESTNET_FILE)  