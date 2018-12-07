import argparse
from eosfactory.core.teos import project_from_template 

parser = argparse.ArgumentParser(description='''
Given a workspace name and a template name (optional),
create a new workspace, compatible with Visual Studio Code.

Example:
    python3 -m eosfactory.utils.create_project contract.name 01_hello_world
''')

parser.add_argument("name", help="Project name or directory.")
parser.add_argument(
    "template", nargs="?", help="Template name or directory.", 
    default="01_hello_world")
parser.add_argument(
    "--c_cpp_prop_path", help="Path to a c_cpp_prop file.", default="")
parser.add_argument(
    "--vsc", help="Open Visual Studio Code.", action="store_true")
parser.add_argument(
    "--throw", help="Throw error if the project exists.", action="store_true")
parser.add_argument(
    "--ovr", help="Overwrite any existing project.", action="store_true")
parser.add_argument(
    "--silent", help="Do not print info.", action="store_true")

args = parser.parse_args()

# with open("/mnt/c/Workspaces/EOS/eosfactory/log.txt", "a") as log:
#     import sys
#     log.write(str(sys.argv) + "\n")
#     log.write(str(args) + "\n")

project_from_template(
    args.name, template=args.template, 
    c_cpp_prop_path=args.c_cpp_prop_path,
    open_vscode=args.vsc,
    throw_exists=args.throw, remove_existing=args.ovr,
    verbosity=[] if args.silent else None
    )
