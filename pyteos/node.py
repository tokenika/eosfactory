#!/usr/bin/python3

"""
Private testnet set-up and tear-down.

.. module:: node
    :platform: Unix, Windows
    :synopsis: Private testnet set-up and tear-down.

.. moduleauthor:: Tokenika

"""

import teos
import cleos


def reset(is_verbose=1):
    """ Start clean the EOSIO local node.

    Return: `True` if `GeiInfo()` call is successful, otherwise `False`.
    """
    node = teos.NodeStart(1, is_verbose)
    # print("XXXXXXXXXXXXX teos.NodeStart(1, is_verbose)")
    cleos.set_wallet_url_arg(node, node.json["EOSIO_DAEMON_ADDRESS"], True)
    # print("XXXXXXXXXXXXX teos.NodeStart(1, is_verbose)")

    probe = teos.NodeProbe(is_verbose)
    if not probe.error:
        if node.is_verbose:
            print("OK")
    return probe


def run(is_verbose=1):
    """ Restart the EOSIO local node.

    Return: `True` if `GeiInfo()` call is successful, otherwise `False`.
    """
    node = teos.NodeStart(0, is_verbose)
    cleos.set_wallet_url_arg(node, node.json["EOSIO_DAEMON_ADDRESS"], True)
    probe = teos.NodeProbe(is_verbose)
    if not probe.error:
        if node.is_verbose:
            print("OK")
    return probe


def stop(is_verbose=1):
    """ Stops all running EOSIO nodes and empties the local `nodeos` wallet 
    directory.

    Return: True if no running nodes and the local `nodeos` wallet directory 
    is empty, otherwise `False`.
    """
    stop = teos.NodeStop(is_verbose)
    cleos.set_wallet_url_arg(stop, "")
    return stop


def info():
    """
    Display EOS node status.
    """
    return cleos.GetInfo()


def is_running():
    """
    Check if testnet is running.
    """
    try:
        head_block_num = int(cleos.GetInfo(0).json["head_block_num"])
    except:
        head_block_num = -1
    return head_block_num > 0
