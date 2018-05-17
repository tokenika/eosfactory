#!/usr/bin/python3

"""
Commands controlling an EOS node.

.. module:: node
    :platform: Unix, Windows
    :synopsis: Commands controlling an EOS node.

.. moduleauthor:: Tokenika

"""

import pyteos

def reset():
    """
    Reset and start a local EOS node.
    """
    pyteos.NodeStart(1)
    probe = pyteos.NodeProbe()
    return probe.get_info


def run():
    """
    Restart a local EOS node.
    """
    return pyteos.NodeStart(0)


def stop():
    """
    Stop a local EOS node. 
    """
    return pyteos.NodeStop()


def info():
    """
    Display EOS node status.
    """
    return pyteos.GetInfo()
