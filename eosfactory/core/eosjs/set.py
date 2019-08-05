import re
import os

import eosfactory.core.errors as errors
import eosfactory.core.manager as manager
import eosfactory.core.interface as interface
import eosfactory.core.eosjs.base as base_commands
import eosfactory.core.common as common


class SetContract(base_commands.Command):
    '''Create or update the contract on an account.

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
    '''
    def __init__(
            self, account, contract_dir, 
            wasm_file=None, abi_file=None, 
            clear=False,
            permission=None, expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=True,
            json=True):

        files = common.contract_is_built(contract_dir, wasm_file, abi_file)
        if not files:
            raise errors.Error("""
            Cannot determine the contract directory. The clue is 
            {}.
            """.format(contract_dir))

        self.contract_path_absolute = files[0]
        wasm_file = files[1]
        abi_file = files[2]

        self.account_name = interface.account_arg(account)
        if not permission is None:
            permission = interface.permission_arg(permission)
        if not expiration_sec:
            expiration_sec = 30
        base_commands.not_json_false(json)           

        # if clear:
        #     args.append("--clear")
        # if force_unique:
        #     args.append("--force-unique")
        # if max_cpu_usage:
        #     args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
        # if  max_net_usage:
        #     args.extend(["--max-net-usage", str(max_net_usage)])
        # if  ref_block:
        #     args.extend(["--ref-block", ref_block])

        base_commands.Command.__init__(
            self,
            '''
    const fs = require(`fs`)
    const path = require(`path`)
    const { Serialize } = require(`eosjs`)

            ''' + base_commands.config_api()
            ,
            '''
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
                blocksBehind: 3,
                expireSeconds: %(expiration_sec)d,
                broadcast: %(broadcast)s,
                sign: %(sign)s,                 
            }
        )
        console.log(JSON.stringify(result))
    })()

            ''' % {
                "wasm_file": wasm_file,
                "abi_file": abi_file,
                "account_name": self.account_name,
                "permissions": base_commands.permission_str(permission, self.account_name),
                "expiration_sec": expiration_sec,
                "broadcast": "false" if dont_broadcast else "true",
                "sign": "false" if skip_sign else "true",
            }, is_verbose)
        
        self.printself()



class SetAccountPermission(base_commands.Command):
    '''Set parameters dealing with account permissions.

    Args:
        account (str or .interface.Account): The account to set/delete a 
            permission authority for.
        permission_name (str or .Permission): The permission to set/delete an 
            authority for (defaults to: "active").
        parent_permission_name (str or .Permission): The permission name of 
            this parents permission (defaults to: "active").
        authority (str or dict or filename):  None to delete.
        add_code (bool): If set, add 'eosio.code' permission to specified 
            permission authority. Default is false.
        remove_code (bool): If set, remove 'eosio.code' permission from 
            specified permission authority. Default is false.
        
    Exemplary values of the argument *authority*::

        # bob, carol are account objects created with 
        # shell.account.create_account factory function

        str_value = "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"

        permission_value = bob.active_public()

        dict_value = {
            "threshold" : 100, 
            "keys" : [], 
            "accounts" : 
                [
                    {
                        "permission":
                            {
                                "actor": bob.active_public(),
                                "permission":"active"
                            },
                        "weight":100
                    }
                ]
        }

    See definitions of the remaining parameters: \
    :func:`.cleos.base.common_parameters`.

    Attributes:
        account_name (str): The EOSIO name of the contract's account.
        console (str): *["processed"]["action_traces"][0]["console"]*
            component of EOSIO cleos responce.
        data (str): *["processed"]["action_traces"][0]["act"]["data"]*
            component of EOSIO cleos responce.
    '''
    def __init__(
            self, account, permission_name, 
            authority=None, 
            parent_permission_name=None,
            permission=None,
            add_code=False,
            remove_code=False,
            expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, return_packed=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=True, json=True
        ):
        account_name = interface.account_arg(account)
        args = [account_name]

        if not permission_name:
            permission_name = "active"
        if isinstance(permission_name, interface.Permission):
            permission_name = permission_name.value
        args.append(permission_name)

        if authority:
            authority = manager.data_json(authority)
            if isinstance(authority, interface.Account):
                args.append(authority.active_public())
            else:
                authority =  re.sub(re.compile(r'\s+'), '', authority)
                args.append(authority)

        if isinstance(parent_permission_name, interface.Permission):
            parent_permission_name = parent_permission_name.value
                
        if parent_permission_name:
            parent_permission_name = interface.permission_arg(
                parent_permission_name)[0]
            args.append(parent_permission_name)

        if json:
            args.append("--json")
        
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
                        
        # base_commands.Command.__init__(
        #     self, args, "set", "account permission", is_verbose)
        self.account_name = account_name
        self.console = None
        self.data = None

        if json and not dont_broadcast:
            self.console = self.json["processed"]["action_traces"][0]["console"]
            self.data = self.json["processed"]["action_traces"][0]["act"]["data"]

        self.printself()    


class SetActionPermission(base_commands.Command):
    '''Set parameters dealing with account permissions.

    Args:
        account (str or .interface.Account): The account to set/delete a 
            permission authority for.
        code (str or .interface.Account): The account that owns the code for \
            the action.
        action_type (str): The type of the action.
        requirement (str): The permission name require for executing the given 
            action.

    See definitions of the remaining parameters: \
    :func:`.cleos.base.common_parameters`.

    Attributes:
        account_name (str): The EOSIO name of the contract's account.
        console (str): *["processed"]["action_traces"][0]["console"]* \
            component of EOSIO cleos responce.
        data (str): *["processed"]["action_traces"][0]["act"]["data"]* \
            component of EOSIO cleos responce.
    '''
    def __init__(
            self, account, code, action_type, requirement,
            permission=None,
            expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, return_packed=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=True, json=True
        ):
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

        base_commands.Command.__init__(self, args, "set", "action permission", is_verbose)
        self.console = None
        self.data = None

        if json and not dont_broadcast:
            self.console = self.json["processed"]["action_traces"][0]["console"]
            self.data = self.json["processed"]["action_traces"][0]["act"]["data"]

        self.printself()
