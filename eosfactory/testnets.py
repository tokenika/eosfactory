import argparse
import eosfactory.core.testnet as testnet

def main():
    '''
    usage: python3 -m eosfactory.testnets [-h]

    List saved testnets.

    Args:
        --name: 
        -h: show help message and exit
    '''
    parser = argparse.ArgumentParser(description='''
    List saved testnets.
    ''')

    parser.add_argument(
        "--name", help="The name of the testnet chosen.", default="")
    args = parser.parse_args()
    if args.name:
        print(testnet.get_testnet(args.name, raise_exception=False))
    else:
        testnet.testnets()

if __name__ == '__main__':
    main()    