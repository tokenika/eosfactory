#!/usr/bin/python3

'''
Private testnet set-up and tear-down.

.. module:: pyteos
    :platform: Unix, Windows
    :synopsis: Private testnet set-up and tear-down.

.. moduleauthor:: Tokenika

'''

import eosf

def reset(verbosity=None):
    ''' Start clean the EOSIO local node.

    Return: `True` if `GeiInfo()` call is successful, otherwise `False`.
    '''
    eosf.reset(verbosity)

def run(verbosity=None):
    ''' Restart the EOSIO local node.

    Return: `True` if `GeiInfo()` call is successful, otherwise `False`.
    '''
    eosf.run(verbosity)

def stop(verbosity=None):
    ''' Stops all running EOSIO nodes and empties the local `nodeos` wallet 
    directory.

    Return: True if no running nodes and the local `nodeos` wallet directory 
    is empty, otherwise `False`.
    '''
    eosf.stop(verbosity)

def info():
    '''
    Display EOS node status.
    '''
    return cleos.GetInfo()

def node_is_operative():
    '''
    Check if testnet is running.
    '''
    try:
        head_block_num = int(cleos.GetInfo(0).json["head_block_num"])
    except:
        head_block_num = -1
    return head_block_num > 0
