#!/usr/bin/python3

"""
Commands controlling an EOS node.

.. module:: node
    :platform: Unix, Windows
    :synopsis: Commands controlling an EOS node.

.. moduleauthor:: Tokenika

"""

import teos
import cleos

def reset():
    """
    Reset and start a local EOS node.
    On error, return false.
    """
    teos.NodeStart(1)
    probe = teos.NodeProbe()
    return probe.error


def run():
    """
    Restart a local EOS node.
    On error, return false.
    """
    teos.NodeStart(0)
    probe = teos.NodeProbe()
    return probe.error


def stop():
    """
    Stop a local EOS node. 
    """
    return teos.NodeStop()


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
        head_block_num = int(pyteos.GetInfo(False).json["head_block_num"])
    except:
        head_block_num = -1
    return head_block_num > 0
