#!/usr/bin/python3

"""
Session initiation and storage for session elements.

.. module:: node
    :platform: Unix, Windows
    :synopsis: Session initiation and storage for session elements.

.. moduleauthor:: Tokenika

"""

import teos


def reset(is_verbose=1):
    """ Start clean the EOSIO local node.

    Return: `True` if `GeiInfo()` call is successful, otherwise `False`.
    """
    node = teos.NodeStart(1, is_verbose)
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
    return stop
