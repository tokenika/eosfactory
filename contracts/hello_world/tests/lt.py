#!/usr/bin/env python3
""""""
import sys

import eosfactory.core.setup as setup
setup.set_is_eosjs()
from eosfactory.eosf import *

import importlib
BASE_COMMANDS = importlib.import_module(".base", setup.interface_package())
GET_COMMANDS = importlib.import_module(".get", setup.interface_package())
SET_COMMANDS = importlib.import_module(".set", setup.interface_package())
SYS_COMMANDS = importlib.import_module(".sys", setup.interface_package())


# setup.IS_PRINT_COMMAND_LINES = True

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_WORKSPACE = sys.path[0] + "/../"

# Actors of the test:
MASTER = Account()
HOST = Account()
ALICE = Account()
CAROL = Account()

def test():
    
    SCENARIO("""
    Execute simple actions.
    """)
   

    reset()
    create_master_account("MASTER")
    # setup.IS_PRINT_REQUEST = True
    # setup.IS_PRINT_RESPONSE = True
    # setup.IS_PRINT_COMMAND_LINES = True
    # setup.IS_PRINT_COMMAND_LINES = True

    create_account("ALICE", MASTER)
    create_account("HOST", MASTER)

    setup.IS_PRINT_REQUEST = False
    setup.IS_PRINT_RESPONSE = False
    
    COMMENT("ALICE.info()")
    ALICE.info()
    COMMENT("get.GetBlock(6)")
    GET_COMMANDS.GetBlock(6)
    COMMENT("get.GetBlock(6)")
    GET_COMMANDS.GetAccounts(ALICE.active_public())
    smart = Contract(HOST, CONTRACT_WORKSPACE)
    smart.deploy()
    create_account("CAROL", MASTER)

    COMMENT("""
    Test an action for Alice:
    """)
    setup.IS_PRINT_COMMAND_LINES = False
    HOST.push_action(
        "hi", {"user":ALICE}, permission=(ALICE, Permission.ACTIVE))

    assert "ALICE" in DEBUG()
    

if __name__ == "__main__":
    test()
    stop()