#!/usr/bin/python3
"""API functions.
"""

import os
import sys
import json
import re
import inspect
import traceback
import time
import importlib
import subprocess

import eosfactory.core.config as config
import eosfactory.core.errors as errors
import eosfactory.core.logger as logger
import eosfactory.core.interface as interface
import eosfactory.core.testnet as testnet_module
import eosfactory.core.setup as setup
import eosfactory.core.teos as teos
BASE_COMMANDS = importlib.import_module(".base", setup.interface_package())
GET_COMMANDS = importlib.import_module(".get", setup.interface_package())


def user_error(error):
    print(str(error))
    stack = inspect.stack()
    traceback.print_stack(stack[2][0])
    sys.exit(1)


def accout_names_2_object_names(sentence, keys=False):
    """Translate blockchain account names to names of corresponding objects.

    Args:
        sentence (str): The message to be translated.
        keys (bool): If set, translate keys, as well.
    """
    if not setup.IS_TRANSLATING:
        return sentence
    exceptions = []
    map_ = account_map(do_not_fail=True)
    for name in map_:
        account_object_name = map_[name]
        if name in exceptions:
            continue
        sentence = sentence.replace("'" + name + "'", account_object_name)
        sentence = sentence.replace('"' + name + "'", account_object_name)
        sentence = sentence.replace(name, account_object_name)
        
        if keys:
            account = BASE_COMMANDS.GetAccount(name, is_verbose=False)
            owner_key = account.owner_public()
            if owner_key:
                sentence = sentence.replace(
                    "'" + owner_key + "'", account_object_name + "@owner")
                sentence = sentence.replace(
                    '"' + owner_key + '"', account_object_name + "@owner")
                sentence = sentence.replace(
                    owner_key, account_object_name + "@owner")

            active_key = account.active_public()
            if active_key:
                sentence = sentence.replace(
                    active_key, account_object_name + "@active")        

    return sentence


def object_names_2_accout_names(sentence, quatation_marks=False):
    """Translate account object names to corresponding blockchain account 
    names.

    Args:
        sentence (str): The message to be translated.
    """
    map_ = account_map(do_not_fail=True)
    for name in map_:
        account_object_name = map_[name]
        if quatation_marks:
            sentence = sentence.replace(
                account_object_name, '"' + name + '"')
        else:
            sentence = sentence.replace(account_object_name, name)

    return sentence


def is_local_testnet():
    """If not set, set local testnet. Is the current testnet local?
    """
    setup.set_local_nodeos_address_if_none()
    return setup.IS_LOCAL_ADDRESS


def node_start(clear=False, nodeos_stdout=None):
    """Start the local test node.

    Args:
        clear (bool): If set, remove persistence files 
            (wallet, account-mapping, passwords) associated with the current 
            testnet.
        nodeos_stdout (str): If set, a file where ``stdout`` stream of
            the local ``nodeos`` is send. Note that the file can be included to 
            the configuration of EOSFactory, see :func:`.core.config.nodeos_stdout`.
            If the file is set with the configuration, and in the same time 
            it is set with this argument, the argument setting prevails.
    """
    wait_time = 0.6
    try_count = 3

    while True:
        try:
            teos.node_start(clear, nodeos_stdout)
            teos.node_probe()
        except Exception as e: # pylint: disable=broad-except
            if not (clear and teos.ERR_MSG_IS_STUCK in str(e)):
                try_count = try_count - 1
                if try_count <= 0:
                    break
            else:
                teos.node_stop(verbose=False)
                time.sleep(wait_time)
        else:
            return

    teos.on_nodeos_error(clear)


def reset(    
    testnet=None,
    url=None,
    nodeos_stdout=None,
    prefix=None):
    """ Start clean an EOSIO node.

    With the local testnet, the procedure addresses problems with
    instabilities of the EOSIO ``nodeos`` executable: it happens that it is
    stuck on clean restart (perhaps with the WSL system only).

    The issue is patched with one subsequent restart if the first attempt
    fails. However, it happens that both launches fail, rarely due to 
    instability of ``nodeos``, sometimes because of misconfiguration.

    When both launch attempts fail, an exception routine passes. At first,
    the command line is printed, for ``example``::

        ERROR:
        The local ``nodeos`` failed to start few times in sequence. Perhaps, 
        something is wrong with configuration of the system. See the command line issued:

        /usr/bin/nodeosx 
        --http-server-address 127.0.0.1:8888 
        --data-dir /mnt/c/Workspaces/EOS/eosfactory/localnode/ 
        --config-dir /mnt/c/Workspaces/EOS/eosfactory/localnode/ 
        --chain-state-db-size-mb 200 --contracts-console --verbose-http-errors --enable-stale-production --producer-name eosio 
        --signature-provider EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV=KEY:5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3 
        --plugin eosio::producer_plugin 
        --plugin eosio::chain_api_plugin 
        --plugin eosio::http_plugin 
        --plugin eosio::history_api_plugin 
        --genesis-json /mnt/c/Workspaces/EOS/eosfactory/localnode/genesis.json
        --delete-all-blocks

    Next, the command line is executed, for example::

        Now, see the result of an execution of the command line.
        /bin/sh: 1: /usr/bin/nodeosx: not found

    The exemplary case is easy, it explains itself. Generally, the command 
    line given can be executed in a ``bash`` terminal separately, in order to 
    understand a problem.

    Args:
        testnet (:class:`.Testnet`): If set, resume the testnet listening at 
            the ``url`` attribute of the argument.
        url (str): If set, resume the testnet listening at ``url``.
        nodeos_stdout (str): If set, a file where ``stdout`` stream of
            the local ``nodeos`` is send. Note that the file can be included to 
            the configuration of EOSFactory, see :func:`.core.config.nodeos_stdout`.
            If the file is set with the configuration, and in the same time 
            it is set with this argument, the argument setting prevails. 
    """
    import eosfactory.shell.account as account
    account.reboot()

    if testnet:
        if isinstance(testnet, str):
            testnet = testnet_module.get_testnet(testnet)
        url = testnet.url
    if url:
        setup.set_nodeos_address(url, prefix)
    
    setup.set_local_nodeos_address_if_none()

    def remove_all_persistance_files():
        if setup.file_prefix():
            logger.TRACE("""
            Removing testnet cache for prefix `{}`
            """.format(setup.file_prefix()))

            teos.keosd_kill() # otherwise the manager may protects the wallet files
            wallet_dir = config.keosd_wallet_dir()
            files = os.listdir(wallet_dir)
            try:
                for file in files:
                    if file.startswith(setup.file_prefix()):
                        os.remove(os.path.join(wallet_dir, file))
            except Exception as e:
                raise errors.Error("""
                Cannot remove testnet cache. The error message is:
                {}
                """.format(str(e))) from e
            
            logger.TRACE("""
            Testnet cache successfully removed.
            """)

    if is_local_testnet():
        remove_all_persistance_files()
        node_start(clear=True, nodeos_stdout=nodeos_stdout)
    else:
        user_response = input(
            logger.WARNING("""
WARNING: The ``reset`` function will remove all persistance files associated 
with the current testnet {}, namely: 
the default wallet, object name map, password map.
Moreover, the testnet will be lost if it does not include private keys. 

A testnet object includes private keys if it is created with the command 
``python3 -m eosfactory.register_testnet`` with `-p` switch.

Do you want to continue? Enter Y to continue or anything else to stop <<<"""\
    .format(setup.nodeos_address())
            ) + " "
        )

        if not user_response == "Y":
            raise errors.Error("User's stop.")

        is_testnet_active() # Throws an error if not.
        logger.INFO("""
            Non-local nodeos is set: {}
            """.format(setup.nodeos_address()))
        remove_all_persistance_files()

    keosd_start()


def resume(testnet=None, url=None, nodeos_stdout=None, prefix=None):
    """ Resume an EOSIO node.

    Args:
        testnet (:class:`.Testnet`): If set, resume the testnet listening at the   ``url`` attribute of the argument.
        url (str): If set, resume the testnet listening at ``url``.
        nodeos_stdout (str): If set, a file where ``stdout`` stream of
            the local ``nodeos`` is send. Note that the file can be included to 
            the configuration of EOSFactory, see :func:`.core.config.nodeos_stdout`.
            If the file is set with the configuration, and in the same time 
            it is set with this argument, the argument setting prevails. 
    """
    import eosfactory.shell.account as account
    account.reboot()
    
    if testnet:
        if isinstance(testnet, str):
            testnet = testnet_module.get_testnet(testnet)
        url = testnet.url
    if url:
        setup.set_nodeos_address(url, prefix)
    
    setup.set_local_nodeos_address_if_none()

    if is_local_testnet():
        node_start(nodeos_stdout=nodeos_stdout)
    else:
        is_testnet_active() # Throws an error if not.
        logger.INFO("""
            Non-local nodeos is set: {}
            """.format(setup.nodeos_address()))

    keosd_start()
    

def stop():
    """ Stops keosd and all running EOSIO nodes."""
    teos.node_stop()
    teos.keosd_kill()


def is_testnet_active(throw_error=True):
    """If the testnet responses return the head block number, otherwise return 0.
    """
    domain = "LOCAL" if is_local_testnet() else "REMOTE"

    head_block = 0
    try:
        head_block = GET_COMMANDS.GetInfo(is_verbose=False).head_block
    except Exception as ex:
        if throw_error:
            raise errors.Error(str(ex)) from ex
        else:
             return ""
    
    logger.INFO("""
    {} testnet is active @ {}.
    """.format(domain, setup.nodeos_address()))

    return "Head block number is {}.".format(head_block)


def keosd_start():
    """Start eos wallet manager ``keosd``."""
    count = 5
    cl = [config.keosd_exe(), "--wallet-dir", config.keosd_wallet_dir()]
    while count > 0:
        if teos.get_pid(config.keosd_exe()):
            return
        count = count -1
        subprocess.Popen(
            cl, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL)

    if not count:
        raise errors.Error("""
Cannot start the eos wallet manager ``keosd``.
Bash command {} does not result in a process. 
    """.format(cl))


def account_map(do_not_fail=False): # pylint: disable=missing-docstring
    # """Return json account map.

    # Attempt to open the account map file named ``setup.ACCOUNT_MAP``, located 
    # in the wallet directory ``config.keosd_wallet_dir()``, to return its json 
    # contents. If the file does not exist, return the empty json.
    # """

    exception = None
    try:
        with open(os.path.join(
                                config.keosd_wallet_dir(),
                                setup.ACCOUNT_MAP), "r") as _:
                map_ = json.load(_)
    except Exception as ex: # pylint: disable=broad-except
        exception = ex

    if exception:
        if do_not_fail:
            return {}
        if isinstance(exception, FileNotFoundError):
            return {}

    return map_


def data_json(data): # pylint: disable=missing-docstring
    class Encoder(json.JSONEncoder): # pylint: disable=missing-docstring
        # """Redefine the method 'default'.
        # """
        def default(self, o): # pylint: disable=method-hidden
            if isinstance(o, interface.Account):
                return repr(o)
            return json.JSONEncoder.default(self, o)
            
    if not data:
        return "{}"

    data_json_ = data
    if isinstance(data, (dict, list)):
        data_json_ = json.dumps(data, cls=Encoder)
    else:
        if isinstance(data, str):
            data_json_ = re.sub(r"\s+|\n+|\t+", " ", data)
            data_json_ = object_names_2_accout_names(data_json_)
    return data_json_
