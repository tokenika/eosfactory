'''
.. module:: eosfactory.core.cleos
    :platform: Unix, Darwin
    :synopsis: eosio cleos commands assorted.

.. moduleauthor:: Tokenika
'''

import subprocess
import json
import pathlib
import random
import os
import re

import eosfactory.core.errors as errors
import eosfactory.core.logger as logger
import eosfactory.core.config as config
import eosfactory.core.setup as setup
import eosfactory.core.interface as interface


def set_local_nodeos_address_if_none():
    if not setup.nodeos_address():
        setup.set_nodeos_address(
            "http://" + config.http_server_address())
        setup.is_local_address = True

    return setup.is_local_address


# http://www.sphinx-doc.org/domains.html#info-field-lists
class Cleos():
    '''A prototype for ``eosio cleos`` commands.
    Calls ``eosio cleos``, and processes the responce.

    :param list args: List of ``eosio cleos`` positionals and options.
    :param str command_group: Command group name.
    :param str command: Command name.

    :var str out_msg: Responce received via the stdout stream.
    :var str out_msg_details: Responce received via the stderr stream.
    :var str err_msg: Error message received via the stderr stream.
    :var dict json: Responce received as JSON, if any.
    :var bool is_verbose: If set, a message is printed.
    :var list args: Value of the ``args`` argument.

    :raises .core.errors.Error: If err_msg.
    '''    
    def __init__(self, args, command_group, command, is_verbose=True):
        self.out_msg = None
        self.out_msg_details = None
        self.err_msg = None
        self.json = {}
        self.is_verbose = is_verbose
        self.args = args

        cl = [config.cli_exe()]
        set_local_nodeos_address_if_none()
        cl.extend(["--url", setup.nodeos_address()])

        if setup.is_print_request:
            cl.append("--print-request")
        if setup.is_print_response:
            cl.append("--print-response")

        cl.append(command_group)
        cl.extend(re.sub(re.compile(r'\s+'), ' ', command.strip()).split(" "))
        cl.extend(args)

        if setup.is_print_command_line:
            print("command line sent to cleos:")
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

            if not self.err_msg or self.err_msg and \
                    not "Transaction took too long" in self.err_msg:
                break

        errors.validate(self)
            
        try:
            self.json = json.loads(self.out_msg)
        except:
            pass

        try:
            self.json = json.loads(self.out_msg_details)
        except:
            pass        

    def printself(self, is_verbose=False):
        '''Print message.

        :keyword bool is_verbose: If set, a message is printed.
        '''
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


class GetAccount(interface.Account, Cleos):
    '''Retrieve an account from the blockchain.

    - **parameters**::

        account: The account object or the name of the account to retrieve.
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        name: The name of the account.
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(self, account, is_info=True, is_verbose=True):
        interface.Account.__init__(self, interface.account_arg(account))
        Cleos.__init__(
            self, 
            [self.name] if is_info else [self.name, "--json"], 
            "get", "account", is_verbose)

        self.owner_key = None
        self.active_key = None
        try:
            if not is_info:
                permissions = self.json["permissions"]
                for permission in permissions:
                    if permission["required_auth"]["keys"]:
                        key = permission["required_auth"]["keys"][0]["key"]
                        if permission["perm_name"] == "owner":
                            self.owner_key = key
                        if permission["perm_name"] == "active":
                            self.active_key = key                   
            else:
                owner = re.search('owner\s+1\:\s+1\s(.*)\n', self.out_msg)
                active = re.search('active\s+1\:\s+1\s(.*)\n', self.out_msg)
                if owner and active:
                    self.owner_key = owner.group(1)
                    self.active_key = active.group(1)
        except:
            pass

        self.printself()

    def __str__(self):
        out = "name: {}\n".format(self.name)
        out = out + str(Cleos.__str__(self))
        return out

class GetAccounts(Cleos):
    '''Retrieve accounts associated with a public key.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(self, key, is_verbose=True):
        public_key = interface.key_arg(key, is_owner_key=True, is_private_key=False)
        Cleos.__init__(
            self, [public_key], "get", "accounts", is_verbose)

        self.names = self.json['account_names']
        self.printself()


class GetTransaction(Cleos):
    '''Retrieve a transaction from the blockchain.

    - **parameters**::

        transaction_id: ID of the transaction to retrieve.
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        transaction_id: ID of the transaction retrieved.
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(self, transaction_id, is_verbose=True):
        
        self.transaction_id = transaction_id
        Cleos.__init__(
            self, [transaction_id], "get", "transaction", is_verbose)

        self.printself()


class WalletCreate(interface.Wallet, Cleos):
    '''Create a new wallet locally.

    - **parameters**::

        name: The name of the new wallet, defaults to ``default``.
        password: The password to the wallet, if the wallet exists. Default is None.
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        name: The name of the wallet.
        password: The password returned by wallet create.
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(self, name="default", password="", is_verbose=True):
        interface.Wallet.__init__(self, name)
        self.password = None
        
        if not password: # try to create a wallet
            Cleos.__init__(
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


class WalletStop(Cleos):
    '''Stop keosd (doesn't work with nodeos).
    '''
    def __init__(self, is_verbose=True):
        Cleos.__init__(self, [], "wallet", "stop", is_verbose)

        self.printself()


class WalletList(Cleos):
    '''List opened wallets, * marks unlocked.

    - **parameters**::

        is_verbose: If ``False`` do not print. Default is ``True``.
            
    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(self, is_verbose=True):
        Cleos.__init__(
            self, [], "wallet", "list", is_verbose)

        self.json = json.loads("{" + self.out_msg.replace("Wallets", \
            '"Wallets"', 1) + "}")
        self.printself()


class WalletImport(Cleos):
    '''Import a private key into wallet.

    - **parameters**::

        wallet: A wallet object or the name of the wallet to import key into.
        key: A key object or a private key in WIF format to import.
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(self, key, wallet="default", is_verbose=True):
        key_private = interface.key_arg(
            key, is_owner_key=True, is_private_key=True)
        Cleos.__init__(
            self, 
            ["--private-key", key_private, "--name", 
                interface.wallet_arg(wallet)],
            "wallet", "import", is_verbose)

        self.json["key_private"] = key_private
        self.key_private = key_private
        self.printself()

class WalletRemove_key(Cleos):
    '''Remove key from wallet
    - **parameters**::

        wallet: A wallet object or the name of the wallet to import key into.
        password: The password returned by wallet create.
        key: A key object or a private key in WIF format to import.
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        error: Whether any error ocurred.
        is_verbose: If set, print output.
    '''
    def __init__(self, key, wallet, password, is_verbose=True):
        key_public = interface.key_arg(
            key, is_owner_key=True, is_private_key=False)

        Cleos.__init__(
            self, 
            [key_public, "--name", interface.wallet_arg(wallet), 
                "--password", password], 
            "wallet", "remove_key", is_verbose)

        self.json["key_public"] = key_public
        self.key_public = key_public
        self.printself()


class WalletKeys(Cleos):
    '''List of public keys from all unlocked wallets.

    - **parameters**::

        is_verbose: If ``False`` do not print. Default is ``True``.

    - **parameters**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(self, is_verbose=True):
        Cleos.__init__(
            self, [], "wallet", "keys", is_verbose)                
        self.printself() 

    def __str__(self):
        out = "Keys in all opened wallets:\n"
        out = out + str(Cleos.__str__(self))
        return out


class WalletOpen(Cleos):
    '''Open an existing wallet.

    - **parameters**::

        wallet: The name of the wallet to import key into. May be an object 
            having the  May be an object having the attribute `name`, 
            or a string. 
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(self, wallet="default", is_verbose=True):
        Cleos.__init__(
            self, ["--name", interface.wallet_arg(wallet)], 
            "wallet", "open", is_verbose)

        self.printself()


class WalletLockAll(Cleos):
    '''Lock all unlocked wallets.
    '''
    def __init__(self, is_verbose=True):
        Cleos.__init__(
            self, [], "wallet", "lock_all", is_verbose)

        self.printself()


class WalletLock(Cleos):
    '''Lock wallet.

    - **parameters**::

        wallet: The name of the wallet to import key into. May be an object 
            having the  May be an object having the attribute `name`, 
            or a string. 
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **parameters**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(self, wallet="default", is_verbose=True):
        Cleos.__init__(
            self, ["--name", interface.wallet_arg(wallet)], 
            "wallet", "lock", is_verbose)

        self.printself()


class WalletUnlock(Cleos):
    '''Unlock wallet.

    - **parameters**::

        wallet: The name of the wallet. May be an object 
            having the  May be an object having the attribute `name`,
            or a string.
        password: If the wallet argument is not a wallet object, the password 
            returned by wallet create, else anything, defaults to "".
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::
    
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(
            self, wallet="default", password="", timeout=0, is_verbose=True):
 
        if isinstance(wallet, interface.Wallet):
            password = wallet.password

        Cleos.__init__(
            self, 
            ["--name", interface.wallet_arg(wallet), "--password", password], 
            "wallet", "unlock", is_verbose)

        self.printself()


class GetCode(Cleos):
    '''Retrieve the code and ABI for an account.

    - **parameters**::

        account: The name of an account whose code should be retrieved. 
            May be an object having the  May be an object having the attribute 
            `name`, or a string.
        code: The name of the file to save the contract .wast/wasm to.
        abi: The name of the file to save the contract .abi to.
        wasm: Save contract as wasm.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.    
    '''
    def __init__(
            self, account, code="", abi="", 
            wasm=False, is_verbose=True):

        account_name = interface.account_arg(account)

        args = [account_name]
        if code:
            args.extend(["--code", code])
        if abi:
            args.extend(["--abi", abi])
        if wasm:
            args.extend(["--wasm"])

        Cleos.__init__(self, args, "get", "code", is_verbose)

        msg = str(self.out_msg)
        self.json["code_hash"] = msg[msg.find(":") + 2 : len(msg) - 1]
        self.code_hash = self.json["code_hash"]
        self.printself()


class GetTable(Cleos):
    '''Retrieve the contents of a database table

    - **parameters**::

        account: The name of the account that owns the table. May be 
            an object having the attribute `name`, or a string.
        scope: The scope within the account in which the table is found. May be
            an object having the attribute `name`, or a string.
        table: The name of the table as specified by the contract abi.
        binary: Return the value as BINARY rather than using abi to 
            interpret as JSON
        limit: The maximum number of rows to return.
        key: The name of the key to index by as defined by the abi, 
            defaults to primary key.
        lower: JSON representation of lower bound value of key, 
            defaults to first.
        upper: JSON representation of upper bound value value of key, 
            defaults to last.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(
            self, account, table, scope,
            binary=False, 
            limit=10, key="", lower="", upper="",
            is_verbose=True
            ):
        args = [interface.account_arg(account)]

        if not scope:
            scope=self.name
        else:
            try:
                scope_name = scope.name
            except:
                scope_name = scope

        args.append(scope_name)
        args.append(table)

        if binary:
            args.append("--binary")
        if limit:
            args.extend(["--limit", str(limit)])
        if key:
            args.extend(
                ["--key", 
                    interface.key_arg(key, is_owner_key=False, 
                    is_private_key=False)])
        if lower:
            args.extend(["--lower", lower])
        if upper:
            args.extend(["--upper", upper])

        Cleos.__init__(self, args, "get", "table", is_verbose)

        self.printself()


class CreateKey(interface.Key, Cleos):
    '''Create a new keypair and print the public and private keys.

    - **parameters**::

        r1: Generate a key using the R1 curve (iPhone), instead of the 
            K1 curve (Bitcoin)

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.    
    '''
    def __init__(
            self, key_public="", key_private="", r1=False, 
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

            Cleos.__init__(
                self, args, "create", "key", is_verbose)
            
            msg = str(self.out_msg)
            first_collon = msg.find(":")
            first_end = msg.find("\n")
            second_collon = msg.find(":", first_collon + 1)
            self.json["privateKey"] = msg[first_collon + 2 : first_end]
            self.json["publicKey"] = msg[second_collon + 2 : len(msg) - 1]
            self.printself()
            self.key_private = self.json["privateKey"]
            self.key_public = self.json["publicKey"]


class RestoreAccount(GetAccount):

    def __init__(self, account, is_verbose=True):
        GetAccount.__init__(self, account, is_verbose=False, is_info=False)

        self.name = self.json["account_name"]
        self.owner_key = ""
        self.active_key = ""
        
    def info(self):
        print(str(GetAccount(self.name, is_verbose=False)))

    def __str__(self):
        return self.name


class CreateAccount(interface.Account, Cleos):
    '''Create an account, buy ram, stake for bandwidth for the account.

    - **parameters**::

        creator: The name, of the account creating the new account. May be an 
            object having the attribute `name`, or a string.
        name: The name of the new account.
        owner_key: The owner public key for the new account.
        active_key: The active public key for the new account.

        permission: An account and permission level to authorize, as in 
            'account@permission'. May be an object having the attribute `name`, 
            or a string.
        expiration: The time in seconds before a transaction expires, 
            defaults to 30s
        skip_sign: Specify if unlocked wallet keys should be used to sign 
            transaction.
        dont_broadcast: Don't broadcast transaction to the network (just print).
        force_unique: Force the transaction to be unique. this will consume extra 
            bandwidth and remove any protections against accidentally issuing the 
            same transaction multiple times.
        max_cpu_usage: Upper limit on the milliseconds of cpu usage budget, for 
            the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: Upper limit on the net usage budget, in bytes, for the 
            transaction (defaults to 0 which means no limit).
        ref_block: The reference block num or block id used for TAPOS 
            (Transaction as Proof-of-Stake).
        delay_sec: The delay in seconds, defaults to 0s.

    - **attributes**::

        owner_key: Owner private key.
        active_key: Active private key.
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.    
    '''
    def __init__(
            self, creator, name, owner_key, 
            active_key=None,
            permission=None,
            expiration_sec=None, 
            skip_signature=0, 
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
        if skip_signature:
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

        Cleos.__init__(
            self, args, "create", "account", is_verbose)
            
        self.json = GetAccount(self.name, is_verbose=False, is_info=False).json
        self.printself()

    def info(self):
        print(str(GetAccount(self.name, is_verbose=False)))

    def get_transaction(self):
        return GetTransaction(self.transaction)
            
    def __str__(self):
        return self.name


def account_name():
    letters = "abcdefghijklmnopqrstuvwxyz12345"
    name = ""
    for i in range(0, 12):
        name += letters[random.randint(0, 30)]

    return name

def contract_is_built(contract_dir, wasm_file=None, abi_file=None):
    contract_path_absolute = config.contract_dir(contract_dir)
    if not contract_path_absolute:
        return []

    if not wasm_file:
        try :
            wasm_file = config.wasm_file(contract_dir)
        except:
            pass
        if not wasm_file:
            return []
    else:
        if not os.path.isfile(
                os.path.join(contract_path_absolute, wasm_file)):
            return []

    if not abi_file:
        abi_file = config.abi_file(contract_dir)
        if not abi_file:
            return []
    else:
        if not os.path.isfile(
                os.path.join(contract_path_absolute, abi_file)):
            return []

    return [contract_path_absolute, wasm_file, abi_file]


class PushAction(Cleos):
    '''Push a transaction with a single action.

    - **parameters**::

        account: The account to publish a contract for.  May be an object 
            having the  May be an object having the attribute `name`, 
            or a string.
        action: A JSON string or filename defining the action to execute on 
            the contract.
        data: The arguments to the contract.
        permission: An account and permission level to authorize, as in 
            'account@permission'. May be an object having the attribute `name`, 
            or a string.
        expiration: The time in seconds before a transaction expires, 
            defaults to 30s
        skip_sign: Specify if unlocked wallet keys should be used to sign 
            transaction.
        dont_broadcast: Don't broadcast transaction to the network (just print).
        force_unique: Force the transaction to be unique. this will consume extra 
            bandwidth and remove any protections against accidentally issuing the 
            same transaction multiple times.
        max_cpu_usage: Upper limit on the milliseconds of cpu usage budget, for 
            the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: Upper limit on the net usage budget, in bytes, for the 
            transaction (defaults to 0 which means no limit).
        ref_block: The reference block num or block id used for TAPOS 
            (Transaction as Proof-of-Stake).

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(
            self, account, action, data,
            permission=None, expiration_sec=None, 
            skip_signature=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
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
        if skip_signature:
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
                        
        self.console = None
        self.data = None
        Cleos.__init__(self, args, "push", "action", is_verbose)

        if not dont_broadcast:
            self.console = self.json["processed"]["action_traces"][0]["console"]
            self.data = self.json["processed"]["action_traces"][0]["act"]["data"]

        self.printself()


    def get_transaction(self):
        return GetTransaction(self.transaction)
