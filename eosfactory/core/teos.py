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
import sys

import eosfactory.core.errors as errors
import eosfactory.core.logger as logger
import eosfactory.core.utils as utils
import eosfactory.core.setup as setup
import eosfactory.core.config as config
import eosfactory.core.vscode as vscode

TEMPLATE_NAME = "CONTRACT_NAME"
TEMPLATE_HOME = "${HOME}"
C_CPP_PROP = "${c_cpp_prop}"
TASK_JSON = "${tasks}"
CONFIGURATIONS = "configurations"
INCLUDE_PATH = "includePath"
BROWSE = "browse"
WORKSPACE_FOLDER = "${workspaceFolder}"
EOSIO_CPP_INCLUDE = "eosio.cdt"
ROOT = config.wsl_root()
HOME = ROOT + os.environ["HOME"]


def resolve_home(string): 
    string = string.replace(TEMPLATE_HOME, HOME)
    return string


def naturalize_path(path):
    path = path.replace(TEMPLATE_HOME, HOME)
    if path.find("/mnt/") != 0:
        path = ROOT + path
    return utils.wslMapLinuxWindows(path, back_slash=False)


def linuxize_path(path):
    return utils.wslMapWindowsLinux(path.replace(ROOT, ""))


def get_c_cpp_properties(contract_dir=None, c_cpp_properties_path=None):
    if not contract_dir:
        contract_dir = os.getcwd()
    if not c_cpp_properties_path:
        c_cpp_properties_path = os.path.join(
                                contract_dir, ".vscode/c_cpp_properties.json")
    else:
        c_cpp_properties_path = linuxize_path(c_cpp_properties_path)
        if not os.path.exists(c_cpp_properties_path):
            c_cpp_properties_path = os.path.join(
                                contract_dir, ".vscode/c_cpp_properties.json")

    if os.path.exists(c_cpp_properties_path):
        try:
            with open(c_cpp_properties_path, "r") as f:
                return json.loads(f.read())
        except Exception as e:
            raise errors.Error(str(e))
    else:
        return json.loads(resolve_home(vscode.c_cpp_properties()))


def build(
        contract_dir_hint, c_cpp_properties_path=None,
        compile_only=False, verbosity=None):
    '''Produce ABI and WASM files.

    Compiler options come with the argument 'c_cpp_properties_path', as 
    components of 'compilerOptions' list. Option can be any of the 'eosio-cpp'
    options, plus the following ones:

    * --no-src - if set, the contract source file is not automatically detected
        as the only source file in the 'src' directory
    * --src - list of the source files, absolute or relative to 'src' or
        project directories, for example:
        --src hello.cpp tests/hello_test.cpp
    * -o - the same as the corresponding eosio-cpp option, but may be relative
        to 'build' directory

    Without any option set, the only source file is determined as a result of the function :func:`.core.config.contract_source_files`, if the result is a 
    single file. If it is not, an error is thrown, stating that the source file has to be specified with the '--src' option.

    The ABI and WASM targets are named after the contract source file. 

    Args:
        contract_dir_hint (str): Path, may be partial, to the project directory.
        c_cpp_properties_path (str): If set, the path to a c_cpp_properties json 
            file in '.vscode' folder in the project directory.
        compile_only (bool): If set, do not link.
        verbosity (([.core.logger.Verbosity])): Verbosity parameter, used in 
            loggers.
    '''
    contract_dir = config.contract_dir(contract_dir_hint)
    # contract_source_files[0] is directory, contract_source_files[1] is contents:
    contract_source_files = config.contract_source_files(contract_dir)
    c_cpp_properties = get_c_cpp_properties(
                                        contract_dir, c_cpp_properties_path)

    build_dir = get_target_dir(contract_dir)
    target_path = None
    compile_options = []
    source_files = []
    
    ############################################################################
    # begin compiler option logics
    ############################################################################
    recardian_dir = "-R=" + get_recardian_dir(contract_source_files[0])
    compile_options_ = c_cpp_properties[CONFIGURATIONS][0]["compilerOptions"]
    
    if not "-abigen" in compile_options_:
        compile_options.append("-abigen")

    if "--no-src" in compile_options_:
        compile_options_.remove("--no-src")
    else:
        source_ext = [".c", ".cpp",".cxx", ".c++"]
        contract_src_name = None
        for file in contract_source_files[1]:
            if os.path.splitext(file)[1].lower() in source_ext:
                if not contract_src_name:
                    contract_src_name = os.path.splitext(
                                                    os.path.basename(file))[0]
                    source_files.append(os.path.normpath(file))
                else:
                    raise errors.Error('''
Cannot determine the source file of the contract. There is many files in 
the 'src' directory. Specify the file with the compiler option '--src', for
example:
--src src_dir/hello.cpp
The file path is to be absolute or relative to the project directory.
                ''')
    
    for i in range(0, len(compile_options_)):
        entry = compile_options_[i]
        if "-R=" in entry:
            recardian_dir = entry
        elif "-o" in entry:
            target_path = utils.wslMapWindowsLinux(
                                            entry.replace("-o", "").strip())
            if not target_path:
                if i + 1 < len(compile_options_):
                    target_path = compile_options_[i + 1]
                else:
                    raise errors.Error('''
The option '-o' does not has its vaslue set:
{}
                    '''.format(compile_options_))

            if not os.path.isabs(target_path):
                target_path = os.path.join(build_dir, target_path)
                target_dir = os.path.dirname(target_path)
                if not os.path.exists(target_dir):
                    try:
                        os.makedirs(target_dir)
                    except Exception as e:
                        raise errors.Error('''
Cannot make directory set with the option '-o'.
{}
                        '''.format(str(e)))
        
        elif "-abigen_output" in entry:
            abigen_path = utils.wslMapWindowsLinux(
                                    entry.replace("-abigen_output=", "").strip())

            if not os.path.isabs(abigen_path):
                abigen_path = os.path.join(build_dir, abigen_path)
                abigen_dir = os.path.dirname(abigen_path)
                if not os.path.exists(abigen_dir):
                    try:
                        os.makedirs(abigen_dir)
                    except Exception as e:
                        raise errors.Error('''
Cannot make directory set with the option '-abigen_output'.
{}
                        '''.format(str(e)))

            compile_options.append("-abigen_output={}".format(abigen_path))
        elif "--src" in entry:
            input_files_ = utils.wslMapWindowsLinux(
                                            entry.replace("--src", "").strip())
            if not input_files_:
                next_index = i + 1
                while True:
                    if next_index >= len(compile_options_):
                        break

                    next_item = compile_options_[next_index]
                    if "-" in next_item:
                        break
                    
                    input_files_ = input_files_ + " " + next_item
                    
            if not input_files_:
                raise errors.Error('''
The option '--src' does not has its value set:
{}
                '''.format(compile_options_))

            for input_file in input_files_.split(" "):
                temp = input_file
                if not os.path.isabs(temp):
                    temp = os.path.join(contract_source_files[0], input_file)
                    if not os.path.exists(temp):
                        temp = os.path.join(contract_dir, input_file)

                if not os.path.exists(temp):
                    raise errors.Error('''
The source file
{} 
cannot be found. It is neither absolute nor relative to the contract directory
or relative to the 'src' directory.
                    '''.format(input_file))

                temp = os.path.normpath(temp)
                if not temp in source_files:
                    source_files.append(temp)

        else:
            compile_options.append(entry)

    compile_options.append(recardian_dir)
        
    ############################################################################
    # end compiler option logics
    ############################################################################


    if not target_path:
        target_path = os.path.normpath(
                        os.path.join(build_dir, contract_src_name  + ".wasm"))
        abigen_path = os.path.normpath(
                        os.path.join(build_dir, contract_src_name  + ".abi"))

    command_line = [config.eosio_cpp()]
    command_line.extend(["-o", target_path])
 
    for entry in c_cpp_properties[CONFIGURATIONS][0][INCLUDE_PATH]:
        if WORKSPACE_FOLDER in entry:
            entry = entry.replace(WORKSPACE_FOLDER, contract_dir)
            command_line.append("-I=" + linuxize_path(entry))
        else:
            if not EOSIO_CPP_INCLUDE in entry:
                command_line.append(
                    "-I=" + linuxize_path(entry))

    for entry in c_cpp_properties[CONFIGURATIONS][0]["libs"]:
        command_line.append(
            "-l=" + linuxize_path(entry))

    for entry in compile_options:
        command_line.append(entry)

    for input_file in source_files:
        command_line.append(input_file)

    if compile_only:
        command_line.append("-c=")

    if setup.is_print_command_line:
        print("######## command line sent to eosio-cpp:")
        print(" ".join(command_line))

    utils.long_process(command_line, build_dir, is_verbose=True, 
                                                            prompt="eosio-cpp")
    if not compile_only:
        if "wasm" in target_path:
            logger.TRACE('''
                ABI file writen to file: 
                    {}
                '''.format(os.path.normpath(abigen_path)), verbosity)        
            logger.TRACE('''
                WASM file writen to file: 
                    {}
                '''.format(os.path.normpath(target_path)), verbosity)
        else:
            logger.TRACE('''
                terget writen to file: 
                    {}
                '''.format(os.path.normpath(target_path)), verbosity)            


def project_from_template(
        project_name, template=None, workspace_dir=None,
        c_cpp_prop_path=None,
        includes=None,
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
        includes: If set, comma-separated list of include folders.
        libs: If set, comma-separated list of libraries.
        remove_existing: If set, overwrite any existing project.
        visual_studio_code: If set, open the ``VSCode``, if available.
        verbosity: The logging configuration.
    '''
    project_name = linuxize_path(project_name.strip())
    template = linuxize_path(template.strip())

    template_dir = template if os.path.isdir(template) else \
                                os.path.join(config.template_dir(), template)
    
    if not os.path.isdir(template_dir):
        raise errors.Error('''
The contract project template '{}' does not exist.
        '''.format(template_dir)) 

    if c_cpp_prop_path:
        c_cpp_prop_path = linuxize_path(c_cpp_prop_path)
        if os.path.exists(c_cpp_prop_path):
            try:
                with open(c_cpp_prop_path, "r") as f:
                    c_cpp_properties = f.read()
            except Exception:
                c_cpp_properties = vscode.c_cpp_properties()
    else:
        c_cpp_properties = vscode.c_cpp_properties()
    
    c_cpp_properties_json = json.loads(c_cpp_properties)

    if includes:
        temp = includes.split(", ")
        temp_ = []
        for entry in temp:
            path = naturalize_path(entry)
            if not path in c_cpp_properties_json[CONFIGURATIONS][0]\
                                                                [INCLUDE_PATH]:
                temp_.append(path)

        c_cpp_properties_json[CONFIGURATIONS][0][INCLUDE_PATH].extend(temp_)
        c_cpp_properties_json[CONFIGURATIONS][0][BROWSE]["path"].extend(temp_)

    path = config.eoside_includes_dir()
    if path:
        path = naturalize_path(path)
        if not path in c_cpp_properties_json[CONFIGURATIONS][0][INCLUDE_PATH]:
            c_cpp_properties_json[CONFIGURATIONS][0][INCLUDE_PATH].append(path)
            c_cpp_properties_json[CONFIGURATIONS][0][BROWSE]["path"]\
                                                                .append(path)
    
    if libs:
        temp = libs.split(", ")
        temp_ = []
        for entry in libs:
            path = naturalize_path(entry)
            if not path in c_cpp_properties_json[CONFIGURATIONS][0]["libs"]:
                temp_.append(path)
            
        c_cpp_properties_json[CONFIGURATIONS][0]["libs"].extend(temp_)

    eoside_libs = config.eoside_libs_dir()
    if(eoside_libs):
        eoside_libs = os.listdir(config.eoside_libs_dir())
        for lib in eoside_libs:
            path = naturalize_path(lib)
            if not path in c_cpp_properties_json[CONFIGURATIONS][0]["libs"]:
                c_cpp_properties_json[CONFIGURATIONS][0]["libs"].append(path)

    c_cpp_properties = json.dumps(c_cpp_properties_json, indent=4)
    c_cpp_properties = resolve_home(c_cpp_properties)
    
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

    try:    # make contract directory and its build directory:
        os.makedirs(os.path.join(project_dir, "build"))
    except Exception as e:
        raise errors.Error(str(e))
    try:    # make contract directory and its tests directory:
        os.makedirs(os.path.join(project_dir, "tests"))
    except Exception as e:
        raise errors.Error(str(e))
    try:    # make contract directory and its include directory:
        os.makedirs(os.path.join(project_dir, "include"))
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
                if not os.path.exists(contract_path):
                    os.mkdir(contract_path)
                copy_dir_contents(
                            project_dir, template_dir, path, project_name)
            elif os.path.isfile(template_path):
                copy(template_path, contract_path, project_name)

    def copy(template_path, contract_path, project_name):
        with open(template_path, "r") as f:
            template = f.read()

        if TEMPLATE_HOME in template:
            resolve_home(template)

        template = template.replace(C_CPP_PROP, c_cpp_properties)
        template = template.replace(TASK_JSON, vscode.TASKS)
        template = template.replace("${" + TEMPLATE_NAME + "}", project_name)

        with open(contract_path, "w") as output:
            output.write(template)

    copy_dir_contents(project_dir, template_dir, "", project_name)  

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
######## Created contract project '{}', 
    originated from template 
    '{}'.
    '''.format(project_dir, template_dir), verbosity)

    return project_dir


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


def get_target_dir(contract_dir):

    path = os.path.join(contract_dir, "build")
    if os.path.exists(path):
        return path
        
    try:
        os.mkdir(path)
    except Exception as e:
        raise errors.Error(str(e))

    return path


def get_recardian_dir(source_dir):
    
    path = os.path.join(source_dir, "..", "ricardian")
    if os.path.exists(path):
        return path

    path = os.path.join(source_dir, "ricardian")
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except Exception as e:
            raise errors.Error(str(e))

    return path


def get_include_dir(source_dir):
    
    path = os.path.join(source_dir, "..", "include")
    if os.path.exists(path):
        return path

    path = os.path.join(source_dir, "include")
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except Exception as e:
            raise errors.Error(str(e))

    return path


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
    count = 20
    count1 = count - 7
    num = 5
    block_num = None
    time.sleep(5)

    while True:
        time.sleep(1)
        count = count - 1
        if count > count1:
            print(".", end="", flush=True)
            continue

        try:
            import eosfactory.core.cleos_get as cleos_get
            head_block_num = cleos_get.GetInfo(is_verbose=0).head_block
        except:
            head_block_num = 0
        finally:
            print("*", end="", flush=True)

        if block_num is None:
            block_num = head_block_num

        if head_block_num - block_num >= num:
            print()
            logger.INFO('''
            Local node is running. Block number is {}
            '''.format(head_block_num))
            break

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

