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
    Reset and start a local EOSIO node.
    """
    pyteos.node_reset()

def stop():
    """
    Stop a local EOSIO node. 
    """
    pyteos.node_stop()

def run():
    """
    Restart a local EOSIO node.
    """
    pyteos.node_run()

def info():
    """
    Display EOSIO node status.
    """
    pyteos.node_info()