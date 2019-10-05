import eosfactory.core.errors as errors
import eosfactory.core.eosjs.base as base_commands
import eosfactory.core.interface as interface


class SystemNewaccount(interface.Account, base_commands.Command):
    """ Create an account, buy ram, stake for bandwidth for the account.

    Args:
        creator (str or .interface.Account): The account creating
            the new account.
        name: The name of the new account.
        owner_key (str): If set, the owner public key for the new account,
            otherwise random.
        active_key (str): If set, the active public key for the new account,
            otherwise random.
        stake_net (int): The amount of EOS delegated for net bandwidth.
        stake_cpu (int): The amount of EOS delegated for CPU bandwidth.
        buy_ram (str): The amount of RAM bytes to purchase for the new
            account in tokens.
        ram_bytes (int): The amount of RAM bytes to purchase for the new
            account in bytes.
        ram_kbytes (int): The amount of RAM bytes to purchase for the new
            account in kibibytes (KiB)
        transfer (bool): Transfer voting power and right to unstake EOS to receiver.

    See definitions of the remaining parameters: \
    :func:`.cleos.base.common_parameters`.
    """
    def __init__(
            self, creator, name, owner_key, active_key,
            stake_net=0, stake_cpu=0,
            permission=None,
            ram_bytes=0, ram_kbytes=0, buy_ram=None,
            transfer=False,
            expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose = 1
            ):
        
        name = interface.account_arg(
                                name if name else base_commands.account_name())
        creator = interface.account_arg(creator)
        expiration_sec = expiration_sec if expiration_sec else 30
        quantity = 0
        if ram_bytes:
            quantity = int(ram_bytes)
        if ram_kbytes:
            quantity += int(ram_kbytes) * 1024

        interface.Account.__init__(self, name, owner_key, active_key)

        # if not permission is None:
        #     p = interface.permission_arg(permission)
        #     for perm in p:
        #         args.extend(["--permission", perm])

        base_commands.common_parameters(
            force_unique=force_unique,
            max_cpu_usage=max_cpu_usage,
            max_net_usage=max_net_usage,
            ref_block=ref_block
            )

        base_commands.Command.__init__(
            self, base_commands.config_api(),
            """
        ;(async () => {
            console.log(JSON.stringify(await api.transact(
                {
                    actions: [
                        {
                            account: 'eosio',
                            name: 'newaccount',
                            authorization: [
                                {
                                    actor: '%(creator)s',
                                    permission: 'active',
                                }
                            ],
                            data: {
                                creator: '%(creator)s',
                                name: '%(name)s',
                                owner: {
                                    threshold: 1,
                                    keys: [
                                        {
                                            key: '%(owner_key_public)s',
                                            weight: 1
                                        }
                                    ],
                                    accounts: [],
                                    waits: []
                                },
                                    active: {
                                    threshold: 1,
                                    keys: [
                                        {
                                            key: '%(active_key_public)s',
                                            weight: 1
                                        }
                                    ],
                                    accounts: [],
                                    waits: []
                                }
                            }
                        },%(buyrambytes)s%(buyram)s
                        {
                            account: 'eosio',
                            name: 'delegatebw',
                            authorization: [
                                {
                                    actor: '%(creator)s',
                                    permission: 'active',
                                }
                            ],
                            data: {
                                from: '%(creator)s',
                                receiver: '%(name)s',
                                stake_net_quantity: '%(stake_net_quantity)s',
                                stake_cpu_quantity: '%(stake_cpu_quantity)s',
                                transfer: %(transfer)s
                            }
                        }
                    ]
                },
                {
                    blocksBehind: %(blocksBehind)d,
                    expireSeconds: %(expiration_sec)d,
                    broadcast: %(broadcast)s,
                    sign: %(sign)s,
                }
            )));
        })();
            """ % {
                "creator": creator,
                "name": name,
                "owner_key_public": interface.key_arg(
                    owner_key, is_owner_key=True, is_private_key=False),
                "active_key_public": interface.key_arg(
                    active_key, is_owner_key=True, is_private_key=False),
                "expiration_sec": expiration_sec,
                "broadcast": "false" if dont_broadcast else "true",
                "sign": "false" if skip_sign else "true",
                "blocksBehind": delay_sec * 2 if delay_sec else 3,
                "transfer": "true" if transfer else "false",
                "stake_net_quantity": "%0.4f EOS" % (stake_net),
                "stake_cpu_quantity": "%0.4f EOS" % (stake_cpu),
                "buyrambytes": """
                    {
                        account: 'eosio',
                        name: 'buyrambytes',
                        authorization: [
                            {
                                actor: '%(creator)s',
                                permission: 'active',
                            }
                        ],
                        data: {
                            payer: '%(creator)s',
                            receiver: '%(name)s',
                            bytes: %(bytes)d
                        }
                    },""" % {
                        "creator": creator,
                        "name": name,
                        "bytes": quantity,
                    } if quantity else "",
                "buyram" : """
                    {
                        account: 'eosio',
                        name: 'buyram',
                        authorization: [
                            {
                                actor: '%(creator)s',
                                permission: 'active',
                            }
                        ],
                        data: {
                            payer: '%(creator)s',
                            receiver: '%(name)s',
                            quant: '%(quant)s'
                        }
                    },""" % {
                        "creator": creator,
                        "name": name,
                        "quant": buy_ram,
                    } if buy_ram else "",
            }, is_verbose)

        self.printself(is_verbose)

    def __repr__(self):
        return self.name

    def __str__(self):
        import eosfactory.core.str.actions
        return str(eosfactory.core.str.actions.Actions(self.json))


class BuyRam(base_commands.Command):
    """ Buy RAM.

    Args:
        payer (str or .interface.Account): The account paying for RAM.
        receiver (str or .interface.Account): The account receiving bought RAM.
        buy_ram (str): The amount of tokens to pay for RAM
        ram_bytes (int): If set, buy ram in number of bytes.
        ram_kbytes (int): If set, buy ram in number of kbytes.

    See definitions of the remaining parameters: \
    :func:`.cleos.base.common_parameters`.
    """
    def __init__(
            self, payer, receiver,
            buy_ram=None, ram_bytes=0, ram_kbytes=0,
            expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=1
            ):

        payer = interface.account_arg(payer)
        receiver = interface.account_arg(receiver)
        expiration_sec = expiration_sec if expiration_sec else 30
        quantity = 0
        if ram_bytes:
            quantity = int(ram_bytes)
        if ram_kbytes:
            quantity += int(ram_kbytes) * 1024

        base_commands.common_parameters(
            force_unique=force_unique,
            max_cpu_usage=max_cpu_usage,
            max_net_usage=max_net_usage,
            ref_block=ref_block
            )

        base_commands.Command.__init__(
            self, base_commands.config_api(),
            """
        ;(async () => {
            console.log(JSON.stringify(await api.transact(
                {
                    actions: [
                        %(buyrambytes)s%(buyram)s
                    ]
                },
                {
                    blocksBehind: %(blocksBehind)d,
                    expireSeconds: %(expiration_sec)d,
                    broadcast: %(broadcast)s,
                    sign: %(sign)s,
                }
            )));
        })();
            """ % {
                "expiration_sec": expiration_sec,
                "broadcast": "false" if dont_broadcast else "true",
                "sign": "false" if skip_sign else "true",
                "blocksBehind": delay_sec * 2 if delay_sec else 3,
                "buyrambytes": """
                    {
                        account: 'eosio',
                        name: 'buyrambytes',
                        authorization: [
                            {
                                actor: '%(payer)s',
                                permission: 'active',
                            }
                        ],
                        data: {
                            payer: '%(payer)s',
                            receiver: '%(receiver)s',
                            bytes: %(bytes)d
                        }
                    },""" % {
                        "payer": payer,
                        "receiver": receiver,
                        "bytes": quantity,
                    } if quantity else "",
                "buyram" : """
                    {
                        account: 'eosio',
                        name: 'buyram',
                        authorization: [
                            {
                                actor: '%(payer)s',
                                permission: 'active',
                            }
                        ],
                        data: {
                            payer: '%(payer)s',
                            receiver: '%(receiver)s',
                            quant: '%(quant)s'
                        }
                    },""" % {
                        "payer": payer,
                        "receiver": receiver,
                        "quant": buy_ram,
                    } if buy_ram else "",
            }, is_verbose)

        self.printself(is_verbose)

    def __str__(self):
        import eosfactory.core.str.actions
        return str(eosfactory.core.str.actions.Actions(self.json))

    
class DelegateBw(base_commands.Command):
    """Delegate bandwidth.

    Args:
        payer (str or .interface.Account): The account to delegate bandwidth 
            from.
        receiver (str or .interface.Account): The account to receive the 
            delegated bandwidth.
        stake_net_quantity (int): The amount of EOS to stake for network bandwidth.
        stake_cpu_quantity (int): The amount of EOS to stake for CPU bandwidth.
        transfer (bool): Transfer voting power and right to unstake EOS to 
            receiver.

    See definitions of the remaining parameters: \
    :func:`.cleos.base.common_parameters`.           
    """
    def __init__(
        self, payer, receiver, stake_net_quantity, stake_cpu_quantity,
        permission=None,
        transfer=False,
        expiration_sec=None, 
        skip_sign=0, dont_broadcast=0, force_unique=0,
        max_cpu_usage=0, max_net_usage=0,
        ref_block=None,
        delay_sec=0,
        is_verbose=1):

        payer = interface.account_arg(payer)
        receiver = interface.account_arg(receiver)
        expiration_sec = expiration_sec if expiration_sec else 30

        # if not permission is None:
        #     p = interface.permission_arg(permission)
        #     for perm in p:
        #         args.extend(["--permission", perm])         

        base_commands.common_parameters(
            force_unique=force_unique,
            max_cpu_usage=max_cpu_usage,
            max_net_usage=max_net_usage,
            ref_block=ref_block
            )

        base_commands.Command.__init__(
            self, base_commands.config_api(),
            """
        ;(async () => {
            console.log(JSON.stringify(await api.transact(
                {
                    actions: [
                        {
                            account: 'eosio',
                            name: 'delegatebw',
                            authorization: [
                                {
                                    actor: '%(payer)s',
                                    permission: 'active',
                                }
                            ],
                            data: {
                                from: '%(payer)s',
                                receiver: '%(receiver)s',
                                stake_net_quantity: '%(stake_net_quantity)s',
                                stake_cpu_quantity: '%(stake_cpu_quantity)s',
                                transfer: %(transfer)s
                            }
                        }
                    ]
                },
                {
                    blocksBehind: %(blocksBehind)d,
                    expireSeconds: %(expiration_sec)d,
                    broadcast: %(broadcast)s,
                    sign: %(sign)s,
                }
            )));
        })();
            """ % {
                "payer": payer,
                "receiver": receiver,
                "expiration_sec": expiration_sec,
                "broadcast": "false" if dont_broadcast else "true",
                "sign": "false" if skip_sign else "true",
                "blocksBehind": delay_sec * 2 if delay_sec else 3,
                "transfer": "true" if transfer else "false",
                "stake_net_quantity": "%0.4f EOS" % (stake_net_quantity),
                "stake_cpu_quantity": "%0.4f EOS" % (stake_cpu_quantity),
            }, is_verbose)

        self.printself(is_verbose)

