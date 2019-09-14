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
        buy_ram_bytes (int): The amount of RAM bytes to purchase for the new
            account in bytes.
        buy_ram_kbytes (int): The amount of RAM bytes to purchase for the new
            account in kibibytes (KiB)
        transfer (bool): Transfer voting power and right to unstake EOS to receiver.

    See definitions of the remaining parameters: \
    :func:`.cleos.base.common_parameters`.
    """
    def __init__(
            self, creator, name, owner_key, active_key,
            stake_net=0, stake_cpu=0,
            permission=None,
            buy_ram_bytes=0, buy_ram_kbytes=0, buy_ram=None,
            transfer=False,
            expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose = 1
            ):
        
        if name is None: 
            name = base_commands.account_name()
        interface.Account.__init__(self, name, owner_key, active_key)

        if not expiration_sec:
            expiration_sec = 30

        if buy_ram_kbytes:
            buy_ram_bytes = buy_ram_kbytes * 1024

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
                "blocksBehind": delay_sec * 2,
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
                        "bytes": buy_ram_bytes,
                    } if buy_ram_bytes else "",
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
        amount (int): The amount of EOS to pay for RAM, or number of kbytes 
            of RAM if ``buy_ram_kbytes`` is set.
        buy_ram_bytes (bool): If set, buy ram in number of bytes,
        buy_ram_kbytes (bool): If set, buy ram in number of kbytes.

    See definitions of the remaining parameters: \
    :func:`.cleos.base.common_parameters`.
    """
    def __init__(
            self, payer, receiver, amount,
            buy_ram_bytes=False, buy_ram_kbytes=False,
            expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=1
            ):

        self.payer = interface.account_arg(payer)
        self.receiver = interface.account_arg(receiver)
        self.amount = str(amount)

        if buy_ram_kbytes:
            amount = amount * 1024

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
                "blocksBehind": delay_sec * 2,
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
                        "bytes": amount,
                    } if buy_ram_bytes or buy_ram_kbytes else "",
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
                        "quant": amount,
                    } if not (buy_ram_bytes or buy_ram_kbytes) else "",
            }, is_verbose)


        self.printself(is_verbose)

    
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
                "blocksBehind": delay_sec * 2,
                "transfer": "true" if transfer else "false",
                "stake_net_quantity": "%0.4f EOS" % (stake_net_quantity),
                "stake_cpu_quantity": "%0.4f EOS" % (stake_cpu_quantity),
            }, is_verbose)

        self.printself(is_verbose)

