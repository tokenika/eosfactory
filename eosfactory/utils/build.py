import argparse
import eosfactory.core.teos as teos

def build_(
        contract_dir_hint, compile_only=False, silent=False):

    verbosity=[] if silent else None
    if not compile_only:
        teos.ABI(contract_dir_hint, None, verbosity)
    teos.WASM(contract_dir_hint, None, compile_only, verbosity)

def build():
    '''
    usage: python3 -m eosfactory.utils.build [-h] [--compile] [--silent] dir

    Given a contract project directory path which may be relative to the
    ``contract workspace`` directory, set on the installation.

    Args:
        dir: Contract name or directory.
        -h: Show help message and exit
        --compile: Do not build, compile only.
        --silent: Do not print info.
    '''
    parser = argparse.ArgumentParser(description='''
    Given a contract project directory path which may be relative to the 
    ``contract workspace`` directory, set on the installation.
    ''')

    parser.add_argument("dir", help="Contract name or directory.")
    parser.add_argument(
        "--compile", help="Do not build, compile only.", action="store_true")
    parser.add_argument(
        "--silent", help="Do not print info.", action="store_true")


    args = parser.parse_args()
    build_(args.dir, args.compile, args.silent)    

if __name__ == '__main__':
    build()
