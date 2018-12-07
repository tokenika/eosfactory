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

import eosfactory.core.logger as logger
import eosfactory.core.utils as utils
import eosfactory.core.setup as setup
import eosfactory.core.config as config
import eosfactory.core.errors as errors
import eosfactory.core.vscode as vscode


TEMPLATE_CONTRACTS_DIR = "templates/contracts"
TEMPLATE_NAME = "CONTRACT_NAME"
TEMPLATE_EOSIO_DIR = "${EOSIO_DIR}"
TEMPLATE_HOME = "${HOME}"
TEMPLATE_ROOT = "${ROOT}"
C_CPP_PROP = "${c_cpp_prop}"
TASK_JSON = "${tasks}"


def replace_templates(string): 
    home = os.environ["HOME"]
    root = ""
    eosio_dir = config.eosio_repository_dir()
    if is_windows_ubuntu():
        home = config.wsl_root() + home
        root = config.wsl_root()
        eosio_dir = config.wsl_root() + eosio_dir

    string = string.replace(TEMPLATE_HOME, home)
    string = string.replace(TEMPLATE_ROOT, root)
    string = string.replace(TEMPLATE_EOSIO_DIR, eosio_dir)
    return string                                                      


def get_c_cpp_properties(contract_dir, c_cpp_properties_path):
    if not c_cpp_properties_path:
        c_cpp_properties_path = os.path.join(
                                contract_dir, ".vscode/c_cpp_properties.json")
    else:
        c_cpp_properties_path = utils.wslMapWindowsLinux(c_cpp_properties_path)
        if not os.path.exists(c_cpp_properties_path):
            raise errors.Error('''
                The given path does not exist:
                ${}       
            '''.format(c_cpp_properties_path))
    
    if os.path.exists(c_cpp_properties_path):
        try:
            with open(c_cpp_properties_path, "r") as input:
                return json.loads(input.read())
        except Exception as e:
            raise errors.Error(str(e))
    else:
        return json.loads(replace_templates(vscode.c_cpp_properties))


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
        "The source is empty. The assumed contract dir is   
        {}
        '''.format(contract_dir))
        return

    code_name = os.path.splitext(os.path.basename(source_files[0]))[0]
    target_path = os.path.normpath(
                        os.path.join(get_target_dir(
                            contract_source_files[0]), code_name  + ".abi"))

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
        config.eosio_abigen(),
        "-contract=" + code_name,
        "-R=" + get_resources_dir(contract_source_files[0]),
        "-output=" + target_path]

    c_cpp_properties = get_c_cpp_properties(
                                    contract_dir, c_cpp_properties_path)

    for entry in c_cpp_properties["configurations"][0]["includePath"]:
        if entry == "${workspaceFolder}":
            command_line.append("-extra-arg=-I=" + contract_dir)
        else:
            command_line.append("-extra-arg=-I=" + strip_wsl_root(entry))

    for file in source_files:
        command_line.append(file)

    try:
        process(command_line)
    except Exception as e:
        raise errors.Error(str(e))

    logger.TRACE('''
    ABI file writen to file: {}
    '''.format(target_path), verbosity)


def WAST(
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
        "The source is empty. The assumed contract dir is   
        {}
        '''.format(contract_dir))
        return

    code_name = os.path.splitext(os.path.basename(source_files[0]))[0]
    target_path = os.path.normpath(
                        os.path.join(get_target_dir(
                            contract_source_files[0]), code_name  + ".wasm"))

    c_cpp_properties = get_c_cpp_properties(
                                        contract_dir, c_cpp_properties_path)

    command_line = [config.eosio_cpp()]

    for entry in c_cpp_properties["configurations"][0]["includePath"]:
        if entry == "${workspaceFolder}":
            command_line.append("-I=" + contract_dir)
        else:
            command_line.append("-I=" + strip_wsl_root(entry))

    for entry in c_cpp_properties["configurations"][0]["libs"]:
        command_line.append("-l=" + strip_wsl_root(entry))

    for entry in c_cpp_properties["configurations"][0]["compilerOptions"]:
        command_line.append(entry)
    
    for file in source_files:
        command_line.append(file)

    if setup.is_print_command_line:
        print("######## {}:".format(config.wasm_llvm_link_exe()))
        print(" ".join(command_line))

    if not compile_only:
        command_line.append("-o=" + target_path)

    try:
        process(command_line)
    except Exception as e:                       
        raise errors.Error(str(e))

    if not compile_only:
        logger.TRACE('''
            WASM file writen to file: {}
            '''.format(os.path.normpath(target_path)), verbosity)


def project_from_template(
        project_name, template=None, workspace_dir=None,
        c_cpp_prop_path=None, 
        remove_existing=False, 
        open_vscode=False, throw_exists=False, 
        verbosity=None):
    '''Given the project name and template name, create a smart contract project.

    - **parameters**::

        project_name: The name of the project, or an existing path to 
            a directory.
        template: The name of the template used.
        workspace_dir: If set, the folder for the work-space. Defaults to the 
            value returned by the config.contract_workspace() function.
        remove_existing: If set, overwrite any existing project.
        visual_studio_code: If set, open the ``VSCode``, if available.
        verbosity: The logging configuration.
    '''
    project_name = utils.wslMapWindowsLinux(project_name.strip())
    template = template.strip()
    template_dir = utils.wslMapWindowsLinux(template)
    if not os.path.isdir(template_dir):
        template_dir = os.path.join(
            config.eosf_dir(), TEMPLATE_CONTRACTS_DIR, template) 
    if not os.path.isdir(template_dir):
        raise errors.Error('''
        TemplateCreate '{}' does not exist.
        '''.format(template_dir)) 
       
    if not workspace_dir \
                            or not os.path.isabs(workspace_dir) \
                            or not os.path.exists(workspace_dir):
        workspace_dir = config.contract_workspace()
    workspace_dir = workspace_dir.strip()

    if c_cpp_prop_path:
        c_cpp_prop_path = utils.wslMapWindowsLinux(c_cpp_prop_path)
        if os.path.exists(c_cpp_prop_path):
            try:
                with open(c_cpp_prop_path, "r") as input:
                    c_cpp_properties = json.loads(input.read())
            except Exception:
                c_cpp_properties = vscode.c_cpp_properties
    else:
        c_cpp_properties = vscode.c_cpp_properties

    c_cpp_properties = replace_templates(vscode.c_cpp_properties)

    split = os.path.split(project_name)
    if os.path.isdir(split[0]):
        project_dir = project_name
        project_name = split[1]
    else:
        project_dir = os.path.join(workspace_dir, project_name)
    if os.path.isdir(project_dir):
        if os.listdir(project_dir):
            if remove_existing:
                try:
                    shutil.rmtree(project_dir)
                except Exception as e:
                    raise errors.Error(str(e))
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
                    logger.ERROR(msg)
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
            # import pdb; pdb.set_trace()                            
            if os.path.isdir(template_path):
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
            eosio_dir = config.eosio_repository_dir()
            if is_windows_ubuntu():
                home = config.wsl_root() + home
                root = config.wsl_root()
                eosio_dir = config.wsl_root() + eosio_dir
            template = template.replace(TEMPLATE_HOME, home)
            template = template.replace(TEMPLATE_ROOT, root)
            template = template.replace(TEMPLATE_EOSIO_DIR, eosio_dir)

        template = template.replace("${" + TEMPLATE_NAME + "}", project_name)
        template = template.replace(C_CPP_PROP, c_cpp_properties)
        template = template.replace(TASK_JSON, vscode.TASKS)

        with open(contract_path, "w") as output:
            output.write(template)

    copy_dir_contents(project_dir, template_dir, "", project_name)

    logger.TRACE('''
    * Contract project '{}' created from template '{}'
    '''.format(project_name, template_dir), verbosity)    

    if open_vscode:
        if is_windows_ubuntu():
            command_line = "cmd.exe /C code {}".format(
                utils.wslMapLinuxWindows(project_dir))
        elif uname() == "Darwin":
            command_line = "open -n -b com.microsoft.VSCode --args {}".format(
                project_dir)
        else:
            command_line = "code {}".format(project_dir)

        os.system(command_line)

    logger.INFO('''
    ######### Created contract project ``{}``, originated from template ``{}``.
    '''.format(project_name, template_dir), verbosity)

    return project_dir


def strip_wsl_root(path):
    return path.replace(config.wsl_root(), "")


def get_keosd_wallet_dir():
    '''
    Get the directory of the `nodeos` local wallet.
    '''
    return config.keosd_wallet_dir()


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
        name = config.node_exe_name()

    child = subprocess.Popen(
        ['pgrep', '-f', name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    return [int(pid) for pid in response.split()]


def uname(options=None):
    args = ['uname']
    if options:
        args.append(options)

    child = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    return response.decode("utf-8").strip()


def is_windows_ubuntu():
    resp = uname("-v")
    return resp.find("Microsoft") != -1


def process(command_line, throw_error=True):
    process = subprocess.run(
        command_line,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE) 
    
    out_msg = process.stdout.decode("utf-8")
    out_err = process.stderr.decode("utf-8")
    returncode = process.returncode
    if returncode and throw_error:
        raise errors.Error(out_err)

    return returncode


def get_target_dir(source_dir):
    
    dir = os.path.join(source_dir, "..", "build")
    if os.path.exists(dir):
        return dir

    dir = os.path.join(source_dir, "build")
    if not os.path.exists(dir):
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
    args_ = [
        "--http-server-address", config.http_server_address(),
        "--data-dir", config.data_dir(),
        "--config-dir", config.config_dir(),
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
    if clear:
        node_stop()
        args_.extend([
            "--genesis-json", config.genesis_json(),
            "--delete-all-blocks"
        ])
    return args_


def node_start(clear=False, nodeos_stdout=None, verbosity=None):
    args_ = args(clear)

    if setup.is_print_command_line:
        print("nodeos command line:")
        print(config.node_exe() + " " + " ".join(args_))

    if config.is_nodeos_in_window():
        if is_windows_ubuntu():
            args_.insert(0, config.node_exe())
            subprocess.call(
                ["cmd.exe", "/c", "start", "/MIN", "bash.exe", "-c", 
                " ".join(args_)])
        elif uname() == "Darwin":
                subprocess.Popen(
                    "open -a "
                    + config.node_exe() + " --args " + " ".join(args_),
                    shell=True)
        else:
            args_.insert(0, config.node_exe())
            subprocess.Popen(
                "gnome-terminal -- " + " ".join(args_), shell=True)
    else:
        if not nodeos_stdout:
            nodeos_stdout = config.nodeos_stdout()

        std_out_handle = subprocess.DEVNULL
        if nodeos_stdout:
            try:
                std_out_handle = open(nodeos_stdout, 'w')
            except Exception as e:
                raise errors.Error('''
Error when preparing to start the local EOS node, opening the given stdout
log file that is 
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

    node_probe(verbosity)


def node_probe(verbosity=None):
    count = 15
    num = 5
    block_num = None
    
    while True:
        time.sleep(1)
        
        try:
            if setup.node_api == "cleos":
                import eosfactory.core.cleos as cleos
            elif setup.node_api == "eosjs":
                import eosfactory.core.eosjs as cleos

            get_info = cleos.GetInfo(is_verbose=0)
            head_block_num = int(get_info.json["head_block_num"])
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
            '''.format(head_block_num), verbosity)
            break

        count = count - 1        
        if count <= 0:
            raise errors.Error('''
            The local node does not respond.
            ''')


def is_local_node_process_running(name=None):
    if not name:
        name = config.node_exe()

    response = subprocess.run(
        'ps aux |  grep -v grep | grep ' + name, shell=True, 
        stdout=subprocess.PIPE)
    out = response.stdout.decode("utf-8")
    return name in out
        

def node_stop(verbosity=None):
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
    '''.format(config.node_exe_name(), str(pids))
    )
    else:         
        logger.INFO('''
        Local node is stopped {}.
        '''.format(str(pids)), verbosity)        

    
def node_is_running():
    return not get_pid()

    return dir