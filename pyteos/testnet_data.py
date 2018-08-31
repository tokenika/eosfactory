import setup
import eosf
import front_end
import eosf_account

class Testnet:
    def __init__(self, url, name, owner_key, active_key):
        self.url = url
        self.account_name = name
        self.owner_key = owner_key
        self.active_key = active_key

    def configure(self, prefix):
        setup.set_nodeos_address(self.url, prefix)


class LocalTestnet(Testnet):
    def __init__(self, reset=False):
        if reset:
            eosf.reset(verbosity=[front_end.Verbosity.ERROR])
        else:
            eosf.resume(verbosity=[front_end.Verbosity.ERROR])
        eosio = eosf_account.Eosio("account_master")

        setup.is_local_address = True
        Testnet.__init__(
            self, 
            None, 
            eosio.name,
            eosio.owner_key.key_private, eosio.active_key.key_private)


# /mnt/c/Workspaces/EOS/eos/build/programs/cleos/cleos --url http://88.99.97.30:38888 get info
cryptolion = Testnet(
    "http://88.99.97.30:38888",
    "dgxo1uyhoytn",
    "5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY",
    "5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA"
)

kylin = Testnet(
    "https://api.kylin-testnet.eospace.io",
    "dgxo1uyhoytn",
    "5K4rezbmuoDUyBUntM3PqxwutPU3rYKrNzgF4f3djQDjfXF3Q67",
    "5JCvLMJVR24WWvC6qD6VbLpdUMsjhiXmcrk4i7bdPfjDfNMNAeX"
)

local = Testnet(
    "https://api.kylin-testnet.eospace.io",
    "eosio",
    "5K4rezbmuoDUyBUntM3PqxwutPU3rYKrNzgF4f3djQDjfXF3Q67",
    "5JCvLMJVR24WWvC6qD6VbLpdUMsjhiXmcrk4i7bdPfjDfNMNAeX"
)