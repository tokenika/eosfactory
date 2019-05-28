import os
import re
import fnmatch
import shutil
import zipfile
import argparse

import eosfactory.core.utils as utils
import eosfactory.core.config as config
import eosfactory.core.logger as logger
import eosfactory.core.errors as errors
import eosfactory.core.vscode as vscode

# https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/EOSIO/eosio.cdt/tree/master/examples/hello

EOSIO_CDT_INCLUDE = r".*\s+\"(.*/eosio\.cdt/\d\.\d\.\d/.*)include.*"
EOSIO_CDT_HOME = '${eosio_cdt_home}'


def create_ignore_list_file(contract_dir, is_log_creation=False):
    ignore_file = os.path.join(contract_dir, config.IGNORE_FILE)
    if not os.path.exists(ignore_file):
        if is_log_creation:
            logger.ERROR('''
                There is not any '{}' file in the project directory
                    {}
                Creating a default one.
            '''.format(config.IGNORE_FILE, contract_dir))

        with open(ignore_file, "w+") as f:
            f.write("\n".join(config.IGNORE_LIST))
                
    return ignore_file


def create_utils(contract_dir):
    UTILS_PATH = "utils"
    path_dest = os.path.join(contract_dir, UTILS_PATH)
    path_src = os.path.join(config.template_dir(), config.PROJECT_0, UTILS_PATH)
    try:
        if not os.path.exists(path_dest):
            shutil.copytree(path_src, path_dest)
    except:
        pass


def create_task_json(contract_dir):
    vscode_task_path = os.path.join(".vscode", "tasks.json")
    path_dest = os.path.join(contract_dir, vscode_task_path)
    if not os.path.exists(path_dest):
        try:
            with open(path_dest, "w+") as f:
                f.write(vscode.TASKS)
        except:
            pass


def is_valid(file, ignore_list):
    for pattern in ignore_list:
        if fnmatch.fnmatch(file, pattern):
            return False
    return True


def unpack(contract_dir=None, zip_file=None):
    '''Unack a contract project folder.

    Make a new contract project folder from a zip file produced with the 
    function :func:`pack`.

    If the given zip file is an arbitrary one, expands it with omiting files 
    matching the `config.IGNORE_LIST`, and localizes the 
    '.vscode.c_cpp_properties.json' file, if found.

    Args:
        contract_dir (str): The contract project directory to be created.
        zip_file (str): The zip file to be extracted.
    '''

    if not contract_dir:
        raise errors.Error('''
            The directory of the new contract has to be specified.
        ''')
    contract_dir = utils.wslMapWindowsLinux(contract_dir)

    if os.path.exists(contract_dir) and os.listdir(contract_dir):
        raise errors.Error('''
            The directory
                {}
            is not empty. Cannot overwrite it.
        '''.format(os.path.realpath(contract_dir)))

    if not zip_file: 
        raise errors.Error('''
            The zip file, defining the new directory, has to be specified.
        ''')

    zip_file = utils.wslMapWindowsLinux(zip_file)
    if not os.path.exists(zip_file):
        raise errors.Error('''
            The zip file
                {}
            does not exists
        '''.format(os.path.realpath(zip_file)))


    def convert_c_cpp_properties(member, zipfile_object):
        if "c_cpp_properties.json" in member.filename:
            c_cpp_properties = zipfile_object.read(member).decode("utf-8") 
            eosio_cdt_include = re.compile(EOSIO_CDT_INCLUDE)
            if re.findall(eosio_cdt_include, c_cpp_properties):
                c_cpp_properties = c_cpp_properties.replace(
                    re.findall(
                        eosio_cdt_include, c_cpp_properties)[0], 
                        EOSIO_CDT_HOME)

            eosio_cdt_root = config.wsl_root() + config.eosio_cdt_root()
            c_cpp_properties = c_cpp_properties.replace(
                                    EOSIO_CDT_HOME, eosio_cdt_root)

            if not os.path.exists(os.path.join(contract_dir, ".vscode")):
                os.makedirs(os.path.join(contract_dir, ".vscode"))

            with open(os.path.join(
                        contract_dir, member.filename), "w+") as f:
                f.write(c_cpp_properties)
            return True
        return False


    try:
        with zipfile.ZipFile(zip_file) as zf:
            info_list = zf.infolist()
            for member in info_list:
                if is_valid(member.filename, config.IGNORE_LIST):
                    if not convert_c_cpp_properties(member, zf):
                        zf.extract(member, contract_dir)

    except Exception as e:
        raise errors.Error('''
            Cannot extract the zip file
                {}
            to the directory
                {}
            The error message is
            {}
        '''.format(
            os.path.realpath(zip_file), os.path.realpath(contract_dir),
            str(e)
            ))

    create_ignore_list_file(contract_dir)
    create_utils(contract_dir)
    create_task_json(contract_dir)


def pack(contract_dir=None, zip_file=None):
    '''Pack a contract project folder.

    If an EOSIO contract project which is a VSCode folder is to be passed by 
    e-mail, it has to be compressed. However, this should not be done in 
    a straightforward way, because of the following issues:
        
        There are volume binaries there.
        There are local configuring files in the .vscode folder.
        There are your private notes and scratchpads there.
        The paths in the .vscode/c_cpp_properties.json are localized according 
        to the local operating system.

    Make compression automatically, solving the issues. 
    With default arguments, produce a zip file, in the project folder. The 
    file is named after the folder name.

    Args:
        contract_dir (str): If set, the contract project directory, otherwise cwd.
        zip_file (str): If set, the name of the zip file, 
                otherwise <project directory>/<project directory name>.zip 
    '''

    if not contract_dir:
        contract_dir = os.getcwd()
    else:
        contract_dir = utils.wslMapWindowsLinux(contract_dir)

    if not os.path.exists(contract_dir):
        raise errors.Error('''
            The given contract directory
                {}
            does not exist.
                    ''')

    if not os.path.isdir(contract_dir):
        raise errors.Error('''
            The given contract path
                {}
            is not a directory.
        ''')        
    
    if not zip_file:
        zip_file = os.path.realpath(os.path.join(
                        os.getcwd(), os.path.basename(contract_dir) + ".zip"))
    else:
        zip_file = utils.wslMapWindowsLinux(zip_file)

    if os.path.exists(zip_file):
        try:
            os.remove(zip_file)
        except Exception as e:
            raise errors.Error('''
                Cannot remove the project zip file
                    {}
                The error message is
                    {}
            '''.format(zip_file, str(e)))

    ignore_file = create_ignore_list_file(contract_dir, True)

    ignore_list = []
    with open(ignore_file, "r") as f:
        for l in f:
            line = l.strip()
            if not line[0] == "#":
                ignore_list.append(line)
    if not zip_file in ignore_list:
        ignore_list.append(zip_file)
    if not config.IGNORE_FILE in ignore_list:
        ignore_list.append(config.IGNORE_FILE)


    def convert_c_cpp_properties(path, path_rel, zipfile_object):
        if "c_cpp_properties.json" in path:
            with open(path, "r") as f:
                c_cpp_properties = f.read()
                eosio_cdt_include = re.compile(EOSIO_CDT_INCLUDE)
                if re.findall(eosio_cdt_include, c_cpp_properties):
                    c_cpp_properties = c_cpp_properties.replace(
                        re.findall(
                                    eosio_cdt_include, c_cpp_properties)[0], 
                                    EOSIO_CDT_HOME)
                print("adding {}".format(path_rel))
                zipfile_object.writestr(path_rel, c_cpp_properties)
            return True
        return False


    def project_files(search_dir, zipfile_object):
        files = []
        paths = os.listdir(search_dir)
        for file in paths:
            path = os.path.join(search_dir, file)
            if os.path.isfile(path):
                if not path == zip_file:
                    path_rel = os.path.relpath(path, contract_dir)
                    if is_valid(path_rel, ignore_list):
                        if not convert_c_cpp_properties(
                                                path, path_rel, zipfile_object):
                            print("adding {}".format(path_rel))
                            zipfile_object.write(path, path_rel)
            else:
                project_files(path, zipfile_object)


    try:
        with zipfile.ZipFile(zip_file, mode='w') as zf:
            project_files(contract_dir, zf)
    except:
        raise errors.Error('''
            Cannot zip the directory
                {}
            to the zip file
                {}
            The error message is
            {}
        '''.format(
            os.path.realpath(contract_dir), os.path.realpath(zip_file), 
            str(e)
            ))



def main():
    '''Pack or unpack a contract project folder.

    usage: pack_contract.py [-h] [--unpack] [--dir DIR] [--zip ZIP] 

    If an EOSIO contract project which is a VSCode folder is to be passed by 
    e-mail, it has to be compressed. However, this should not be done in 
    a straightforward way, because of the following issues:
        
        There are volume binaries there.
        There are local configuring files in the .vscode folder.
        There are your private notes and scratchpads there.
        The paths in the .vscode/c_cpp_properties.json are localized according 
        to the local operating system.

    This is a tool that makes the compression -- and decompression -- 
    automatically solving the issues. 
    It produces a zip file, in the project folder. The file is named after the folder name.

    Args:
        --unpack: If set, unpack.
        --dir: If set, the contract project directory, otherwise cwd.
        --zip: If set, the name of the zip file, otherwise 
                <project directory>/<project directory name>.zip    
    '''

    parser = argparse.ArgumentParser(description='''
    Pack or unpack a contract project folder.

    If an EOSIO contract project which is a VSCode folder is to be passed by 
    e-mail, it has to be compressed. However, this should not be done in 
    a straightforward way, because of the following issues:
        
        There are volume binaries there.
        There are local configuring files in the .vscode folder.
        There are your private notes and scratchpads there.
        The paths in the .vscode/c_cpp_properties.json are localized according 
        to the local operating system.

    This is a tool that makes the compression -- and decompression -- 
    automatically solving the issues. 
    It produces a zip file, in the project folder. The file is named after the folder name.
    ''')

    parser.add_argument(
                        "--unpack", help="Unpack the project.", 
                        action="store_true")    
    parser.add_argument("--dir", help="Contract directory.", default="")
    parser.add_argument("--zip", help="Zip file.", default="")


    args = parser.parse_args()
    if args.unpack:
        unpack(args.dir, args.zip)
    else:
        pack(args.dir, args.zip)


if __name__ == "__main__":
    main()

