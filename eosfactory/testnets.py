import argparse
import eosfactory.core.testnet as testnet

def main():
    '''
    usage: testnets.py [-h] [--name NAME] [--remove]

    List saved testnets.

    Args:
        --name: print a testent of the given name
        --remove: remove a testent of the given name
        -h: show help message and exit
    '''
    parser = argparse.ArgumentParser(description='''
    List saved testnets.
    ''')

    parser.add_argument(
        "--name", help="The name of the testnet chosen.", default="")
    parser.add_argument(
        "--remove", help="Remove testnet of the given name.", 
        action="store_true")        
    args = parser.parse_args()
    if args.name:
        print(testnet.get_testnet(args.name, raise_exception=False))
        if args.remove:
            testnet.remove_from_mapping(args.name)
            testnet.testnets()
    else:
        testnet.testnets()

if __name__ == '__main__':
    main()    