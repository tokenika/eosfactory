import re
import os
import json as json_module

import eosfactory.core.errors as errors
import eosfactory.core.manager as manager
import eosfactory.core.interface as interface
import eosfactory.core.common as common
import eosfactory.core.cleos.base as base_commands


class SetContract(base_commands.Command):
    """Create or update the contract on an account.

    Args:
        account (str or .interface.Account): The account to publish a contract 
            for.
        contract_dir (str): The path to a directory.
        wasm_file (str): The WASM file relative to the contract_dir.
        abi_file (str): The ABI file for the contract relative to the 
            contract-dir.
        clear (bool): Remove contract on an account. Default is False.

    See definitions of the remaining parameters: \
    :func:`.cleos.base.common_parameters`.

    Attributes:
        contract_path_absolute (str): The path to the contract project
        account_name (str): The EOSIO name of the contract's account.
    """
    def __init__(
            self, account, contract_dir, 
            wasm_file=None, abi_file=None, 
            clear=False,
            permission=None, expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=True):

        files = common.contract_is_built(contract_dir, wasm_file, abi_file)
        if not files:
            raise errors.UserError("""
            Cannot determine the contract directory. The clue is 
            {}.
            """.format(contract_dir))

        contract_path_absolute = files[0]
        wasm_file = files[1]
        abi_file = files[2]            
        account_name = interface.account_arg(account)

        args = [account_name, contract_path_absolute]
        if os.path.isabs(wasm_file):
            wasm_file = os.path.relpath(wasm_file, contract_path_absolute)
        if os.path.isabs(abi_file):
            abi_file = os.path.relpath(abi_file, contract_path_absolute)
        
        if clear:
            args.append("--clear")
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
        if wasm_file:
            args.append(wasm_file)
        if abi_file:
            args.append(abi_file)

        base_commands.Command.__init__(self, args, "set", "contract", is_verbose)
        
        self.contract_path_absolute = files[0]
        self.account_name = interface.account_arg(account)
        self.printself()


class SetAccountPermission(base_commands.Command):
    """Set parameters dealing with account permissions.

    Args:
        account (str or .interface.Account): The account to set/delete a 
            permission authority for.
        permission_name (str or .Permission): The permission to set/delete an
            authority for.
        authority (str or dict or filename):  Public key, JSON string or
            filename defining the authority. ``NULL`` or "REMOVE" or "delete" 
            (case insensitive) to delete.
        parent (str or .Permission): The permission name of
            this parents permission (defaults to: "active").
        add_code (bool): If set, add 'eosio.code' permission to specified 
            permission authority. Default is false.
        remove_code (bool): If set, remove 'eosio.code' permission from 
            specified permission authority. Default is false.

    See definitions of the remaining parameters: \
    :func:`.cleos.base.common_parameters`.

    NOTE::

        `cleos` eosio CLI demands that the lists in the `authority` JSON are 
        specifically sorted. EOSFactory sorts them itself.

    Attributes:
        console (str): *["processed"]["action_traces"][0]["console"]*
            component of EOSIO cleos responce.
        data (str): *["processed"]["action_traces"][0]["act"]["data"]*
            component of EOSIO cleos responce.
    """

    def __init__(
            self, account, permission_name, authority,
            parent=None,
            permission=None,
            add_code=False,
            remove_code=False,
            expiration_sec=None,
            skip_sign=0, dont_broadcast=0, return_packed=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=True
        ):
        if add_code and remove_code:
            raise errors.ArgumentNotSet(message = """
        It cannot be ``add_code`` and ``remove_code`` in the same time.
        """)
        if not account:
            raise errors.ArgumentNotSet(
                        "account",
                        "the account to set/delete a permission authority for")
        if not permission_name:
            raise errors.ArgumentNotSet(
                        "permission_name",
                        "the permission to set/delete an authority for")
        if not authority:
            raise errors.ArgumentNotSet(
                "authority",
                """a public key, JSON string or filename defining the authority 
                or ``NULL`` to delete""")

        args = [
                interface.account_arg(account),
                interface.Permission.name(permission_name)
                ]

        if add_code or remove_code:
            authority = interface.account_arg(authority)
        elif isinstance(authority, interface.Key):
            authority = authority.key_public
        elif isinstance(authority, str):
            if authority.upper() == "NULL" \
                or authority.upper() == "REMOVE" \
                    or authority.upper() == "DELETE":
                authority = "NULL"
            elif interface.is_key(authority):
                authority = interface.key_arg(authority)
            else:
                is_file = False
                if os.path.exists(authority):
                    try:
                        with open(authority, "r") as _:
                            authority = _.read()
                        is_file = True
                    except EnvironmentError as ex:
                        raise errors.UserError(str(ex)) from ex
                
                try:
                    authority = json_module.loads(
                        manager.object_names_2_accout_names(authority, True))
                except Exception as ex:
                    msg = """
                The argument ``authority`` which is
                ``{}``
                points to an existing file. However, it does not contain any valid JSON string.
                                        """ if is_file else """
                The argument ``authority`` which is
                ``{}``
                is neither a valid JSON string nor EOS public key.
                        """.format(authority)
                    raise errors.UserError(msg) from ex

        if isinstance(authority, dict):
            try:
                authority = json_module.loads(manager.data_json(authority))
            except Exception as ex:
                raise errors.UserError("""
                The value 
                {}
                of the argument ``authority`` is not valid.
                """.format(authority)) from ex

            if "waits" in authority:
                authority["waits"].sort(
                                key=lambda x: x["wait_sec"], reverse=True)
            else:
                authority["waits"] = []

            if "keys" in authority:
                authority["keys"].sort(key=lambda x: x["key"])
            else:
                authority["keys"] = []

            if "accounts" in authority:
                authority["accounts"].sort(key=lambda x: (
                                            x["permission"]["actor"], 
                                            x["permission"]["permission"]))
            else:
                authority["accounts"] = []

            authority = json_module.dumps(authority)

        args.append(authority)
        if parent:
            args.append(interface.Permission.name(parent))

        if permission:
            p = interface.permission_arg(permission)
            for perm in p:
                args.extend(["--permission", perm])
        
        if add_code:
            args.append("--add-code")
        if remove_code:
            args.append("--remove-code")
        if expiration_sec:
            args.extend(["--expiration", str(expiration_sec)])
        if skip_sign:
            args.append("--skip-sign")
        if dont_broadcast:
            args.append("--dont-broadcast")
        if force_unique:
            args.append("--force-unique")
        if return_packed:
            args.append("--return-packed")
        if max_cpu_usage:
            args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
        if  max_net_usage:
            args.extend(["--max-net-usage", str(max_net_usage)])
        if  not ref_block is None:
            args.extend(["--ref-block", ref_block])
        if delay_sec:
            args.extend(["--delay-sec", str(delay_sec)])

        args.append("--json")
        base_commands.Command.__init__(
            self, args, "set", "account permission", is_verbose)

        self.console = None
        self.data = None

        if not dont_broadcast:
            self.console = self.json["processed"]["action_traces"][0]["console"]
            self.data = self.json["processed"]["action_traces"][0]["act"]["data"]

        self.printself()

    def __str__(self):
        import eosfactory.core.str.actions
        return str(eosfactory.core.str.actions.Actions(self.json))


class SetActionPermission(base_commands.Command):
    """Set parameters dealing with account permissions.

    Args:
        account (str or .interface.Account): The account to set/delete
            a permission authority for.
        code (str or .interface.Account): The account that owns the code for \
            the action.
        action_type (str): The type of the action.
        requirement (str): The permission name require for executing the given 
            action.

    See definitions of the remaining parameters: \
    :func:`.cleos.base.common_parameters`.

    Attributes:
        console (str): ``["processed"]["action_traces"][0]["console"]`` \
            component of EOSIO cleos responce.
        data (str): ``["processed"]["action_traces"][0]["act"]["data"]`` \
            component of EOSIO cleos responce.
    """
    def __init__(
            self, account, code, action_type, requirement,
            permission=None,
            expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, return_packed=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=True
        ):
        if not account:
            raise errors.ArgumentNotSet(
                        "account",
                        "the account to set/delete a permission authority for")
        if not code:
            raise errors.ArgumentNotSet(
                        "code",
                        "the account that owns the code for the action")
        if not action_type:
            raise errors.ArgumentNotSet(
                        "code",
                        "the type of the action")        
        if not requirement:
            raise errors.ArgumentNotSet(
                "requirement",
                "'NULL' or the permission name require for executing the given action")

        account_name = interface.account_arg(account)
        args = [account_name]

        code_name = interface.account_arg(code)
        args.append(code_name)

        args.append(action_type)

        if requirement:
            requirement_name = interface.account_arg(requirement)
            args.append(requirement_name)
        else:
            args.append("NULL")

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
        if return_packed:
            args.append("--return-packed")
        if max_cpu_usage:
            args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
        if  max_net_usage:
            args.extend(["--max-net-usage", str(max_net_usage)])
        if  not ref_block is None:
            args.extend(["--ref-block", ref_block])
        if delay_sec:
            args.extend(["--delay-sec", str(delay_sec)])
        args.append("--json")

        base_commands.Command.__init__(
                            self, args, "set", "action permission", is_verbose)

        self.console = None
        self.data = None

        if not dont_broadcast:
            self.console = self.json["processed"]["action_traces"][0]["console"]
            self.data = self.json["processed"]["action_traces"][0]["act"]["data"]

        self.printself()

    def __str__(self):
        import eosfactory.core.str.actions
        return str(eosfactory.core.str.actions.Actions(self.json))


    def __str__(self):
        import eosfactory.core.str.actions
        return str(eosfactory.core.str.actions.Actions(self.json))
    