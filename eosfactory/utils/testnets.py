import argparse
import eosfactory.core.testnet as testnet

def testnets():
    '''
    usage: python3 -m eosfactory.utils.testnets [-h]

    List saved testnets.

    Args:
        -h: show help message and exit
    '''
    parser = argparse.ArgumentParser(description='''
    List saved testnets.
    ''')

    args = parser.parse_args()
    testnet.testnets()

if __name__ == '__main__':
    testnets()    