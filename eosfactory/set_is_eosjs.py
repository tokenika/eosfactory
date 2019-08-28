#!/usr/bin/env python3
"""Set testnet interface."""

import argparse
import eosfactory.core.config as config
import eosfactory.core.checklist as checklist

def main():
    parser = argparse.ArgumentParser(description="""
    Set testnet interface.

    The testnet interface can be either ``cleos`` or ``eosio``. The former is more comprehensive than the latter which does not have any local testnet and it doesnot build contracts.

    However, the latter interface does not need the heavy local installations of both ``eos`` and ``eosio.cdt``. Instead, it uses the ``eosjs`` node package.
    """)
    parser.add_argument(
                    "--is_cleos", help="If set, use the ``cleos`` interface.", 
                    action="store_true")

    args = parser.parse_args()

    check = checklist.Checklist(
        interface_package=config.CLEOS_PACKAGE if args.is_cleos \
                                                    else config.EOSJS_PACKAGE)
    if not check.is_error and not check.is_warning:
        print("... all the dependencies are in place.\n\n")
    else:
        print(
"""Some functionalities of EOSFactory may fail if the indicated errors are not 
corrected.
""")
    config.set_is_eosjs(not args.is_cleos)


if __name__ == '__main__':
    main()
