import sys

import eosfactory.core.setup as setup
setup.set_is_lt()
from eosfactory.eosf import *

import importlib
base_commands = importlib.import_module(".base", setup.light_full)
get_commands = importlib.import_module(".get", setup.light_full)
set_commands = importlib.import_module(".set", setup.light_full)
sys_commands = importlib.import_module(".sys", setup.light_full)


# setup.is_print_command_lines = True

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_WORKSPACE = sys.path[0] + "/../"

# Actors of the test:
MASTER = MasterAccount()
HOST = Account()
ALICE = Account()
CAROL = Account()

def test():
    
    SCENARIO('''
    Execute simple actions.
    ''')
   

    reset()
    create_master_account("MASTER")
    # setup.is_print_request = True
    # setup.is_print_response = True
    # setup.is_print_command_lines = True
    # setup.is_print_command_lines = True

    create_account("ALICE", MASTER)
    create_account("HOST", MASTER)

    setup.is_print_request = False
    setup.is_print_response = False
    
    COMMENT("ALICE.info()")
    ALICE.info()
    COMMENT("get.GetBlock(6)")
    get_commands.GetBlock(6)
    COMMENT("get.GetBlock(6)")
    get_commands.GetAccounts(ALICE.active_public())
    smart = Contract(HOST, CONTRACT_WORKSPACE)
    smart.deploy()
    create_account("CAROL", MASTER)

    COMMENT('''
    Test an action for Alice:
    ''')
    setup.is_print_command_lines = True
    HOST.push_action(
        "hi", {"user":ALICE}, permission=(ALICE, Permission.ACTIVE))
    assert("ALICE" in DEBUG())
    

if __name__ == "__main__":
    test()
    stop()
    sys.exit(0)