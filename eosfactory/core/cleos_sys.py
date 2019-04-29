import eosfactory.core.cleos as cleos
import eosfactory.core.interface as interface

def reload():
    import importlib
    importlib.reload(cleos)


class SystemNewaccount(interface.Account, cleos.Cleos):
    ''' Create an account, buy ram, stake for bandwidth for the account.

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
            account in EOS.
        buy_ram_kbytes (int): The amount of RAM bytes to purchase for the new 
            account in kibibytes (KiB)
        transfer (bool): Transfer voting power and right to unstake EOS to receiver.

    See definitions of the remaining parameters: \
    :func:`.cleos.common_parameters`.
    '''
    def __init__(
            self, creator, name, owner_key, active_key,
            stake_net, stake_cpu,
            permission=None,
            buy_ram_kbytes=0, buy_ram="",
            transfer=False,
            expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose = 1
            ):

        stake_net = "{} EOS".format(stake_net)
        stake_cpu = "{} EOS".format(stake_cpu)
        
        if name is None: 
            name = cleos.account_name()
        interface.Account.__init__(self, name)

        self.owner_key = None # private keys
        self.active_key = None
        
        if active_key is None:
            active_key = owner_key

        args = [
            interface.account_arg(creator), self.name, 
                interface.key_arg(owner_key, is_owner_key=True, is_private_key=False), 
                interface.key_arg(active_key, is_owner_key=False, is_private_key=False)
            ]

        args.append("--json")
        args.extend([
            "--stake-net", stake_net, 
            "--stake-cpu", stake_cpu])
        if buy_ram_kbytes:
            args.extend(["--buy-ram-kbytes", str(buy_ram_kbytes)])
        if buy_ram:
            args.extend(["--buy-ram", str(buy_ram)])
        if transfer:
            args.extend(["--transfer"])
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
            args.extend(["--delay-sec", delay_sec])

        cleos.Cleos.__init__(
            self, args, "system", "newaccount", is_verbose)
            
        self.json = cleos.GetAccount(
            self.name, is_verbose=0, is_info=False).json

        if self.is_verbose:
            print(self.__str__())
            
    def __str__(self):
        return self.name


class BuyRam(cleos.Cleos):
    ''' Buy RAM.

    Args:
        payer (str or .interface.Account): The account paying for RAM.
        receiver (str or .interface.Account): The account receiving bought RAM.
        amount (int): The amount of EOS to pay for RAM, or number of kbytes 
            of RAM if ``buy_ram_kbytes`` is set.
        buy_ram_kbytes (bool): If set, buy ram in number of kbytes.

    See definitions of the remaining parameters: \
    :func:`.cleos.common_parameters`.
    '''
    def __init__(
            self, payer, receiver, amount,
            buy_ram_kbytes=0, 
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

        args = [self.payer, self.receiver, self.amount]

        if buy_ram_kbytes:
            args.extend(["--kbytes"])
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
        if max_net_usage:
            args.extend(["--max-net-usage", str(max_net_usage)])
        if not ref_block is None:
            args.extend(["--ref-block", ref_block])
        if delay_sec:
            args.extend(["--delay-sec", delay_sec])

        cleos.Cleos.__init__(
            self, args, "system", "buyram", is_verbose)

    
class DelegateBw(cleos.Cleos):
    '''Delegate bandwidth.

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
    :func:`.cleos.common_parameters`.           
    '''
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

        self.payer = interface.account_arg(payer)
        self.receiver = interface.account_arg(receiver)
        self.stake_net_quantity = stake_net_quantity
        self.stake_cpu_quantity = stake_cpu_quantity

        args = [
            self.payer, self.receiver,
            "{} EOS".format(self.stake_net_quantity),
            "{} EOS".format(self.stake_cpu_quantity),
            "--expiration", str(expiration_sec),
            "--json"]

        if not permission is None:
            p = interface.permission_arg(permission)
            for perm in p:
                args.extend(["--permission", perm])
        if transfer:
            args.append("--transfer")
        if skip_sign:
            args.append("--skip-sign")
        if dont_broadcast:
            args.append("--dont-broadcast")
        if force_unique:
            args.append("--force-unique")
        if max_cpu_usage:
            args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
        if max_net_usage:
            args.extend(["--max-net-usage", str(max_net_usage)])
        if not ref_block is None:
            args.extend(["--ref-block", ref_block])
        if delay_sec:
            args.extend(["--delay-sec", delay_sec])            

        cleos.Cleos.__init__(
            self, args, "system", "delegatebw", is_verbose)




            
