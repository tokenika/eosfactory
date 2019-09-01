"""Base classes for CLEOS interface."""

import subprocess
import json as json_module
import pathlib
import random
import os
import re

import eosfactory.core.utils as utils
import eosfactory.core.errors as errors
import eosfactory.core.logger as logger
import eosfactory.core.config as config
import eosfactory.core.setup as setup
import eosfactory.core.interface as interface
import eosfactory.core.common as common


# http://www.sphinx-doc.org/domains.html#info-field-lists
class Command():
    """A prototype for ``EOSIO cleos`` commands.
    Calls ``EOSIO cleos``, and processes the responce.

    Args:
        args (list): List of ``EOSIO cleos`` positionals and options.
        command_group (str): Command group name.
        command (str): Command name.

    Attributes:
        out_msg (str): Responce received via the stdout stream.
        out_msg_details (str): Responce received via the stderr stream.
        err_msg (str): Error message received via the stderr stream.
        json (json): Responce received as JSON, if any.
        is_verbose (bool): If set, a message is printed.
        args (list): Value of the ``args`` argument.

    Raises:
        .core.errors.Error: If err_msg.
    """    
    def __init__(self, args, command_group, command, is_verbose=True):
        self.out_msg = None
        self.out_msg_details = None
        self.err_msg = None
        self.json = {}
        self.is_verbose = is_verbose
        self.args = args

        cl = [config.cli_exe()]
        setup.set_local_nodeos_address_if_none()
        cl.extend(["--url", utils.relay(
                            "http://" + config.RELY_URL, setup.nodeos_address(), 
                            setup.IS_PRINT_REQUEST, setup.IS_PRINT_RESPONSE)])

        cl.append(command_group)
        cl.extend(re.sub(re.compile(r'\s+'), ' ', command.strip()).split(" "))
        cl.extend(args)

        if setup.IS_SAVE_COMMAND_LINES:
            setup.add_to__COMMAND_LINE_FILE(" ".join(cl))        
        if setup.IS_PRINT_COMMAND_LINES:
            print("######## command line sent to cleos:")
            print(" ".join(cl))
            print("")
            
        while True:
            process = subprocess.run(
                                cl,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                cwd=str(pathlib.Path(config.cli_exe()).parent)) 

            self.out_msg = process.stdout.decode("ISO-8859-1")
            self.out_msg_details = process.stderr.decode("ISO-8859-1")
            self.err_msg = None
            error_key_words = ["ERROR", "Error", "error", "Failed"]
            for word in error_key_words:
                if word in self.out_msg_details:
                    self.err_msg = self.out_msg_details
                    self.out_msg_details = None
                    break

            if not self.err_msg:
                break
            if self.err_msg and not "Transaction took too long" in self.err_msg:
                break

        errors.validate(self)
            
        try:
            self.json = json_module.loads(self.out_msg)
        except:
            pass

        try:
            self.json = json_module.loads(self.out_msg_details)
        except:
            pass        

    def printself(self, is_verbose=False):
        """Print a message.

        Args:
            is_verbose (bool): If set, a message is printed.
        """
        if not hasattr(self, "is_verbose"):
            self.is_verbose = is_verbose

        if self.is_verbose:
            logger.OUT(self.__str__())

    def __str__(self):
        if self.err_msg:
            return self.err_msg
        else:
            out = self.out_msg
            if self.out_msg_details:
                out = out + self.out_msg_details
            return out

    def __repr__(self):
        return ""


def common_parameters(
        permission=None, 
        expiration_sec=None, 
        skip_sign=False, dont_broadcast=False, force_unique=False,
        max_cpu_usage=0, max_net_usage=0,
        ref_block=None,
        delay_sec=0
    ):
    """Common parameters.

    Args:
        permission (.interface.Account or str or (str, str) or \
            (.interface.Account, str) or any list of the previous items.): 
            An account and permission level to authorize.
        
    Exemplary values of the argument ``permission``::

        eosio # eosio is interface.Account object

        "eosio@owner"

        ("eosio", "owner")

        (eosio, interface.Permission.ACTIVE)

        ["eosio@owner", (eosio, .Permission.ACTIVE)]

    Args:
        expiration (int): The time in seconds before a transaction expires, 
            defaults to 30s
        skip_sign (bool): Specify if unlocked wallet keys should be used to 
            sign transaction.
        dont_broadcast (bool): Don't broadcast transaction to the network 
            (just print).
        force_unique(bool): Force the transaction to be unique. This will 
            consume extra bandwidth and remove any protections against 
            accidentally issuing the same transaction multiple times.
        max_cpu_usage (int): Upper limit on the milliseconds of cpu usage budget, 
            for the execution of the transaction (defaults to 0 which means no limit).
        max_net_usage (int): Upper limit on the net usage budget, in bytes, for the 
            transaction (defaults to 0 which means no limit).
        ref_block (int): The reference block num or block id used for TAPOS 
            (Transaction as Proof-of-Stake).
        delay_sec: The delay in seconds, defaults to 0s.
    """
    pass


class GetAccount(interface.Account, Command):
    """Retrieve an account from the blockchain.

    Args:
        account (str or .interface.Account): The account to retrieve.
        json: If set, prints the json representation of the object.
        is_verbose (bool): If ``False`` do not print. Default is ``True``.

    Attributes:
        name (str): The EOSIO name of the account.
        owner_key (str) The ``owner`` public key.
        active_key (str) The ``active`` public key.
        json: The json representation of the object.
    """
    def __init__(self, account, json=False, is_verbose=True):
        interface.Account.__init__(self, interface.account_arg(account))
        Command.__init__(
            self, 
            [self.name, "--json"] if json else [self.name], 
            "get", "account", is_verbose)

        self.owner_key = None
        self.active_key = None
        try:
            if json:
                permissions = self.json["permissions"]
                for permission in permissions:
                    if permission["required_auth"]["keys"]:
                        key = permission["required_auth"]["keys"][0]["key"]
                        if permission["perm_name"] == "owner":
                            self.owner_key = key
                        if permission["perm_name"] == "active":
                            self.active_key = key                   
            else:
                owner = re.search(r'owner\s+1\:\s+1\s(.*)\n', self.out_msg)
                active = re.search(r'active\s+1\:\s+1\s(.*)\n', self.out_msg)
                if owner and active:
                    self.owner_key = owner.group(1)
                    self.active_key = active.group(1)
        except:
            pass

        self.printself()

    def __str__(self):
        return "name: {}\n".format(self.name) + str(Command.__str__(self))


class GetTransaction(Command):
    """Retrieve a transaction from the blockchain.

    Args:
        transaction_id (str): ID of the transaction to retrieve.
        block_hint (int): If set, the block number this transaction may be in.
        is_verbose (bool): If ``False`` do not print. Default is ``True``.

    Attributes:
        transaction_id: The ID of the transaction retrieved.
        json: The transaction retrieved.
    """
    def __init__(self, transaction_id, block_hint=None, is_verbose=True):
        
        self.transaction_id = transaction_id
        args = [transaction_id]
        if block_hint:
            args.extend(["--block-hint", str(block_hint)])
        Command.__init__(
            self, args, "get", "transaction", is_verbose)

        self.printself()


class WalletCreate(interface.Wallet, Command):
    """Create a new wallet locally.

    If the ``password`` argument is set, try to open a wallet. Otherwise, create
    a new wallet.

    Args:
        name (str): The name of the wallet, defaults to ``default``.
        password (str): The password to the wallet, if the wallet exists. 
        is_verbose (bool): If ``False`` do not print. Default is ``True``.

    Attributes:
        name (str): The name of the wallet.
        password (str): The password returned by the ``wallet create`` 
            EOSIO cleos command.
        is_created (bool): True, if the wallet created.
    """
    def __init__(self, name="default", password="", is_verbose=True):
        interface.Wallet.__init__(self, name)
        self.password = None
        
        if not password: # try to create a wallet
            Command.__init__(
                self, ["--name", self.name, "--to-console"], 
                "wallet", "create", is_verbose)
            self.json["name"] = name
            msg = self.out_msg

            self.password = msg[msg.find("\"")+1:msg.rfind("\"")]
            self.json["password"] = self.password
            self.is_created = True

        else: # try to open an existing wallet
            WalletOpen(name, is_verbose=False)
            wallet_unlock = WalletUnlock(name, password, is_verbose=False)
            self.json = {} 
            self.name = name
            self.password = password
            self.is_created = False
            self.json["name"] = name
            self.json["password"] = password
            self.out_msg = "Restored wallet: {}".format(self.name)

        self.printself(is_verbose)


class WalletStop(Command):
    """Stop keosd, the EOSIO wallet manager.

    Args:
        is_verbose (bool): If ``False`` do not print. Default is ``True``.    
    """
    def __init__(self, is_verbose=True):
        Command.__init__(self, [], "wallet", "stop", is_verbose)

        self.printself()


class WalletList(Command):
    """List opened wallets, * marks unlocked.

    Args:
        is_verbose (bool): If ``False`` do not print. Default is ``True``.    
            
    Attributes:
        json: The list of the open wallets.
    """
    def __init__(self, is_verbose=True):
        Command.__init__(
            self, [], "wallet", "list", is_verbose)

        self.json = json_module.loads("{" + self.out_msg.replace("Wallets", \
            '"Wallets"', 1) + "}")
        self.printself()


class WalletImport(Command):
    """Import a private key into wallet.

    Args:
        wallet (str or .interface.Wallet): A wallet to import key into.
        key (str or .interface.Key): A key to import.
        is_verbose (bool): If ``False`` do not print. Default is ``True``.

    Attributes:
        key_private (str) The key imported.
    """
    def __init__(self, key, wallet="default", is_verbose=True):
        key_private = interface.key_arg(
            key, is_owner_key=True, is_private_key=True)
        Command.__init__(
            self, 
            ["--private-key", key_private, "--name", 
                interface.wallet_arg(wallet)],
            "wallet", "import", is_verbose)

        self.json["key_private"] = key_private
        self.key_private = key_private
        self.printself()

class WalletRemove_key(Command):
    """Remove key from wallet

    Args:
        wallet (str or .interface.Wallet): The wallet to remove key from.
        password (str): The password returned by wallet create.
        key (str or .interface.Key): A public key to remove.
        is_verbose (bool): If ``False`` do not print. Default is ``True``.

    Attributes:
        key_public (str): The public key removed.
    """
    def __init__(self, key, wallet, password, is_verbose=True):
        key_public = interface.key_arg(
            key, is_owner_key=True, is_private_key=False)

        Command.__init__(
            self, 
            [key_public, "--name", interface.wallet_arg(wallet), 
                "--password", password], 
            "wallet", "remove_key", is_verbose)

        self.json["key_public"] = key_public
        self.key_public = key_public
        self.printself()


class WalletKeys(Command):
    """List of public keys from all unlocked wallets.

    Args:
        is_verbose (bool): If ``False`` do not print. Default is ``True``.
    """
    def __init__(self, is_verbose=True):
        Command.__init__(
            self, [], "wallet", "keys", is_verbose)                
        self.printself() 

    def __str__(self):
        out = "Keys in all opened wallets:\n"
        out = out + str(Command.__str__(self))
        return out


class WalletOpen(Command):
    """Open an existing wallet.

    Args:
        wallet (str or .interface.Wallet): The wallet to open.
        is_verbose (bool): If ``False`` do not print. Default is ``True``.
    """
    def __init__(self, wallet="default", is_verbose=True):
        Command.__init__(
            self, ["--name", interface.wallet_arg(wallet)], 
            "wallet", "open", is_verbose)

        self.printself()


class WalletLockAll(Command):
    """Lock all unlocked wallets.

    Args:
        is_verbose (bool): If ``False`` do not print. Default is ``True``.    
    """
    def __init__(self, is_verbose=True):
        Command.__init__(
            self, [], "wallet", "lock_all", is_verbose)

        self.printself()


class WalletLock(Command):
    """Lock wallet.

    Args:
        wallet (str or .interface.Wallet): The wallet to open.
        is_verbose (bool): If ``False`` do not print. Default is ``True``.
    """
    def __init__(self, wallet="default", is_verbose=True):
        Command.__init__(
            self, ["--name", interface.wallet_arg(wallet)], 
            "wallet", "lock", is_verbose)

        self.printself()


class WalletUnlock(Command):
    """Unlock wallet.

    Args:
        wallet (str or .interface.Wallet): The wallet to remove key from.
        password (str): The password returned by wallet create.
        is_verbose (bool): If ``False`` do not print. Default is ``True``.
    """
    def __init__(
            self, wallet="default", password="", timeout=0, is_verbose=True):
 
        if isinstance(wallet, interface.Wallet):
            password = wallet.password

        Command.__init__(
            self, 
            ["--name", interface.wallet_arg(wallet), "--password", password], 
            "wallet", "unlock", is_verbose)

        self.printself()


class CreateKey(interface.Key, Command):
    """Create a new keypair and print the public and private keys.

    Args:
        key_private (str): If set, a private key to set, otherwise random.
        key_public (str): If set, a public key to set, otherwise random.
        r1: Generate a key using the R1 curve (iPhone), instead of the 
            K1 curve (Bitcoin)
        is_verbose (bool): If ``False`` do not print. Default is ``True``.

    Attributes:
        key_private (str): The private key set.
        key_public (str): The public key set.
    """
    def __init__(
                    self, key_public=None, key_private=None, r1=False, 
                    is_verbose=True):
        interface.Key.__init__(self, key_public, key_private)

        if self.key_public or self.key_private:
            self.json = {}
            self.json["publicKey"] = self.key_public           
            self.json["privateKey"] = self.key_private
            self.out_msg = "Private key: {0}\nPublic key: {1}\n" \
                .format(self.key_private, self.key_public)
        else:
            args = ["--to-console"]
            if r1:
                args.append("--r1")

            Command.__init__(self, args, "create", "key", is_verbose)
            
            msg = str(self.out_msg)
            first_collon = msg.find(":")
            first_end = msg.find("\n")
            second_collon = msg.find(":", first_collon + 1)
            self.json["privateKey"] = msg[first_collon + 2 : first_end]
            self.json["publicKey"] = msg[second_collon + 2 : len(msg) - 1]
            self.key_private = self.json["privateKey"]
            self.key_public = self.json["publicKey"]

        self.printself(is_verbose)


class RestoreAccount(GetAccount):

    def __init__(self, account, is_verbose=True):
        GetAccount.__init__(self, account, is_verbose=False, json=True)

        self.name = self.json["account_name"]
        self.owner_key = ""
        self.active_key = ""

    def __str__(self):
        return self.name


class CreateAccount(interface.Account, Command):
    """Create an account, buy ram, stake for bandwidth for the account.

    Args:
        creator (str or .interface.Account): The account creating 
            the new account.
        name: (str) The name of the new account.
        owner_key (str): If set, the owner public key for the new account, 
            otherwise random.
        active_key (str): If set, the active public key for the new account, 
            otherwise random.

    See definitions of the remaining parameters: \
    :func:`.cleos.base.common_parameters`.
    """
    def __init__(
            self, creator, name, owner_key, 
            active_key=None,
            permission=None,
            expiration_sec=None, 
            skip_sign=0, 
            dont_broadcast=0,
            force_unique=0,
            max_cpu_usage=0,
            max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=True
            ):

        if name is None: 
            name = account_name()
        interface.Account.__init__(self, name)

        self.owner_key = None # private keys
        self.active_key = None
        
        if active_key is None:
            active_key = owner_key        

        owner_key_public = interface.key_arg(
            owner_key, is_owner_key=True, is_private_key=False)
        active_key_public = interface.key_arg(
            active_key, is_owner_key=False, is_private_key=False)

        args = [
                interface.account_arg(creator), self.name, 
                owner_key_public, active_key_public
            ]

        args.append("--json")
        if not permission is None:
            p = interface.permission_arg(permission)
            for perm in p:
                args.extend(["--permission", perm])

        if expiration_sec:
            args.extend(["--expiration", str(expiration_sec)])
        if skip_sign:
            args.append("--skip-sign")
        if dont_broadcast:
            args.append("--dont-broadcast")
        if force_unique:
            args.append("--force-unique")
        if max_cpu_usage:
            args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
        if  max_net_usage:
            args.extend(["--max-net-usage", str(max_net_usage)])
        if  not ref_block is None:
            args.extend(["--ref-block", ref_block])
        if delay_sec:
            args.extend(["--delay-sec", delay_sec])

        Command.__init__(
            self, args, "create", "account", is_verbose)

        self.printself(is_verbose)
        
    def __repr__(self):
        return self.name
            
    def __str__(self):
        if self.json:
            import eosfactory.core.str.actions
            return str(eosfactory.core.str.actions.Actions(self.json))

        return self.out_msg


def account_name():
    """Get a random EOSIO account name.
    """
    letters = "abcdefghijklmnopqrstuvwxyz12345"
    name = ""
    for i in range(0, 12):
        name += letters[random.randint(0, 30)]

    return name


class PushAction(Command):
    """Push a transaction with a single action.

    Args:
        account (str or .interface.Account): The account to publish a contract 
            for.
        action (str or json or filename): Definition of the action to execute on 
            the contract.
        data (str): The arguments to the contract.

    See definitions of the remaining parameters: \
    :func:`.cleos.base.common_parameters`.

    Attributes:
        account_name (str): The EOSIO name of the contract's account.
        console (str): Sum of all *["processed"]["action_traces"][]["console"]* \
            components of EOSIO cleos responce.
        act (str): Summary of all actions, like \
            ``eosio.null::nonce <= 5d0a572c49880500``.
    """
    def __init__(
            self, account, action, data,
            permission=None, expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=True,
            json=False
        ):
        self.account_name = interface.account_arg(account)

        args = [self.account_name, action, data]
        if json:
            args.append("--json")
        if not permission is None:
            p = interface.permission_arg(permission)
            for perm in p:
                args.extend(["--permission", perm])

        if expiration_sec:
            args.extend(["--expiration", str(expiration_sec)])
        if skip_sign:
            args.append("--skip-sign")
        if dont_broadcast:
            args.append("--dont-broadcast")
        if force_unique:
            args.append("--force-unique")
        if max_cpu_usage:
            args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
        if  max_net_usage:
            args.extend(["--max-net-usage", str(max_net_usage)])
        if  not ref_block is None:
            args.extend(["--ref-block", ref_block])
        if delay_sec:
            args.extend(["--delay-sec", str(delay_sec)])

        Command.__init__(self, args, "push", "action", is_verbose)

        self.console = ""
        self.act = ""
        if not dont_broadcast and self.json:
            for act in self.json["processed"]["action_traces"]:
                self.console += common.gather_console_output(act)

            for trace in self.json["processed"]["action_traces"]:
                if trace["act"]["data"]:
                    if self.act:
                        self.act += "\n"
                    self.act += "{} <= {}::{} {}".format( 
                                                        trace["act"]["account"], 
                                                        trace["act"]["account"],
                                                        trace["act"]["name"],
                                                        trace["act"]["data"])
        self.printself()

    def __str__(self):
            import eosfactory.core.str.push
            return str(eosfactory.core.str.push.Push(self.json))


