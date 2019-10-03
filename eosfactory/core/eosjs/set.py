import re
import os
import json as json_module

import eosfactory.core.errors as errors
import eosfactory.core.manager as manager
import eosfactory.core.interface as interface
import eosfactory.core.eosjs.base as base_commands
import eosfactory.core.common as common


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

        account = interface.account_arg(account)
        expiration_sec = expiration_sec if expiration_sec else 30
        permission = base_commands.permission_str(permission, account)
        files = common.contract_is_built(contract_dir, wasm_file, abi_file)
        if not files:
            raise errors.UserError("""
            Cannot determine the contract directory. The clue is 
            {}.
            """.format(contract_dir))

        self.contract_path_absolute = files[0]
        wasm_file = files[1]
        abi_file = files[2]
        
        # if clear:
        #     args.append("--clear")
        # you should first empty any tables out before setting the wasm code to an empty array.

        base_commands.common_parameters(
            force_unique=force_unique,
            max_cpu_usage=max_cpu_usage,
            max_net_usage=max_net_usage,
            ref_block=ref_block
            )

        base_commands.Command.__init__(
            self,
            """
    const fs = require(`fs`)
    const path = require(`path`)
    const { Serialize } = require(`eosjs`)

            """ + base_commands.config_api()
            ,
            """
    ;(async () => {
        const permissions = JSON.parse('%(permissions)s')
        const wasm = fs.readFileSync('%(wasm_file)s').toString(`hex`)
        const buffer = new Serialize.SerialBuffer({
            textEncoder: api.textEncoder,
            textDecoder: api.textDecoder,
        })

        let abi = JSON.parse(fs.readFileSync('%(abi_file)s', `utf8`))
        const abiDefinition = api.abiTypes.get(`abi_def`)
        // need to make sure abi has every field in abiDefinition.fields
        // otherwise serialize throws
        abi = abiDefinition.fields.reduce(
            (acc, { name: fieldName }) =>
            Object.assign(acc, { [fieldName]: acc[fieldName] || [] }),
            abi
        )
        abiDefinition.serialize(buffer, abi)
        let abi_ = Buffer.from(buffer.asUint8Array()).toString(`hex`)

        //Send transaction with both setcode and setabi actions
        const result = await api.transact(
            {
                actions: [
                    {
                        account: 'eosio',
                        name: 'setcode',
                        authorization: permissions,
                        data: {
                            account: '%(account_name)s',
                            vmtype: 0,
                            vmversion: 0,
                            code: wasm,
                        },
                    },
                    {
                        account: 'eosio',
                        name: 'setabi',
                        authorization: permissions,
                        data: {
                            account: '%(account_name)s',
                            abi: Buffer.from(buffer.asUint8Array()).toString(`hex`),
                        },
                    },
                ],
            },
            {
                blocksBehind: %(blocksBehind)d,
                expireSeconds: %(expiration_sec)d,
                broadcast: %(broadcast)s,
                sign: %(sign)s,                 
            }
        )
        console.log(JSON.stringify(result))
    })()

            """ % {
                "wasm_file": wasm_file,
                "abi_file": abi_file,
                "account_name": account,
                "permissions": permission,
                "expiration_sec": expiration_sec,
                "broadcast": "false" if dont_broadcast else "true",
                "sign": "false" if skip_sign else "true",
                "blocksBehind": delay_sec * 2,
            }, is_verbose)
        
        self.printself()


class SetAccountPermission(base_commands.Command):
    """Set parameters dealing with account permissions.

    Args:
        account (str or .interface.Account): The account to set/delete
            a permission authority for.
        permission_name (str or .Permission): The permission to set/delete
            an authority for.
        authority (str or dict or filename): Public key, JSON string or
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

# actions: [
    # {
    #     account: 'eosio',
    #     authorization: [{
    #         actor: 'miniminimini',
    #         permission: 'active',
    #     }],
    #     name: 'updateauth',

    #     data: {
    #         account: 'miniminimini',
    #         permission: 'active',
    #         parent: 'owner',
    #         auth: {
    #             threshold: 1,
    #             keys: [
    #                 {
    #                     weight: 1,
    #                     key: 'EOS8Dkj827FpinZBGmhTM28B85H9eXiFH5XzvLoeukCJV5sKfLc6K',
    #                 },
    #                 {
    #                     weight: 2,
    #                     key: 'EOS8Dkj827FpinZBGmhTM28B85H9eXiFH5XzvLoeukCJV5sKfLc6K',
    #                 }
    #             ],
    #             accounts: [{
    #                 permission: {
    #                     actor: 'miniminimini',
    #                     permission: 'active',
    #                 },
    #                 weight: 3,
    #             }],
    #             waits: [
    #                 {
    #                     wait_sec: 55,
    #                     weight: 4
    #                 }
    #             ]
    #         },
    #     },

    # }
# ]


    def __init__(
            self, account, 
            permission_name, 
            authority, 
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

        base_commands.common_parameters(
            force_unique=force_unique,
            max_cpu_usage=max_cpu_usage,
            max_net_usage=max_net_usage,
            ref_block=ref_block
            )

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

        account_name = interface.account_arg(account)
        permission_name = interface.Permission.name(permission_name)
        expiration_sec = expiration_sec if expiration_sec else 30
        permission_str = base_commands.permission_str(permission, account)

        data = {}
        data["account"] = account_name
        data["parent"] \
                    = interface.Permission.name(parent) if parent else "active"
        data["permission"] = permission_name

        if add_code or remove_code:
            account_permissions = json_module.loads(base_commands.GetAccount(
                account_name, is_verbose=False).out_msg.replace(
                    "required_auth", "auth").replace(
                        "perm_name", "permission"))["permissions"]

            if add_code:
                for perm in account_permissions:
                    if perm["permission"] == permission_name:
                        data = perm
                        data["account"] = account_name
                        data["auth"]["accounts"].append({
                        "permission": {
                            "actor": interface.account_arg(authority),
                            "permission": "eosio.code"
                        },
                        "weight": 1
                        })
                        break
                if not data:
                    raise errors.UserError("""
                    There is no permission named ``{}`` among in the permition set 
                    of the account ``{}``.
                """.format(permission_name, account_name))
            else:
                for perm in account_permissions:
                    if perm["permission"] == permission_name:
                        data = perm
                        data["account"] = account_name
                        for acc in data["auth"]["accounts"]:
                            if acc["permission"]["permission"] == "eosio.code":
                                data["auth"]["accounts"].remove(acc)
                                perm = None
                                break
                        if not perm:
                            break

        elif isinstance(authority, interface.Key):
            data["auth"] = {"threshold": 1}
            data["auth"]["keys"] = [{
                        "key": authority.key_public,
                        "weight": 1
                    }]

        elif isinstance(authority, str):
            if authority.upper() == "NULL" \
                or authority.upper() == "REMOVE" \
                    or authority.upper() == "DELETE":
                authority = "NULL"
            elif interface.is_key(authority):
                data["auth"] = {"threshold": 1}
                data["auth"]["keys"] = [{
                        "key": interface.key_arg(authority),
                        "weight": 1
                    }]
            else:
                is_file = False
                if os.path.exists(authority):
                    try:
                        with open(authority, "r") as _:
                            authority = _.read()
                        is_file = True
                    except EnvironmentError as ex:
                        raise UserError(str(ex)) from ex
                
                try:
                    data["auth"] = json_module.loads(
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
        elif isinstance(authority, dict):
            data["auth"] = authority

        data = manager.data_json(data)
        try:
            data = json_module.loads(data)
        except Exception as ex:
            raise errors.UserError("""
            The value 
            {}
            of the argument ``authority`` is not valid.
        """.format(authority)) from ex

        if "auth" in data:
            if "waits" in data["auth"]:
                data["auth"]["waits"].sort(
                                key=lambda x: x["wait_sec"], reverse=True)
            else:
                data["auth"]["waits"] = []

            if "keys" in data["auth"]:
                data["auth"]["keys"].sort(key=lambda x: x["key"])
            else:
                data["auth"]["keys"] = []

            if "accounts" in data["auth"]:
                data["auth"]["accounts"].sort(key=lambda x: (
                                            x["permission"]["actor"], 
                                            x["permission"]["permission"]))
            else:
                data["auth"]["accounts"] = []

        data = json_module.dumps(data, indent=4)

        base_commands.Command.__init__(
            self,
            base_commands.config_api(),
            """
    ;(async () => {
        const permissions = JSON.parse(`%(permissions)s`)
        const data = JSON.parse(`%(data)s`)
        const result = await api.transact(
            {
                actions: [
                {
                    account: "eosio",
                    authorization: permissions,
                    name: "%(name)s",
                    data: data
                }
                ],
            },
            {
                blocksBehind: %(blocksBehind)d,
                expireSeconds: %(expiration_sec)d,
                broadcast: %(broadcast)s,
                sign: %(sign)s,
            }
        )
        console.log(JSON.stringify(result))
    })()

            """ % {
                "account_name": account_name,
                "permissions": permission_str,
                "name": "deleteauth" if authority == "NULL" else "updateauth",
                "data": data,
                "expiration_sec": expiration_sec,
                "broadcast": "false" if dont_broadcast else "true",
                "sign": "false" if skip_sign else "true",
                "blocksBehind": delay_sec * 2,
            }, is_verbose)

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
        code (str or .interface.Account): The account that owns the code for
            the action.
        action_type (str): The type of the action.
        requirement (str): The permission name require for executing the given
            action.

    See definitions of the remaining parameters:
    :func:`.cleos.base.common_parameters`.

    Attributes:
        account_name (str): The EOSIO name of the contract's account.
        console (str): ``["processed"]["action_traces"][0]["console"]``
            component of EOSIO cleos responce.
        data (str): ``["processed"]["action_traces"][0]["act"]["data"]``
            component of EOSIO cleos responce.
    """
    def __init__(
            self, account, code, action_type, requirement,
            permission=None,
            expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, return_packed=0,
            force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=True
        ):

        base_commands.common_parameters(
            force_unique=force_unique,
            max_cpu_usage=max_cpu_usage,
            max_net_usage=max_net_usage,
            ref_block=ref_block
            )

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
        expiration_sec = expiration_sec if expiration_sec else 30
        permission_str = base_commands.permission_str(permission, account)

        base_commands.Command.__init__(
            self,
            base_commands.config_api(),
            """
    ;(async () => {
        const permissions = JSON.parse(`%(permissions)s`)
        const result = await api.transact(
            {
                actions: [
                {
                    account: "eosio",
                    authorization: permissions,
                    name: "linkauth",
                    data: {
                        "account": "%(account_name)s",
                        "code": "%(code)s",
                        "type": "%(type)s",
                        "requirement": "%(requirement)s"
                    }
                }
                ],
            },
            {
                blocksBehind: %(blocksBehind)d,
                expireSeconds: %(expiration_sec)d,
                broadcast: %(broadcast)s,
                sign: %(sign)s,
            }
        )
        console.log(JSON.stringify(result))
    })()

            """ % {
                "account_name": account_name,
                "code": code,
                "type": action_type,
                "requirement": requirement,
                "permissions": permission_str,
                "expiration_sec": expiration_sec,
                "broadcast": "false" if dont_broadcast else "true",
                "sign": "false" if skip_sign else "true",
                "blocksBehind": delay_sec * 2,
            }, is_verbose)

        self.console = None
        self.data = None

        if not dont_broadcast:
            self.console = self.json["processed"]["action_traces"][0]["console"]
            self.data = self.json["processed"]["action_traces"][0]["act"]["data"]

        self.printself()

    def __str__(self):
        import eosfactory.core.str.actions
        return str(eosfactory.core.str.actions.Actions(self.json))
