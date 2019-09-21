"""Object factories for the class :class:`.interface.Account`."""
import importlib

import eosfactory.core.manager as manager
import eosfactory.core.logger as logger

import eosfactory.core.setup as setup
import eosfactory.core.config as config
import eosfactory.core.errors as errors
import eosfactory.core.interface as interface

BASE_COMMANDS = importlib.import_module(".base", setup.interface_package())
SYS_COMMANDS = importlib.import_module(".sys", setup.interface_package())


class Eosio(interface.Account):
    def __init__(self, account_object_name):
        interface.Account.__init__(
            self, "eosio",
            BASE_COMMANDS.CreateKey(
                config.eosio_key_public(),
                config.eosio_key_private(),
                is_verbose=False))
        self.account_object_name = account_object_name

    def info(self):
        msg = manager.accout_names_2_object_names(
            "account object name: {}\n{}".format(
                self.account_object_name,
                (BASE_COMMANDS.GetAccount(self.name, is_verbose=False))),
                True)
        print(msg)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class GetAccount(BASE_COMMANDS.GetAccount):
    """Given a name, get an account object.

    Get an object, of the class :class:`.interface.Account` (having the name and a pair of keys), implementing the account having the given name. The name may or may not represent an existing account.
    """
    def __init__(
            self,
            account_object_name, name=None, 
            owner_key_private=None, active_key_private=None):

        self.account_object_name = account_object_name
        if name is None: 
            self.name = BASE_COMMANDS.account_name()
        else:
            self.name = name

        if active_key_private is None:
            active_key_private = owner_key_private

        self.exists = False
        
        try:
            BASE_COMMANDS.GetAccount.__init__(
                                self, self.name, json=True, is_verbose=False)
        except errors.AccountDoesNotExistError:
            return
        except Exception as ex:
            raise errors.Error(str(ex))

        self.exists = True
        self.owner_key = interface.Key(self.owner_key_public, None)
        self.active_key = interface.Key(self.active_key_public, None)
        if owner_key_private:
            self.owner_key.key_private = owner_key_private
            self.active_key.key_private = active_key_private

        logger.TRACE("""
            * Account *{}* exists in the blockchain.
            """.format(self.name))

    def __repr__(self):
        return self.name


class CreateAccount(BASE_COMMANDS.CreateAccount):
    def __init__(
            self, creator, name, owner_key, 
            active_key=None,
            permission=None,
            expiration_sec=None, 
            skip_sign=0, 
            dont_broadcast=0,
            force_unique=0,
            max_cpu_usage=0,
            max_net_usage=0,
            ref_block=None,
            delay_sec=0):
        
        BASE_COMMANDS.CreateAccount.__init__(
            self, creator, name, owner_key, active_key, permission,
            expiration_sec, skip_sign, dont_broadcast, force_unique,
            max_cpu_usage, max_net_usage,
            ref_block, delay_sec, is_verbose=False
            )


class SystemNewaccount(SYS_COMMANDS.SystemNewaccount):
    def __init__(
            self, creator, name, owner_key, 
            active_key=None,
            stake_net=0, stake_cpu=0,
            permission=None,
            ram_bytes=0, ram_kbytes=0, buy_ram="",
            transfer=False,
            expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0):

        SYS_COMMANDS.SystemNewaccount.__init__(
            self, creator, name, owner_key, active_key,
            stake_net, stake_cpu, permission, 
            ram_bytes, ram_kbytes, buy_ram,
            transfer, expiration_sec, skip_sign, dont_broadcast, force_unique,
            max_cpu_usage, max_net_usage, ref_block, delay_sec,
            is_verbose=False)
        
