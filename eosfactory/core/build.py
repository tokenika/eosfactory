import argparse
import eosfactory.core.teos as teos

def build(
        contract_dir_hint, c_cpp_properties_path=None, 
        compile_only=False, silent=False):

    verbosity=[] if args.silent else None
    if not compile_only:
        teos.ABI(contract_dir_hint, c_cpp_properties_path, verbosity)
    teos.WAST(contract_dir_hint, c_cpp_properties_path, compile_only, verbosity)

parser = argparse.ArgumentParser(description='''
Given a workspace name and a template name (optional),
create a new workspace, compatible with Visual Studio Code.

Example:
    python3 -m eosfactory.utils.create_project contract.name 01_hello_world
''')

parser.add_argument("dir", help="Contract name or directory.")
parser.add_argument("depend", nargs="?", help="Dependencies of the build.",
    default="")
parser.add_argument(
    "--compile", help="Do not build, compile only.", action="store_true")
parser.add_argument(
    "--silent", help="Do not print info.", action="store_true")


args = parser.parse_args()
build(args.dir, args.depend, args.compile, args.silent)

