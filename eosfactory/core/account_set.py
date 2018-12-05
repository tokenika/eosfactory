import eosfactory.core.logger as logger

import eosfactory.core.manager as manager
import eosfactory.core.cleos_set as cleos_set


def set_action_permission(
    account_object, code, type, requirement,
            permission=None,
            expiration_sec=None, 
            skip_signature=0, 
            dont_broadcast=0,
            return_packed=0,
            forceUnique=0,
            max_cpu_usage=0,
            max_net_usage=0,
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
            bandwidth and remove any protections against accidently issuing the 
            same transaction multiple times.
        max_cpu_usage: Upper limit on the milliseconds of cpu usage budget, for 
            the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: Upper limit on the net usage budget, in bytes, for the 
            transaction (defaults to 0 which means no limit).
        ref_block: The reference block num or block id used for TAPOS 
            (Transaction as Proof-of-Stake).
        delay_sec: Set the delay_sec seconds, defaults to 0s
    '''

    logger.TRACE('''
    * Set action permission.
    ''')

    result = cleos_set.SetActionPermission(
        account_object, code, type, requirement,
        permission,
        expiration_sec, 
        skip_signature, 
        dont_broadcast,
        return_packed,
        forceUnique,
        max_cpu_usage,
        max_net_usage,
        ref_block,
        delay_sec,
        is_verbose=False, json=True)


def set_account_permission(
    account_object, permission_name, authority, parent_permission_name, 
        permission=None,
        expiration_sec=None, 
        skip_signature=0, 
        dont_broadcast=0,
        return_packed=0,
        forceUnique=0,
        max_cpu_usage=0,
        max_net_usage=0,
        ref_block=None,
        delay_sec=0,
        is_verbose=True,
        json=False
    ):
    '''Set parameters dealing with account permissions.

    - **parameters**::

        permission_name: The permission to set/delete an authority for. May be
            a string or an instance of ``eosfactory.coreinterface.Permission``.
        authority:  None to delete; a public key string or an interface.key_arg
            object; JSON string; a filename defining the authority.
        parent_permission_name: The permission name of this parents permission 
            (defaults to: "Active"). May be a string or an instance of 
            ``eosfactory.core.interface.Permission``.
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
            bandwidth and remove any protections against accidently issuing the 
            same transaction multiple times.
        max_cpu_usage: Upper limit on the milliseconds of cpu usage budget, for 
            the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: Upper limit on the net usage budget, in bytes, for the 
            transaction (defaults to 0 which means no limit).
        ref_block: The reference block num or block id used for TAPOS 
            (Transaction as Proof-of-Stake).
        delay_sec: Set the delay_sec seconds, defaults to 0s

    '''
    logger.TRACE('''
    * Set account premission.
    ''')

    authority = manager.data_json(authority)

    result = cleos_set.SetAccountPermission(
        account_object, permission_name, authority, parent_permission_name,
        permission,
        expiration_sec, 
        skip_signature, 
        dont_broadcast,
        return_packed,
        forceUnique,
        max_cpu_usage,
        max_net_usage,
        ref_block,
        delay_sec,
        is_verbose=False, json=True)
    
