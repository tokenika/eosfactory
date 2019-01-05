import argparse
from eosfactory.core.teos import project_from_template 

def create_project():
    '''
    usage: python3 -m eosfactory.utils.create_project [-h] [--vsc]
                            [--throw] [--ovr] [--silent]
                            name [template]

    Given a workspace name and (optional) a template name, create a new 
    workspace, compatible with Visual Studio Code.

    Args:
        name: Project name or directory.
        template: Template name or directory.
        -h: Show help message and exit
        --vsc: Open Visual Studio Code.
        --throw: Throw error if the project exists.
        --ovr: Overwrite any existing project.
        --silent: Do not print info.
    '''
    parser = argparse.ArgumentParser(description='''
    Given a workspace name and (optional) a template name,
    create a new workspace, compatible with Visual Studio Code.
    ''')

    parser.add_argument("name", help="Project name or directory.")
    parser.add_argument(
        "template", nargs="?", help="Template name or directory.", 
        default="01_hello_world")
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
        args.name, template=args.template, 
        open_vscode=args.vsc,
        throw_exists=args.throw, remove_existing=args.ovr,
        verbosity=[] if args.silent else None
        )

if __name__ == '__main__':
    create_project()
