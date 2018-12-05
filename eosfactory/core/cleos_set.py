import re

import eosfactory.core.interface as interface
import eosfactory.core.cleos as cleos

class SetAccountPermission(cleos._Cleos):
    '''Set parameters dealing with account permissions.

    - **parameters**::

        account: The account to set/delete a permission authority for. May be 
            an object having the attribute `name`, or a string.
        permission_name: The permission to set/delete an authority for. May be
            a string or an instance of ``eosfactory.core.interface.Permission``.
        parent_permission_name: The permission name of this parents permission 
            (defaults to: "Active"). May be a string or an instance of 
            ``eosfactory.core.interface.Permission``.
        authority:  None to delete; a public key string or an interface.key_arg
            object; JSON string; a filename defining the authority.
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
    def __init__(
            self, account, permission_name, authority, 
            parent_permission_name,
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
        # import pdb; pdb.set_trace()
        self.account_name = interface.account_arg(account)
        args = [self.account_name]

        if isinstance(permission_name, interface.Permission):
            permission_name = permission_name.value
        args.append(permission_name)

        if authority:
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
                        
        self.console = None
        self.data = None
        
        cleos._Cleos.__init__(
            self, args, "set", "account permission", is_verbose)

        if not dont_broadcast:
            self.console = self.json["processed"]["action_traces"][0]["console"]
            self.data = self.json["processed"]["action_traces"][0]["act"]["data"]

        self.printself()


class SetActionPermission(cleos._Cleos):
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
    def __init__(
            self, account, code, type, requirement,
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
        # import pdb; pdb.set_trace()
        self.account_name = interface.account_arg(account)
        args = [self.account_name]

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
                        
        self.console = None
        self.data = None
        
        cleos._Cleos.__init__(
            self, args, "set", "action permission", is_verbose)

        if not dont_broadcast:
            self.console = self.json["processed"]["action_traces"][0]["console"]
            self.data = self.json["processed"]["action_traces"][0]["act"]["data"]

        self.printself()