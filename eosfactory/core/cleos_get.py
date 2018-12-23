import types

import eosfactory.core.logger as logger
import eosfactory.core.interface as interface
import eosfactory.core.cleos as cleos


class GetInfo(cleos.Cleos):
    '''Get current blockchain information.

    :param bool is_verbose: If ``False``, print a message. Default is ``True``.

    :return: A :class:`eosfactory.core.cleos.Cleos` object, extended with the 
        following items:

    :var str head_block_time: The time of the most recent block.
    :var int head_block: The most recent block number.
    :var int last_irreversible_block_num: The number of the most recent irreversible
        block.
    '''
    def __init__(self, is_verbose=True):
        cleos.Cleos.__init__(self, [], "get", "info", is_verbose)
        self.head_block = int(self.json["head_block_num"])
        self.head_block_time = self.json["head_block_time"]
        self.last_irreversible_block_num \
                            = int(self.json["last_irreversible_block_num"])
        self.printself()

    def __str__(self):
        return json.dumps(self.json, sort_keys=True, indent=4)


class GetBlock(cleos.Cleos):
    '''Retrieve a full block from the blockchain.

    :param int block_number: The number of the block to retrieve.
    :param str block_id: The ID of the block to retrieve, if set, defaults to "".   
    :param bool is_verbose: If ``False``, print a message. Default is ``True``.
        
    :return: A :class:`eosfactory.core.cleos.Cleos` object.
    '''
    def __init__(self, block_number, block_id=None, is_verbose=True):
        cleos.Cleos.__init__(
                        self, [block_id] if block_id else [str(block_number)], 
                        "get", "block", is_verbose)
        self.printself()

    def __str__(self):
        return json.dumps(self.json, sort_keys=True, indent=4)


def get_block_trx_data(block_num):
    block = GetBlock(block_num, is_verbose=False)
    trxs = block.json["transactions"]
    if not len(trxs):
        logger.OUT("No transactions in block {}.".format(block_num))
    else:
        for trx in trxs:
            logger.OUT(trx["trx"]["transaction"]["actions"][0]["data"])


def get_block_trx_count(block_num):
    block = GetBlock(block_num, is_verbose=False)
    trxs = block.json["transactions"]
    if not len(trxs):
        logger.OUT("No transactions in block {}.".format(block_num))    
    return len(trxs)


class GetAccounts(cleos.Cleos):
    '''Retrieve accounts associated with a public key.

    Args:
        key (str or .interface.Key): The public key to retrieve accounts for.
        is_verbose (bool): If *False* do not print. Default is *True*.

    Attributes:
        names (list): The retrieved list of accounts.
    '''
    def __init__(self, key, is_verbose=True):
        public_key = interface.key_arg(key, is_owner_key=True, is_private_key=False)
        cleos.Cleos.__init__(
            self, [public_key], "get", "accounts", is_verbose)

        self.names = self.json['account_names']
        self.printself()


class GetCode(cleos.Cleos):
    '''Retrieve the code and ABI for an account.

    Args:
        account (str or .interface.Account): The account to retrieve.
        code (str): If set, the name of the file to save the contract 
            .wast/wasm to.
        abi (str): If set, the name of the file to save the contract .abi to.
        wasm (bool): Save contract as wasm.
        is_verbose (bool): If *False* do not print. Default is *True*.

    Attributes:
        code_hash (str): The hash of the code.
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

        cleos.Cleos.__init__(self, args, "get", "code", is_verbose)

        msg = str(self.out_msg)
        self.json["code_hash"] = msg[msg.find(":") + 2 : len(msg) - 1]
        self.code_hash = self.json["code_hash"]
        self.printself()


class GetTable(cleos.Cleos):
    '''Retrieve the contents of a database table

    Args:
        account (str or .interface.Account): The account that owns the table. 
        scope (str or .interface.Account): The scope within the account in 
            which the table is found.
        table (str): The name of the table as specified by the contract abi.
        binary (bool): Return the value as BINARY rather than using abi to 
            interpret as JSON. Default is *False*.
        limit (int): The maximum number of rows to return. Default is 10.
        lower (str): JSON representation of lower bound value of key, 
            defaults to first.
        upper (str): JSON representation of upper bound value value of key, 
            defaults to last.
        is_verbose (bool): If *False* do not print. Default is *True*.
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
        if lower:
            args.extend(["--lower", lower])
        if upper:
            args.extend(["--upper", upper])

        cleos.Cleos.__init__(self, args, "get", "table", is_verbose)

        self.printself()
