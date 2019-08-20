#!/usr/bin/env python3
"""Test example."""

import argparse, sys, time
import eosfactory.core.setup as setup
#setup.set_is_lt()
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE])

CONTRACT_WORKSPACE = sys.path[0] + "/../contracts/tic_tac_toe"

INITIAL_RAM_KBYTES = 8
INITIAL_STAKE_NET = 3
INITIAL_STAKE_CPU = 3

# Actors of the test:
MASTER = MasterAccount()
HOST = Account()
ALICE = None
CAROL = None

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


def test(testnet, reset):
    SCENARIO("""
    There is the ``MASTER`` account that sponsors the ``HOST``
    account equipped with an instance of the ``tic_tac_toe`` smart contract. There
    are two players ``ALICE`` and ``CAROL``. We are testing that the moves of
    the game are correctly stored in the blockchain database.
    """)

    if reset:
        manager.reset(testnet)
    else:
        manager.resume(testnet)
    
    create_master_account("MASTER", testnet)
    create_account("HOST", MASTER,
        buy_ram_kbytes=INITIAL_RAM_KBYTES, stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)
    create_account("ALICE", MASTER,
        buy_ram_kbytes=INITIAL_RAM_KBYTES, stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)
    create_account("CAROL", MASTER,
        buy_ram_kbytes=INITIAL_RAM_KBYTES, stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)

    stats()

    smart = Contract(HOST, CONTRACT_WORKSPACE)
    smart.build(force=False)

    try:
        smart.deploy(payer=MASTER)
    except errors.ContractRunningError:
        pass

    COMMENT("""
    Attempting to create a new game.
    This might fail if the previous game has not been closes properly:
    """)
    try:
        HOST.push_action(
            "create",
            {
                "challenger": ALICE,
                "host": CAROL
            },
            permission=(CAROL, Permission.ACTIVE))
    except Error as e:
        if "game already exists" in e.message:
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
            raise Error(str(e))

    table = HOST.table("games", CAROL)
    assert(table.json["rows"][0]["board"][0] == 0)
    assert(table.json["rows"][0]["board"][1] == 0)
    assert(table.json["rows"][0]["board"][2] == 0)
    assert(table.json["rows"][0]["board"][3] == 0)
    assert(table.json["rows"][0]["board"][4] == 0)
    assert(table.json["rows"][0]["board"][5] == 0)
    assert(table.json["rows"][0]["board"][6] == 0)
    assert(table.json["rows"][0]["board"][7] == 0)
    assert(table.json["rows"][0]["board"][8] == 0)

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
    assert(table.json["rows"][0]["board"][0] == 1)
    assert(table.json["rows"][0]["board"][1] == 0)
    assert(table.json["rows"][0]["board"][2] == 0)
    assert(table.json["rows"][0]["board"][3] == 0)
    assert(table.json["rows"][0]["board"][4] == 2)
    assert(table.json["rows"][0]["board"][5] == 0)
    assert(table.json["rows"][0]["board"][6] == 0)
    assert(table.json["rows"][0]["board"][7] == 0)
    assert(table.json["rows"][0]["board"][8] == 0)

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
    assert(table.json["rows"][0]["board"][0] == 0)
    assert(table.json["rows"][0]["board"][1] == 0)
    assert(table.json["rows"][0]["board"][2] == 0)
    assert(table.json["rows"][0]["board"][3] == 0)
    assert(table.json["rows"][0]["board"][4] == 0)
    assert(table.json["rows"][0]["board"][5] == 0)
    assert(table.json["rows"][0]["board"][6] == 0)
    assert(table.json["rows"][0]["board"][7] == 0)
    assert(table.json["rows"][0]["board"][8] == 0)

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

    stop()
    stats()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""
    This is a unit test for the ``tic-tac-toe`` smart contract.
    It works both on a local testnet and remote testnet.
    The default option is local testnet.
    """)

    parser.add_argument(
        "alias", nargs="?",
        help="Testnet alias")

    parser.add_argument(
        "-table", "--testnet", nargs=4,
        help="<url> <name> <owner key> <active key>")

    parser.add_argument(
        "-r", "--reset", action="store_true",
        help="Reset testnet cache")

    args = parser.parse_args()
    test(get_testnet(args.alias, args.testnet), reset=args.reset)
