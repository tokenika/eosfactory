import sys
import setup
import eosf
import node
from termcolor import cprint


setup.set_verbose(False)
setup.use_keosd(False)
setup.set_json(False)


contract_dir = sys.path[0] + "/../"


def test():
    testnet = node.reset(is_verbose=False)
    assert(not testnet.error)
    cprint(
        "Started a local testnet: {}".format(not testnet.error), 
        'magenta')

    wallet = eosf.Wallet()
    assert(not wallet.error)
    cprint(
        "The wallet is unlocked: {}".format(not wallet.error), 
        'magenta')

    account_master = eosf.AccountMaster(is_verbose=False)
    assert(not account_master.error)
    cprint(
        "The account_master is in the wallet: {}" \
            .format(not account_master.error), 
        'magenta')
    wallet.import_key(account_master)

    contract_eosio_bios = eosf.Contract(
        account_master, "eosio.bios", is_verbose=False).deploy()
    assert(not contract_eosio_bios.error)
    cprint(
        "The contract_eosio_bios is deployed: {}" \
            .format(not contract_eosio_bios.error), 
         'magenta') 

    cprint("account = eosf.account()", 'magenta')
    account = eosf.account()
    wallet.import_key(account)    

    cprint("contract = eosf.Contract(account, contract_dir)", 'magenta')
    contract = eosf.Contract(account, contract_dir)

    cprint("contract.deploy()", 'magenta')
    assert(not contract.deploy(is_verbose=0).error)

    cprint("contract.code()", 'magenta')
    code = contract.code()
    print("code hash: {}".format(code.code_hash))

    cprint("alice = eosf.account()", 'magenta')
    alice = eosf.account()
    assert(not alice.error)
    wallet.import_key(alice)

    cprint("carol = eosf.account()", 'magenta')
    carol = eosf.account()
    assert(not carol.error)
    wallet.import_key(carol) 

    cprint(
        """contract.push_action("hi", '{"user":"' + str(alice) + '"}', alice)""", 'magenta')
    assert(not contract.push_action(
        "hi", '{"user":"' + str(alice) + '"}', alice, console=True).error)

    cprint(
        """contract.push_action("hi", '{"user":"' + str(carol) + '"}', carol)""", 'magenta')
    assert(not contract.push_action(
        "hi", '{"user":"' + str(carol) + '"}', carol, console=True).error)

    testnet = node.stop()
    assert(not testnet.error)
    cprint(
        "Closed the local testnet: {}".format(not testnet.error), 'magenta')


if __name__ == "__main__":
    test()
