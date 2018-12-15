import re
import types

import eosfactory.core.logger as logger
import eosfactory.core.manager as manager
import eosfactory.core.interface as interface
import eosfactory.core.cleos as cleos


def set_contract_(
            account, contract_dir, 
            wasm_file=None, abi_file=None, 
            permission=None, expiration_sec=None, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=True,
            json=False
    ):
    '''Create or update the contract on an account.

    - **parameters**:: 

        account: The account to publish a contract for. May be an object having 
            the attribute `name`, or a string.
        contract_dir: The path containing to a directory. 
        wasm_file: The WASM file relative to the contract_dir.
        abi_file: The ABI file for the contract relative to the contract-dir.
        permission: An account and permission level to authorize, as in 
            'account@permission'. May be an object having the attribute `name`, 
            or a string.
        expiration: The time in seconds before a transaction expires, 
            defaults to 30s
        skip_sign: Specify if unlocked wallet keys should be used to sign 
            transaction.
        dont_broadcast: Don't broadcast transaction to the network (just print).
        forceUnique: Force the transaction to be unique. this will consume extra 
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
    files = cleos.contract_is_built(contract_dir, wasm_file, abi_file)
    if not files:
        raise errors.Error("""
        Cannot determine the contract directory. The clue is 
        {}.
        """.format(contract_dir))
        return

    contract_path_absolute = files[0]
    wasm_file = files[1]
    abi_file = files[2]            

    account_name = interface.account_arg(account)

    args = [account_name, contract_path_absolute]

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
    if forceUnique:
        args.append("--force-unique")
    if max_cpu_usage:
        args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
    if  max_net_usage:
        args.extend(["--max-net-usage", str(max_net_usage)])
    if  not ref_block is None:
        args.extend(["--ref-block", ref_block]) 
    if delay_sec:
        args.extend(["--delay-sec", str(delay_sec)])
    if wasm_file:
        args.append(wasm_file)
    if abi_file:
        args.append(abi_file)

    result = cleos._Cleos(args, "set", "contract", is_verbose)
    result.contract_path_absolute = files[0]
    result.account_name = interface.account_arg(account)

    def get_transaction(self):
        return GetTransaction(self.transaction)

    result.get_transaction = types.MethodType(get_transaction, result)
    result.printself()

    return result


def set_contract(
            self, contract_dir, 
            wasm_file="", abi_file="", 
            permission=None, expiration_sec=None, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0
    ):
    '''Create or update the contract on an account.

    This is a specification of the function 
    :func:`.set_contract`, used as a 
    method of objects created with the ``create_action`` factory function. 
    The owning account object is represented as the ``self`` parameter.
    '''

    result = set_contract_(
                self, contract_dir, 
                wasm_file, abi_file, 
                permission, expiration_sec, 
                skip_signature, dont_broadcast, forceUnique,
                max_cpu_usage, max_net_usage,
                ref_block,
                delay_sec,
                is_verbose=False, json=True
            )

    logger.OUT(result)
    self.set_contract = result


def set_account_permission_(
            account, permission_name, authority, parent_permission_name,
            permission=None,
            expiration_sec=None, 
            skip_signature=0, dont_broadcast=0, return_packed=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=True, json=False
    ):
    '''Set parameters dealing with account permissions.

    - **parameters**::

        account: The account to set/delete a permission authority for. May be 
            an object having the attribute `name`, or a string.
        permission_name: The permission to set/delete an authority for. May be
            a string or an instance of ``eosfactory.core.interface.Permission``.
        parent_permission_name: The permission name of this parents permission 
            (defaults to: "Active"). May be a string or an instance of 
            ``eosfactory.core.interface.Permission``.
        authority:  None to delete. May be a public key string, or an 
            interface.key_arg object, or JSON string, or Python ``dict`` object,
            or a filename defining the authority.
        permission: An account and permission level to authorize, as in 
            'account@permission'. May be an object having the attribute `name`, 
            or a string.
        expiration: The time in seconds before a transaction expires, 
            defaults to 30s
        skip_sign: Specify if unlocked wallet keys should be used to sign 
            transaction.
        dont_broadcast: Don't broadcast transaction to the network (just print).
        return_packed: Used in conjunction with dont_broadcast to get the 
            packed transaction.
        forceUnique: Force the transaction to be unique. this will consume extra 
            bandwidth and remove any protections against accidentally issuing 
            the same transaction multiple times.
        max_cpu_usage: Upper limit on the milliseconds of cpu usage budget, for 
            the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: Upper limit on the net usage budget, in bytes, for the 
            transaction (defaults to 0 which means no limit).
        ref_block: The reference block num or block id used for TAPOS 
            (Transaction as Proof-of-Stake).
        delay_sec: Set the delay_sec seconds, defaults to 0s            
    '''
    account_name = interface.account_arg(account)
    args = [account_name]

    if isinstance(permission_name, interface.Permission):
        permission_name = permission_name.value
    args.append(permission_name)

    if authority:
        authority = manager.data_json(authority)
        if isinstance(authority, interface.Account):
            args.append(authority.active())
        else:
            authority =  re.sub(re.compile(r'\s+'), '', authority)
            args.append(authority)
    else:
        args.append("NULL")

    if isinstance(parent_permission_name, interface.Permission):
        parent_permission_name = parent_permission_name.value
    args.append(parent_permission_name)        

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
    if forceUnique:
        args.append("--force-unique")
    if max_cpu_usage:
        args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
    if  max_net_usage:
        args.extend(["--max-net-usage", str(max_net_usage)])
    if  not ref_block is None:
        args.extend(["--ref-block", ref_block])
    if delay_sec:
        args.extend(["--delay-sec", str(delay_sec)])
                    
    result = cleos._Cleos(args, "set", "account permission", is_verbose)
    result.account_name = account_name
    result.console = None
    result.data = None

    if json and not dont_broadcast:
        result.console = result.json["processed"]["action_traces"][0]["console"]
        result.data = result.json["processed"]["action_traces"][0]["act"]["data"]

    result.printself()    
    return result


def set_account_permission(
            self, permission_name, authority, parent_permission_name,
            permission=None,
            expiration_sec=None, 
            skip_signature=0, dont_broadcast=0, return_packed=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0
    ):
    '''Set parameters dealing with account permissions.

    This is a specification of the function 
    :func:`.set_account_permission_`, used as a 
    method of objects created with the ``create_action`` factory function. 
    The owning account object is represented as the ``self`` parameter.
    '''
    logger.TRACE('''
        * Set action permission.
        ''')
    return set_account_permission_(
            self, permission_name, authority, parent_permission_name,
            permission,
            expiration_sec, 
            skip_signature, dont_broadcast, return_packed, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            delay_sec,
            is_verbose=False, json=True
    )


def set_action_permission_(
            account, code, type, requirement,
            permission=None,
            expiration_sec=None, 
            skip_signature=0, dont_broadcast=0, return_packed=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=True,
            json=False
    ):
    '''Set parameters dealing with account permissions.

    - **parameters**::

        account: The account to set/delete a permission authority for. May be 
            an object having the attribute `name`, or a string.
        code: The account that owns the code for the action. May be 
            an object having the attribute `name`, or a string.
        type: The type of the action, string.
        requirement: The permission name require for executing the given 
            action, string.
        permission: An account and permission level to authorize, as in 
            'account@permission'. May be an object having the attribute `name`, 
            or a string.
        expiration: The time in seconds before a transaction expires, 
            defaults to 30s
        skip_sign: Specify if unlocked wallet keys should be used to sign 
            transaction.
        dont_broadcast: Don't broadcast transaction to the network (just print).
        return_packed: Used in conjunction with dont_broadcast to get the 
            packed transaction.
        forceUnique: Force the transaction to be unique. this will consume extra 
            bandwidth and remove any protections against accidentally issuing 
            the same transaction multiple times.
        max_cpu_usage: Upper limit on the milliseconds of cpu usage budget, for 
            the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: Upper limit on the net usage budget, in bytes, for the 
            transaction (defaults to 0 which means no limit).
        ref_block: The reference block num or block id used for TAPOS 
            (Transaction as Proof-of-Stake).
        delay_sec: Set the delay_sec seconds, defaults to 0s
    '''
    account_name = interface.account_arg(account)
    args = [account_name]

    code_name = interface.account_arg(code)
    args.append(code_name)

    args.append(type)

    if requirement:
        requirement_name = interface.account_arg(requirement)
        args.append(requirement_name)
    else:
        args.append("NULL")

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
    if forceUnique:
        args.append("--force-unique")
    if max_cpu_usage:
        args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
    if  max_net_usage:
        args.extend(["--max-net-usage", str(max_net_usage)])
    if  not ref_block is None:
        args.extend(["--ref-block", ref_block])
    if delay_sec:
        args.extend(["--delay-sec", str(delay_sec)])

    result = cleos._Cleos(args, "set", "action permission", is_verbose)
    result.console = None
    result.data = None

    if json and not dont_broadcast:
        result.console = result.json["processed"]["action_traces"][0]["console"]
        result.data = result.json["processed"]["action_traces"][0]["act"]["data"]

    result.printself()


def set_action_permission(
            self, code, type, requirement,
            permission=None,
            expiration_sec=None, 
            skip_signature=0, dont_broadcast=0, return_packed=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0
    ):
    '''Set parameters dealing with account permissions.

    This is a specification of the function 
    :func:`.set_action_permission_`, used as a method of objects created with 
    the ``create_action`` factory function. 
    The owning account object is represented as the ``self`` parameter.
    '''
    logger.TRACE('''
    * Set action permission.
    ''')

    return set_action_permission_(
            self, code, type, requirement,
            permission,
            expiration_sec, 
            skip_signature, dont_broadcast, return_packed, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            delay_sec,
            is_verbose=False,
            json=True
    )
    