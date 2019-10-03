#!/usr/bin/env python3
"""Test example."""

import sys
import time
import importlib
import argparse

import eosfactory.core.setup as setup
# Set the interface configuration (CLEOS or EOSJS):
# setup.set_is_eosjs(False)
setup.set_is_eosjs()

from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE])

CONTRACT_WORKSPACE = sys.path[0] + "/../contracts/tic_tac_toe"

INITIAL_RAM_KBYTES = 3
INITIAL_STAKE_NET = 3
INITIAL_STAKE_CPU = 3

# Actors of the test:
MASTER = Account()
HOST = Account()
ALICE = Account()
CAROL = Account()

def stats():
    print_stats(
        [MASTER, HOST, ALICE, CAROL],
        [
            "core_liquid_balance",
            "ram_usage",
            "ram_quota",
            "total_resources.ram_bytes",
            "self_delegated_bandwidth.net_weight",
            "self_delegated_bandwidth.cpu_weight",
            "total_resources.net_weight",
            "total_resources.cpu_weight",
            "net_limit.available",
            "net_limit.max",
            "net_limit.used",
            "cpu_limit.available",
            "cpu_limit.max",
            "cpu_limit.used"
        ]
    )


def test(testnet, reset_testnet):
    SCENARIO("""
    There is the ``MASTER`` account that sponsors the ``HOST``
    account equipped with an instance of the ``tic_tac_toe`` smart contract. There
    are two players ``ALICE`` and ``CAROL``. We are testing that the moves of
    the game are correctly stored in the blockchain database.
    """)
    if reset_testnet:
        reset(testnet)
    else:
        resume(testnet)

    create_master_account("MASTER", testnet)

    MASTER.info()

    create_account(
        "HOST", MASTER,
        ram_kbytes=INITIAL_RAM_KBYTES, 
        stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)
    create_account(
        "ALICE", MASTER,
        ram_kbytes=INITIAL_RAM_KBYTES, 
        stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)
    create_account(
        "CAROL", MASTER,
        ram_kbytes=INITIAL_RAM_KBYTES, 
        stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)
    CAROL.info()

    stats()

    smart = Contract(HOST, CONTRACT_WORKSPACE)
    smart.build(force=False)

    if not HOST.is_code():
        smart.deploy(payer=MASTER)
        MASTER.info()

    COMMENT("""
    Attempting to create a new game.
    This might fail if the previous game has not been closes properly:
    """)
    try:
        setup.IS_PRINT_COMMAND_LINES = True
        HOST.push_action(
            "create",
            {
                "challenger": ALICE,
                "host": CAROL
            },
            permission=(CAROL, Permission.ACTIVE))
    except Error as ex:
        if "game already exists" in ex.message:
            COMMENT("""
            We need to close the previous game before creating a new one:
            """)
            HOST.push_action(
                "close",
                {
                    "challenger": ALICE,
                    "host": CAROL
                },
                permission=(CAROL, Permission.ACTIVE))

            time.sleep(3)

            COMMENT("""
            Second attempt to create a new game:
            """)
            HOST.push_action(
                "create",
                {
                    "challenger": ALICE, 
                    "host": CAROL
                },
                permission=(CAROL, Permission.ACTIVE))
        else:
            COMMENT("""
            The error is different than expected.
            """)
            raise Error(str(ex))

    table = HOST.table("games", CAROL)
    assert table.json["rows"][0]["board"][0] == 0
    assert table.json["rows"][0]["board"][1] == 0
    assert table.json["rows"][0]["board"][2] == 0
    assert table.json["rows"][0]["board"][3] == 0
    assert table.json["rows"][0]["board"][4] == 0
    assert table.json["rows"][0]["board"][5] == 0
    assert table.json["rows"][0]["board"][6] == 0
    assert table.json["rows"][0]["board"][7] == 0
    assert table.json["rows"][0]["board"][8] == 0

    COMMENT("""
    First move is by CAROL:
    """)
    HOST.push_action(
        "move",
        {
            "challenger": ALICE,
            "host": CAROL,
            "by": CAROL,
            "row":0, "column":0
        },
        permission=(CAROL, Permission.ACTIVE))

    COMMENT("""
    Second move is by ALICE:
    """)
    HOST.push_action(
        "move",
        {
            "challenger": ALICE,
            "host": CAROL,
            "by": ALICE,
            "row":1, "column":1
        },
        permission=(ALICE, Permission.ACTIVE))

    table = HOST.table("games", CAROL)
    assert table.json["rows"][0]["board"][0] == 1
    assert table.json["rows"][0]["board"][1] == 0
    assert table.json["rows"][0]["board"][2] == 0
    assert table.json["rows"][0]["board"][3] == 0
    assert table.json["rows"][0]["board"][4] == 2
    assert table.json["rows"][0]["board"][5] == 0
    assert table.json["rows"][0]["board"][6] == 0
    assert table.json["rows"][0]["board"][7] == 0
    assert table.json["rows"][0]["board"][8] == 0

    COMMENT("""
    Restarting the game:
    """)
    HOST.push_action(
        "restart",
        {
            "challenger": ALICE,
            "host": CAROL,
            "by": CAROL
        }, 
        permission=(CAROL, Permission.ACTIVE))

    table = HOST.table("games", CAROL)
    assert table.json["rows"][0]["board"][0] == 0
    assert table.json["rows"][0]["board"][1] == 0
    assert table.json["rows"][0]["board"][2] == 0
    assert table.json["rows"][0]["board"][3] == 0
    assert table.json["rows"][0]["board"][4] == 0
    assert table.json["rows"][0]["board"][5] == 0
    assert table.json["rows"][0]["board"][6] == 0
    assert table.json["rows"][0]["board"][7] == 0
    assert table.json["rows"][0]["board"][8] == 0

    COMMENT("""
    Closing the game:
    """)

    HOST.push_action(
        "close",
        {
            "challenger": ALICE,
            "host": CAROL
        },
        permission=(CAROL, Permission.ACTIVE))

    COMMENT("""
    ################################################################################
    ################################################################################
    Demonstrate varies properties of the ``Account`` object.
    """)

    # COMMENT("""
    # Show all actions with ALICE referenced in authorization or receiver:
    # """)
    # ALICE.actions()

    COMMENT("""
    Retrieve the code and ABI for the account HOST:
    """)
    HOST.code() # abi="xxx.abi", code="xxx.wasm")

    COMMENT("""
    Show all accounts associated with the active key of ALICE:
    """)

    # importlib.import_module(".get", setup.interface_package())
    # returns a ``eosfactory.core.cleos.get`` or ``eosfactory.core.eosjs.get``
    # module, depending on the interface configuration (CLEOS or EOSJS) 
    # set with ``setup.set_is_eosjs()``

    importlib.import_module(".get", setup.interface_package()).\
                                        GetAccounts(ALICE.active_key.key_public)
    COMMENT("""
    Buy RAM for ALICE:
    """)
    stats()
    MASTER.buy_ram(ALICE, ram_kbytes=1)
    stats()

    COMMENT("""
    Delegate bandwidth to MASTER from himself:
    """)
    MASTER.delegate_bw(stake_net_quantity=1, stake_cpu_quantity=1)

    stop()


def main():
    parser = argparse.ArgumentParser(description="""
    This is a unit test for the ``tic-tac-toe`` smart contract.
    It works both on a local testnet and remote testnet.
    The default option is local testnet.
    """)

    parser.add_argument(
        "alias", nargs="?",
        help="Testnet name or its url.")

    parser.add_argument(
        "-t", "--testnet", nargs=4,
        help="<account name> <owner key> <active key> <url>")

    parser.add_argument(
        "-r", "--reset", action="store_true",
        help="Reset testnet cache.")

    args = parser.parse_args()
    test(get_testnet(args.alias, args.testnet), reset_testnet=args.reset)


if __name__ == '__main__':
    main()

# python3 ./tests/tic_tac_toe.py http://145.239.133.201:8888
# python3 ./tests/tic_tac_toe.py JUNGLE
# python3 ./tests/tic_tac_toe.py -t 5jejduh2w2cb 5KGVA3efMr4rZEWUxWQzD4k11sApFrjYwVYfsVqvBYge1AppHdh 5KAkkZLZVQbhJL6JnxodcBScgLi1LNv8yEX5LRXaWvXyoH87DK8 http://145.239.133.201:8888