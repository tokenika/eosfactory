#!/usr/bin/env python3
"""Edit an account mapping file
============================================
"""

import argparse
from argparse import RawTextHelpFormatter
import eosfactory.core.utils as utils
import eosfactory.core.errors as errors
import eosfactory.core.setup as setup

TEXT_EDITOR = "nano"

def main():
    """
    usage::

        python3 -m eosfactory.edit_account_map [-h] [-p PREFIX] url [text_editor]

    Args:
        url: An URL of a node offering access to the testnet.
        text_editor:Text editor to be used.
        -h, --help: Show a help message and exit.
        -p PREFIX, --prefix PREFIX: A prefix prependend to the default file name.
    """

    parser = argparse.ArgumentParser(description="""""")
    parser.add_argument(
                "url",
                help="An URL of a node offering access to the testnet.")
    parser.add_argument(
                "text_editor", nargs="?", default=TEXT_EDITOR,
                help="Text editor to be used.")
    parser.add_argument(
                "-p", "--prefix",
                default=None,
                help="A prefix prependend to the default file name.")

    args = parser.parse_args()
    if args.text_editor == TEXT_EDITOR:
        (_, error) = utils.spawn(
                        [TEXT_EDITOR, "--version"], raise_exception=False)
        if error:
            raise errors.Error(
        """
The default editor ``{}`` is not available.
The error message is 
{}
Set another editor as the second argument in the command line.
        """.format(TEXT_EDITOR, error), translate=False
        )

    setup.edit_account_map(args.url, text_editor=args.text_editor)


if __name__ == '__main__':
    main()


# python3 -m eosfactory.edit_account_map http://145.239.133.201:8888