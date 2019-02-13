#!/usr/bin/python3

import os
import subprocess
import threading
import time
import re
import pathlib
import shutil
import pprint
import json
import shutil
import sys

import eosfactory.core.errors as errors
import eosfactory.core.logger as logger
import eosfactory.core.utils as utils
import eosfactory.core.setup as setup
import eosfactory.core.config as config
import eosfactory.core.vscode as vscode

TEMPLATE_NAME = "CONTRACT_NAME"
TEMPLATE_HOME = "${HOME}"
TEMPLATE_ROOT = "${ROOT}"
C_CPP_PROP = "${c_cpp_prop}"
TASK_JSON = "${tasks}"
CONFIGURATIONS = "configurations"
INCLUDE_PATH = "includePath"
BROWSE = "browse"
WORKSPACE_FOLDER = "${workspaceFolder}"
EOSIO_CPP_INCLUDE = "eosio.cdt"
EOSIO_DISPATCH = "EOSIO_DISPATCH"

def replace_templates(string): 
    home = os.environ["HOME"]
    root = ""
    if utils.is_windows_ubuntu():
        home = config.wsl_root() + home
        root = config.wsl_root()

    string = string.replace(TEMPLATE_HOME, home)
    string = string.replace(TEMPLATE_ROOT, root)
    return string                                                      


def get_c_cpp_properties(contract_dir=None, c_cpp_properties_path=None):
    if not contract_dir:
        contract_dir = os.getcwd()
    if not c_cpp_properties_path:
        c_cpp_properties_path = os.path.join(
                                contract_dir, ".vscode/c_cpp_properties.json")
    else:
        c_cpp_properties_path = utils.wslMapWindowsLinux(c_cpp_properties_path)
        if not os.path.exists(c_cpp_properties_path):
            raise errors.Error('''
                The given path to the file 'c_cpp_properties.json'
                does not exist:
                {}       
            '''.format(c_cpp_properties_path))
    
    if os.path.exists(c_cpp_properties_path):
        try:
            with open(c_cpp_properties_path, "r") as input:
                return json.loads(input.read())
        except Exception as e:
            raise errors.Error(str(e))
    else:
        return json.loads(replace_templates(vscode.c_cpp_properties()))


def ABI(
        contract_dir_hint=None, c_cpp_properties_path=None,
        verbosity=None):
    '''Given a hint to a contract directory, produce ABI file.
    '''
    contract_dir = config.contract_dir(contract_dir_hint)
    # source_files[0] is directory, source_files[1] is contents:
    contract_source_files = config.contract_source_files(contract_dir)

    source_files = []
    source_ext = [".c", ".cpp",".cxx", ".c++"]
    for file in contract_source_files[1]:
        if os.path.splitext(file)[1].lower() in source_ext:
            source_files.append(file)

    if not source_files:
        raise errors.Error('''
        The source of the contract project is empty. 
        The assumed contract dir is   
        {}
        '''.format(contract_dir))
        return

    code_name = os.path.splitext(os.path.basename(source_files[0]))[0]
    target_dir = get_target_dir(contract_source_files[0])
    target_path = os.path.normpath(
                        os.path.join(target_dir, code_name  + ".abi"))

    for file in contract_source_files[1]:
        if os.path.splitext(file)[1].lower() == ".abi":
            logger.INFO('''
            NOTE:
            An ABI exists in the source directory. Cannot overwrite it:
            {}
            Just copying it to the target directory.
            '''.format(file), verbosity)
            shutil.move(file, target_path)
            return

    command_line = [
        config.eosio_cpp(),
        "-contract=" + code_name,
        "-R=" + get_resources_dir(contract_source_files[0]),
        "-abigen",
        "-abigen_output=" + target_path]

    c_cpp_properties = get_c_cpp_properties(
                                    contract_dir, c_cpp_properties_path)
    for entry in c_cpp_properties[CONFIGURATIONS][0][INCLUDE_PATH]:
        if WORKSPACE_FOLDER in entry:
            entry = entry.replace(WORKSPACE_FOLDER, contract_dir)
            command_line.append(
                "-I=" + utils.wslMapWindowsLinux(entry))
        else:
            if not EOSIO_CPP_INCLUDE in entry:
                command_line.append(
                    "-I=" + utils.wslMapWindowsLinux(
                        strip_wsl_root(entry)))

    input_file = None
    for file in source_files:
        with open(file, 'r') as f:
            if EOSIO_DISPATCH in f.read():
                input_file = file
                break
    if not input_file:
        raise errors.Error('''
        Cannot determine the 'input file', defined as using the {} macro.
        Source files considered:
        {}
        '''.format(EOSIO_DISPATCH, source_files))

    command_line.append(input_file)

    if setup.is_print_command_line:
        print("######## command line sent to eosio-cpp:")
        print(" ".join(command_line))

    eosio_cpp(command_line, target_dir)

    logger.TRACE('''
    ABI file writen to file: 
        {}
    '''.format(target_path), verbosity)


def WASM(
        contract_dir_hint, c_cpp_properties_path=None,
        compile_only=False, verbosity=None):
    '''Produce WASM code.
    '''
    contract_dir = config.contract_dir(contract_dir_hint)
    # source_files[0] is directory, source_files[1] is contents:
    contract_source_files = config.contract_source_files(contract_dir)

    source_files = []
    source_ext = [".c", ".cpp",".cxx", ".c++"]
    for file in contract_source_files[1]:
        if os.path.splitext(file)[1].lower() in source_ext:
            source_files.append(file)

    if not source_files:
        raise errors.Error('''
        The source of the contract project is empty. 
        The assumed contract dir is   
        {}
        '''.format(contract_dir))
        return

    code_name = os.path.splitext(os.path.basename(source_files[0]))[0]
    target_dir = get_target_dir(contract_source_files[0])
    target_path = os.path.normpath(
                        os.path.join(target_dir, code_name  + ".wasm"))

    c_cpp_properties = get_c_cpp_properties(
                                        contract_dir, c_cpp_properties_path)

    command_line = [config.eosio_cpp()]

    for entry in c_cpp_properties[CONFIGURATIONS][0][INCLUDE_PATH]:
        if WORKSPACE_FOLDER in entry:
            entry = entry.replace(WORKSPACE_FOLDER, contract_dir)
            command_line.append("-I=" + utils.wslMapWindowsLinux(entry))
        else:
            if not EOSIO_CPP_INCLUDE in entry:
                command_line.append(
                    "-I=" + utils.wslMapWindowsLinux(strip_wsl_root(entry)))

    for entry in c_cpp_properties[CONFIGURATIONS][0]["libs"]:
        command_line.append(
            "-l=" + utils.wslMapWindowsLinux(strip_wsl_root(entry)))

    for entry in c_cpp_properties[CONFIGURATIONS][0]["compilerOptions"]:
        command_line.append(entry)
    
    input_file = None
    for file in source_files:
        with open(file, 'r') as f:
            if EOSIO_DISPATCH in f.read():
                input_file = file
                break
    if not input_file:
        raise errors.Error('''
        Cannot determine the 'input file', defined as using the {} macro.
        Source files considered:
        {}
        '''.format(EOSIO_DISPATCH, source_files))

    command_line.append(input_file)

    if compile_only:
        command_line.append("-c=")

    command_line.append("-o=" + target_path)

    if setup.is_print_command_line:
        print("######## command line sent to eosio-cpp:")
        print(" ".join(command_line))

    eosio_cpp(command_line, target_dir)

    if not compile_only:
        logger.TRACE('''
            WASM file writen to file: 
                {}
            '''.format(os.path.normpath(target_path)), verbosity)


def project_from_template(
        project_name, template=None, workspace_dir=None,
        c_cpp_prop_path=None,
        include=None,
        libs=None, 
        remove_existing=False, 
        open_vscode=False, throw_exists=False, 
        verbosity=None):
    '''Given the project name and template name, create a smart contract project.

    - **parameters**::

        project_name: The name of the project, or an existing path to 
            a directory.
        template: The name of the template used.
        workspace_dir: If set, the folder for the work-space. Defaults to the 
            value returned by the config.contract_workspace_dir() function.
        include: If set, comma-separated list of include folders.
        libs: If set, comma-separated list of libraries.
        remove_existing: If set, overwrite any existing project.
        visual_studio_code: If set, open the ``VSCode``, if available.
        verbosity: The logging configuration.
    '''
    project_name = utils.wslMapWindowsLinux(project_name.strip())
    template = template.strip()

    template_dir = utils.wslMapWindowsLinux(template)
    if not os.path.isdir(template_dir):
        template_dir = os.path.join(config.template_dir(), template) 
    if not os.path.isdir(template_dir):
        raise errors.Error('''
        The contract project template '{}' does not exist.
        '''.format(template_dir)) 

    if c_cpp_prop_path:
        c_cpp_prop_path = utils.wslMapWindowsLinux(c_cpp_prop_path)
        if os.path.exists(c_cpp_prop_path):
            try:
                with open(c_cpp_prop_path, "r") as input:
                    c_cpp_properties = input.read()
            except Exception:
                c_cpp_properties = vscode.c_cpp_properties()
    else:
        c_cpp_properties = vscode.c_cpp_properties()

    c_cpp_properties = replace_templates(c_cpp_properties)

    if include:
        c_cpp_properties_json = json.loads(c_cpp_properties)
        c_cpp_properties_json[CONFIGURATIONS][0][INCLUDE_PATH].extend(
                                                        include.split(", "))
        c_cpp_properties_json[CONFIGURATIONS][0][BROWSE]["path"].extend(
                                                        include.split(", "))
        c_cpp_properties = json.dumps(c_cpp_properties_json, indent=4)

    if libs:
        c_cpp_properties_json = json.loads(c_cpp_properties)
        c_cpp_properties_json[CONFIGURATIONS][0]["libs"].extend(
                                                        libs.split(", "))
        c_cpp_properties = json.dumps(c_cpp_properties_json, indent=4)


    split = os.path.split(project_name)
    if os.path.isdir(split[0]):
        project_dir = project_name
        project_name = split[1]
    else:
        if not workspace_dir \
                                or not os.path.isabs(workspace_dir) \
                                or not os.path.exists(workspace_dir):
            workspace_dir = config.contract_workspace_dir()
        workspace_dir = workspace_dir.strip()        
        project_dir = os.path.join(workspace_dir, project_name)

    if os.path.isdir(project_dir):
        if os.listdir(project_dir):
            if remove_existing:
                try:
                    shutil.rmtree(project_dir)
                except Exception as e:
                    raise errors.Error('''
Cannot remove the directory {}.
error message:
==============
{}
                    '''.format(project_dir, str(e)))
            else:
                msg = '''
                NOTE:
                Contract workspace
                '{}'
                already exists. Cannot overwrite it.
                '''.format(project_dir)
                if throw_exists:
                    raise errors.Error(msg)
                else:
                    raise errors.Error(msg)
                    return

    try:    # make contract directory and its build directory:
        os.makedirs(os.path.join(project_dir, "build"))
    except Exception as e:
            raise errors.Error(str(e))

    def copy_dir_contents(
            project_dir, template_dir, directory, project_name):
        contents = os.listdir(os.path.join(template_dir, directory))
        
        for item in contents:
            path = os.path.join(directory, item)
            template_path = os.path.join(template_dir, path)
            contract_path = os.path.join(
                project_dir, path.replace(
                                        TEMPLATE_NAME, project_name))
                          
            if os.path.isdir(template_path) \
                                        and not "__pycache__" in template_path:
                os.mkdir(contract_path)
                copy_dir_contents(
                            project_dir, template_dir, path, project_name)
            elif os.path.isfile(template_path):
                copy(template_path, contract_path, project_name)

    def copy(template_path, contract_path, project_name):
        with open(template_path, "r") as input:
            template = input.read()

        if TEMPLATE_HOME in template or TEMPLATE_ROOT in template:
            home = os.environ["HOME"]
            root = ""
            if utils.is_windows_ubuntu():
                replace_templates(template)

        template = template.replace("${" + TEMPLATE_NAME + "}", project_name)
        template = template.replace(C_CPP_PROP, c_cpp_properties)
        template = template.replace(TASK_JSON, vscode.TASKS)

        with open(contract_path, "w") as output:
            output.write(template)

    copy_dir_contents(project_dir, template_dir, "", project_name)

    logger.TRACE('''
    * Contract project '{}' created from template 
        '{}'
    '''.format(project_name, template_dir), verbosity)    

    if open_vscode:
        if utils.is_windows_ubuntu():
            command_line = "cmd.exe /C code {}".format(
                utils.wslMapLinuxWindows(project_dir))
        elif utils.uname() == "Darwin":
            command_line = "open -n -b com.microsoft.VSCode --args {}".format(
                project_dir)
        else:
            command_line = "code {}".format(project_dir)

        os.system(command_line)

    logger.INFO('''
    ######## Created contract project ``{}``, 
        originated from template 
        ``{}``.
    '''.format(project_name, template_dir), verbosity)

    return project_dir


def strip_wsl_root(path):
    wsl_root = config.wsl_root()
    if wsl_root:
        return path.replace(config.wsl_root(), "")
    else:
        return path


def get_pid(name=None):
    """Return process ids found by (partial) name or regex.

    >>> get_process_id('kthreadd')
    [2]
    >>> get_process_id('watchdog')
    [10, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56, 61]  # ymmv
    >>> get_process_id('non-existent process')
    []
    """    
    if not name:
        name = os.path.splitext(os.path.basename(config.node_exe()))[0]

    command_line = ['pgrep', name]
    stdout = utils.spawn(
        command_line, "Cannot determine PID of any nodeos process.")

    return [int(pid) for pid in stdout.split()]


def eosio_cpp(command_line, target_dir):

    cwd = os.path.join(target_dir, "cwd")
    os.mkdir(cwd)

    p = subprocess.run(
        command_line,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE) 
    
    stdout = p.stdout.decode("ISO-8859-1")
    stderr = p.stderr.decode("ISO-8859-1")
    returncode = p.returncode
    shutil.rmtree(cwd)

    if returncode:
        raise errors.Error('''
command line:
=============
{}

error message:
==============
{}
        '''.format(" ".join(command_line), stderr))

    return returncode


def get_target_dir(source_dir):
    
    dir = os.path.join(source_dir, "build")
    if os.path.exists(dir):
        return dir

    dir = os.path.join(source_dir, "..", "build")
    if os.path.exists(dir):
        return dir
        
    try:
        os.mkdir(dir)
    except Exception as e:
        raise errors.Error(str(e))

    return dir


def get_resources_dir(source_dir):
    
    dir = os.path.join(source_dir, "..", "resources")
    if os.path.exists(dir):
        return dir

    dir = os.path.join(source_dir, "resources")
    if not os.path.exists(dir):
        try:
            os.mkdir(dir)
        except Exception as e:
            raise errors.Error(str(e))

    return dir


def args(clear=False):
    try:
        data_dir = config.data_dir()
    except:
        data_dir = None

    try:
        config_dir = config.nodeos_config_dir()
    except:
        config_dir = None

    try:
        genesis_json = config.genesis_json()
    except:
        genesis_json = None

    args_ = [
        "--http-server-address", config.http_server_address(),
        "--chain-state-db-size-mb", config.chain_state_db_size_mb(),
        "--contracts-console",
        "--verbose-http-errors",
        "--enable-stale-production",
        "--producer-name eosio",
        "--signature-provider " + config.eosio_key_public() + "=KEY:" 
            + config.eosio_key_private(),
        "--plugin eosio::producer_plugin",
        "--plugin eosio::chain_api_plugin",
        "--plugin eosio::http_plugin",
        "--plugin eosio::history_api_plugin"
    ]
    if config_dir:
        args_.extend(["--config-dir", config_dir])
    if data_dir:
        args_.extend(["--data-dir", data_dir])

    if clear:
        node_stop()
        args_.extend(["--delete-all-blocks"])
        if genesis_json:
            args_.extend(["--genesis-json", genesis_json])            
    return args_


def keosd_start():
    if not config.keosd_wallet_dir(raise_error=False):
        utils.spawn([config.keosd_exe()])

        while True:
            time.sleep(1)
            if config.keosd_wallet_dir(raise_error=False):
                break


def on_nodeos_error(clear=False):

    node_stop()
    args_ = args(clear)
    args_.insert(0, config.node_exe())
    command_line = " ".join(args_)

    logger.ERROR('''
    The local ``nodeos`` failed to start twice in sequence. Perhaps, something is
    wrong with configuration of the system. See the command line issued:

    ''')
    print("\n{}\n".format(command_line))
    logger.INFO('''
    Now, see the result of execution of the command line:
    ''')
    
    p = subprocess.run(
        command_line, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)
    
    err_msg = p.stderr.decode("ISO-8859-1")
    if "error" in err_msg and not "exit shutdown" in err_msg:
        logger.ERROR(err_msg)
    elif not err_msg or "exit shutdown" in err_msg:
        logger.OUT(
        '''
        Just another instability incident of the ``nodeos`` executable. 
        Rerun the script.
        '''
        )
    else:
        print(err_msg)

    node_stop()
    exit()


def node_start(clear=False, nodeos_stdout=None):
    '''Start the local EOSIO node.

    Args:
        clear (bool): If set, the blockchain is deleted and then re-created.
        nodeos_stdout (str): If set, a file where *stdout* stream of
            the local *nodeos* is send. Note that the file can be included to 
            the configuration of EOSFactory, see :func:`.core.config.nodeos_stdout`.
            If the file is set with the configuration, and in the same time 
            it is set with this argument, the argument setting prevails. 
    '''
    args_ = args(clear)

    if setup.is_print_command_line:
        print("######## nodeos command line:")
        print(config.node_exe() + " " + " ".join(args_))

    if not nodeos_stdout:
        nodeos_stdout = config.nodeos_stdout()

    std_out_handle = subprocess.DEVNULL
    if nodeos_stdout:
        try:
            std_out_handle = open(nodeos_stdout, 'w')
        except Exception as e:
            raise errors.Error('''
            Error when preparing to start the local EOS node, 
            opening the given stdout log file that is 
            {}
            Error message is
            {}
            '''.format(nodeos_stdout, str(e)))

    def onExit():
        if not std_out_handle == subprocess.DEVNULL:
            try:
                std_out_handle.close()
            except:
                pass

    if setup.is_print_command_line:
        print("######## nodeos command line:")
        print(config.node_exe() + " " + " ".join(args_))
                
    args_.insert(0, config.node_exe())
    def runInThread():
        proc = subprocess.Popen(
            " ".join(args_), 
            stdin=subprocess.DEVNULL, stdout=std_out_handle, 
            stderr=subprocess.DEVNULL, shell=True)
        proc.wait()
        onExit()
        return
    
    thread = threading.Thread(target=runInThread)
    thread.start()


def node_probe():
    count = 10
    num = 5
    block_num = None
    
    while True:
        time.sleep(1)
        
        try:
            import eosfactory.core.cleos_get as cleos_get
            head_block_num = cleos_get.GetInfo(is_verbose=0).head_block
        except:
            head_block_num = 0
        finally:
            print(".", end="", flush=True)

        if block_num is None:
            block_num = head_block_num

        if head_block_num - block_num >= num:
            print()
            logger.INFO('''
            Local node is running. Block number is {}
            '''.format(head_block_num))
            break

        count = count - 1        
        if count <= 0:
            raise errors.Error('''
            The local node does not respond.
            ''')


def is_local_node_process_running(name=None):
    if not name:
        name = config.node_exe()
    return name in utils.spawn(
        'ps aux |  grep -v grep | grep ' + name, shell=True)
        

def node_stop():
    # You can see if the process is a zombie by using top or 
    # the following command:
    # ps aux | awk '$8=="Z" {print $2}'
    
    pids = get_pid()
    count = 10
    if pids:
        for pid in pids:
            os.system("kill " + str(pid))
        while count > 0:
            time.sleep(1)
            if not is_local_node_process_running():
                break
            count = count -1

    if count <= 0:
        raise errors.Error('''
Failed to kill {}. Pid is {}.
    '''.format(
        os.path.splitext(os.path.basename(config.node_exe()))[0], str(pids))
    )
    else:         
        logger.INFO('''
        Local node is stopped {}.
        '''.format(str(pids)))        

    
def node_is_running():
    return not get_pid()

    return dir
