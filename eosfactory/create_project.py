#!/usr/bin/env python3
"""Create a new project from a template
====================================
"""

import argparse
from argparse import RawTextHelpFormatter
from eosfactory.core.teos import project_from_template 

def main():
    """
    usage::
    
        python3 -m eosfactory.create_project [-h] [--vsc] [--throw] [--ovr] [--silent] name [template]

    Given a workspace name and (optional) a template name, create a new
    workspace, compatible with Visual Studio Code.
    
    If the project directory is not specified, use the contract workspace
    directory (given with the command ``python3 -m eosfactory.config`` with the
    ``EOSIO_CONTRACT_WORKSPACE`` field in the result, or set with the command
    ``python3 -m eosfactory.config --workspace``).

    If the template directory is not specified, use a default one. If the
    template name is not specified, use the template ``empty_project``.

    Example command line, resulting with a contract project in the contract
    workspace directory, derived from the template ``empty_project``. Finally
    it opens a new VSCode window with the new project in it::

        python3 -m eosfactory.create_project foo2 --vsc

    Args:
        name: Project name or directory.
        template: Template name or directory.
        --c_cpp_prop: c_cpp_properties.json file path.
        --includes: Comma-separated list of additional include folders.
        --libs: Comma-separated list of additional libraries.
        --vsc: Open Visual Studio Code.
        --throw: Throw error if the project exists.
        --ovr: Overwrite any existing project.
        --silent: Do not print info.
        -h: Show help message and exit        
    """
    parser = argparse.ArgumentParser(description="""
Given a workspace name and (optional) a template name, create a new 
workspace, compatible with Visual Studio Code.

If the project directory is not specified, use the contract workspace 
directory (given with the command ``python3 -m eosfactory.config`` 
with the ``EOSIO_CONTRACT_WORKSPACE`` field in the result, or set with the 
``command python3 -m eosfactory.config --workspace``).

If the template directory is not specified, use a default one. If 
the template name is not specified, use the template ``empty_project``.

Example command line, resulting with a contract project in the contract 
workspace directory, derived from the template ``empty_project``. Finally 
it opens a new VSCode window with the new project in it:

    python3 -m eosfactory.create_project foo2 --vsc
    """, formatter_class=RawTextHelpFormatter)

    parser.add_argument("name", help="Project name or directory.")
    parser.add_argument(
        "template", nargs="?", help="Template name or directory.", 
        default="empty_project")
    parser.add_argument(
        "--includes", help="Comma-separated list of includes folders", default="")
    parser.add_argument(
        "--libs", help="Comma-separated list of libraries.", default="")    
    parser.add_argument(
        "--vsc", help="Open Visual Studio Code.", action="store_true")
    parser.add_argument(
        "--throw", help="Throw error if the project exists.", action="store_true")
    parser.add_argument(
        "--ovr", help="Overwrite any existing project.", action="store_true")
    parser.add_argument(
        "--silent", help="Do not print info.", action="store_true")

    args = parser.parse_args()

    project_from_template(
        project_name=args.name, 
        template=args.template,
        includes=args.includes,
        libs=args.libs,
        open_vscode=args.vsc,
        throw_exists=args.throw, remove_existing=args.ovr,
        verbosity=[] if args.silent else None
        )

if __name__ == '__main__':
    main()
