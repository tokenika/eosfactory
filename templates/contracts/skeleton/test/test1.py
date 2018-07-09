import sys
import setup
import eosf
import node
from termcolor import cprint

setup.set_verbose(False)
setup.use_keosd(False)
setup.set_json(False)

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

    cprint("account_deploy = eosf.account(account_master)", 'magenta')
    account_deploy = eosf.account(account_master)
    wallet.import_key(account_deploy)

    cprint("""contract = eosf.Contract(account_deploy, sys.path[0] + "/../")""", 'magenta')
    contract = eosf.Contract(account_deploy, sys.path[0] + "/../")

    cprint("contract.deploy()", 'magenta')
    assert(not contract.deploy(is_verbose=0).error)

    cprint("contract.code()", 'magenta')
    code = contract.code()
    print("code hash: {}".format(code.code_hash))

    cprint("account_alice = eosf.account(account_master)", 'magenta')
    account_alice = eosf.account(account_master)
    assert(not account_alice.error)
    wallet.import_key(account_alice)

    cprint("account_carol = eosf.account(account_master)", 'magenta')
    account_carol = eosf.account(account_master)
    assert(not account_carol.error)
    wallet.import_key(account_carol) 

    cprint(
        """contract.push_action("hi", '{"user":"' + str(account_alice) + '"}', account_alice)""", 'magenta')
    assert(not contract.push_action(
        "hi", '{"user":"' + str(account_alice) + '"}', account_alice, output=True).error)

    cprint(
        """contract.push_action("hi", '{"user":"' + str(account_carol) + '"}', account_carol)""", 'magenta')
    assert(not contract.push_action(
        "hi", '{"user":"' + str(account_carol) + '"}', account_carol, output=True).error)

    testnet = node.stop()
    assert(not testnet.error)
    cprint(
        "Closed the local testnet: {}".format(not testnet.error), 'magenta')


if __name__ == "__main__":
    test()
