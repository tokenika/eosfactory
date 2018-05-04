#!/usr/bin/python3

""" 
This is a collection of commands controlling an EOS node
"""

import pyteos

def reset():
    pyteos.node_reset()

def stop():
    pyteos.node_stop()

def run():
    pyteos.node_run()