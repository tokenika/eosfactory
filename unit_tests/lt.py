import sys
import eosfactory.core.setup as setup
setup.set_is_lt()
import eosfactory.core.eosjs.base as js
from eosfactory.eosf import *


setup.is_print_command_lines = True

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
    create_account("ALICE", MASTER)
    ALICE.info()

    # create_account("CAROL", MASTER)
    # create_account("BOB", MASTER)


if __name__ == "__main__":
    test()