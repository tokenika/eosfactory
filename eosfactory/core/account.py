import eosfactory.core.config as config
import eosfactory.core.errors as errors
import eosfactory.core.interface as interface
import eosfactory.core.cleos as cleos
import eosfactory.core.cleos_sys as cleos_sys
import eosfactory.core.manager as manager
import eosfactory.core.logger as logger


class Eosio(interface.Account):
    def __init__(self, account_object_name):
        interface.Account.__init__(self, "eosio",
        cleos.CreateKey(
            config.eosio_key_public(),
            config.eosio_key_private()
            ))
        self.account_object_name = account_object_name

    def info(self):
        msg = manager.accout_names_2_object_names(
            "account object name: {}\nname: {}\n{}".format(
                self.account_object_name, 
                self.name,
                cleos.GetAccount(self.name, is_verbose=False).out_msg),
                True)
        print(msg)

    def __str__(self):
        return self.name

    def __repr__(self):
        return ""


class GetAccount(cleos.GetAccount):  
    def __init__(
            self,
            account_object_name, name=None, 
            owner_key=None, active_key=None):

        self.account_object_name = account_object_name
        if name is None: 
            self.name = cleos.account_name()
        else:
            self.name = name
            
        if active_key is None:
            active_key = owner_key

        self.exists = False
        self.in_wallet_on_stack = False
        self.has_keys = not owner_key is None
        
        try:
            cleos.GetAccount.__init__(
                self, self.name, is_info=False, is_verbose=False)
        except errors.AccountDoesNotExistError:
            return

        self.exists = True
        if owner_key is None:
            self.owner_key = cleos.CreateKey(
                self.json["permissions"][1]["required_auth"]["keys"] \
                [0]["key"], 
                is_verbose=0)
        else: # an orphan account, private key is restored from cache
            self.owner_key = cleos.CreateKey(
                self.json["permissions"][1]["required_auth"]["keys"] \
                [0]["key"], interface.key_arg(
                    owner_key, is_owner_key=True, is_private_key=True),
                is_verbose=0) 

        if active_key is None:
            self.owner_key = cleos.CreateKey(
                self.json["permissions"][0]["required_auth"]["keys"] \
                [0]["key"], 
                is_verbose=0)
        else: # an orphan account, private key is restored from cache
            self.active_key = cleos.CreateKey(
                self.json["permissions"][0]["required_auth"]["keys"] \
                [0]["key"], interface.key_arg(
                    active_key, is_owner_key=False, is_private_key=True),
                is_verbose=0)

        logger.TRACE('''
            * Account *{}* exists in the blockchain.
            '''.format(self.name))

    def __str__(self):
        return self.name


class RestoreAccount(cleos.RestoreAccount):
    def __init__(self, name):
        cleos.RestoreAccount.__init__(self, name, is_verbose=False)


class CreateAccount(cleos.CreateAccount):
    def __init__(
            self, creator, name, owner_key, 
            active_key="",
            permission=None,
            expiration_sec=None, 
            skip_sign=0, 
            dont_broadcast=0,
            force_unique=0,
            max_cpu_usage=0,
            max_net_usage=0,
            ref_block=None,
            delay_sec=0):
        cleos.CreateAccount.__init__(
            self, creator, name, owner_key, active_key, permission,
            expiration_sec, skip_sign, dont_broadcast, force_unique,
            max_cpu_usage, max_net_usage,
            ref_block, delay_sec, is_verbose=False
            )


class SystemNewaccount(cleos_sys.SystemNewaccount):
    def __init__(
            self, creator, name, owner_key, active_key,
            stake_net, stake_cpu,
            permission=None,
            buy_ram_kbytes=0, buy_ram="",
            transfer=False,
            expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None):
            
        cleos_sys.SystemNewaccount.__init__(
            self, creator, name, owner_key, active_key,
            stake_net, stake_cpu, permission, buy_ram_kbytes, buy_ram,
            transfer, expiration_sec, skip_sign, dont_broadcast, force_unique,
            max_cpu_usage, max_net_usage, ref_block, is_verbose=False)
        
