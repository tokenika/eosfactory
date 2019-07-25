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
import math
import psutil

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
BROWSE = "browse"
WORKSPACE_FOLDER = "${workspaceFolder}"
# The root directory of the Windows WSL, or empty string if not Windows:
ROOT = config.wsl_root() 
HOME = ROOT + os.environ["HOME"] # Linux ~home<user name>
PROJECT_0_DIR = os.path.join(config.template_dir(), config.PROJECT_0)
ERR_MSG_IS_STUCK = "The process of 'nodeos' is stuck."


def resolve_home(string): 
    return string.replace(TEMPLATE_HOME, HOME)


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
        compile_only=False, is_test_mode=False, is_execute=False, 
        verbosity=None):
    '''Produce ABI and WASM files.

    Compiler options come with the argument 'c_cpp_properties_path', as 
    components of 'compilerOptions' list. Option can be any of the 'eosio-cpp'
    options, plus the following ones:

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

    if is_test_mode \
                and vscode.TEST_OPTIONS in c_cpp_properties[CONFIGURATIONS][0]:
        compile_options_ = c_cpp_properties[CONFIGURATIONS][0]\
                                                        [vscode.TEST_OPTIONS]
    elif not is_test_mode \
                and vscode.CODE_OPTIONS in c_cpp_properties[CONFIGURATIONS][0]:
        compile_options_ = c_cpp_properties[CONFIGURATIONS][0]\
                                                        [vscode.CODE_OPTIONS]
    else:
        compile_options_ = []

    contract_src_name = None
    is_verbose = False

    if not "-abigen" in compile_options_:
        compile_options.append("-abigen")
    if is_test_mode and not "-fnative" in compile_options_:
        compile_options.append("-fnative")
    
    for i in range(0, len(compile_options_)):
        entry = compile_options_[i]
        if "-R=" in entry:
            recardian_dir = entry
        elif "-contract=" in entry:
            contract_src_name = entry.replace("-contract=", "").strip()
            compile_options.append(entry)
        elif "--verbose" in entry:
            is_verbose = True
        elif "-o" in entry:
            target_path = utils.wslMapWindowsLinux(
                                            entry.replace("-o", "").strip())
            if not target_path:
                if i + 1 < len(compile_options_):
                    target_path = compile_options_[i + 1]
                else:
                    raise errors.Error('''
The option '-o' does not has its value set:
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
                    if not contract_src_name:
                        contract_src_name = os.path.splitext(
                                                    os.path.basename(temp))[0]
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

    if not source_files:
        source_files = contract_source_files[1]
    
    if not source_files:
        raise errors.Error('''
Cannot find any source file (".c", ".cpp",".cxx", ".c++") in the contract folder.
        ''')

    if not is_test_mode and len(source_files) > 1: 
            raise errors.Error('''
Cannot determine the source file of the contract. There is many files in 
the 'src' directory, namely:
{}
Specify the file with the compiler option '--src', for
example:
--src src_dir/hello.cpp
The file path is to be absolute or relative to the project directory.
            '''.format("\n".join(source_files)))

    if not contract_src_name:
        contract_src_name = os.path.splitext(
                                        os.path.basename(source_files[0]))[0]

    if not contract_src_name and len(source_files) == 1:
            contract_src_name = os.path.splitext(
                                        os.path.basename(source_files[0]))[0]
        
    ############################################################################
    # end compiler option logics
    ############################################################################

    if not target_path:
        target_path = os.path.normpath(
                        os.path.join(build_dir, contract_src_name  + ".wasm"))
        abigen_path = os.path.normpath(
                        os.path.join(build_dir, contract_src_name  + ".abi"))
    if is_execute:
        logger.TRACE('''
            Executing target
                {}
        '''.format(target_path))
        command_line = [target_path]

        if setup.is_print_command_lines and setup.is_save_command_lines:
            setup.add_to__command_line_file(" ".join(command_line))
        if setup.is_print_command_lines or is_verbose:
            logger.DEBUG('''
                ######## command line:
                {}
                '''.format(" ".join(command_line)), [logger.Verbosity.DEBUG])
        utils.long_process(command_line, build_dir, is_verbose=True, 
                                                            prompt=target_path)
        return

    command_line = [config.eosio_cpp()]

    if compile_only:
        command_line.append("-c")
    else:
        command_line.extend(["-o", target_path])

    for entry in c_cpp_properties[CONFIGURATIONS][0][vscode.INCLUDE_PATH]:
        if WORKSPACE_FOLDER in entry:
            entry = entry.replace(WORKSPACE_FOLDER, contract_dir)
            command_line.append("-I=" + linuxize_path(entry))
        else:
            path = linuxize_path(entry)
            if not path in config.eosio_cpp_includes():
                command_line.append(
                    "-I=" + path)

    for entry in c_cpp_properties[CONFIGURATIONS][0][vscode.LIBS]:
        command_line.append(
            "-l=" + linuxize_path(entry))

    for entry in compile_options:
        command_line.append(entry)

    for input_file in source_files:
        command_line.append(input_file)

    if setup.is_print_command_lines and setup.is_save_command_lines:
        setup.add_to__command_line_file(" ".join(command_line))
    if setup.is_print_command_lines or is_verbose:
        logger.DEBUG('''
            ######## command line:
            {}
            '''.format(" ".join(command_line)), [logger.Verbosity.DEBUG])
        
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
    print("eosio-cpp: OK")            


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
                                                        [vscode.INCLUDE_PATH]:
                temp_.append(path)

        c_cpp_properties_json[CONFIGURATIONS][0][vscode.INCLUDE_PATH]\
                                                                .extend(temp_)
        c_cpp_properties_json[CONFIGURATIONS][0][BROWSE]["path"].extend(temp_)

    path = config.eoside_includes_dir()
    if path:
        path = naturalize_path(path)
        if not path in c_cpp_properties_json[CONFIGURATIONS][0]\
                                                        [vscode.INCLUDE_PATH]:
            c_cpp_properties_json[CONFIGURATIONS][0]\
                                            [vscode.INCLUDE_PATH].append(path)
            c_cpp_properties_json[CONFIGURATIONS][0][BROWSE]["path"]\
                                                                .append(path)
    
    if libs:
        temp = libs.split(", ")
        temp_ = []
        for entry in libs:
            path = naturalize_path(entry)
            if not path in c_cpp_properties_json[CONFIGURATIONS][0]\
                                                                [vscode.LIBS]:
                temp_.append(path)
            
        c_cpp_properties_json[CONFIGURATIONS][0][vscode.LIBS].extend(temp_)

    eoside_libs = config.eoside_libs_dir()
    if(eoside_libs):
        eoside_libs = os.listdir(config.eoside_libs_dir())
        for lib in eoside_libs:
            path = naturalize_path(lib)
            if not path in c_cpp_properties_json[CONFIGURATIONS][0]\
                                                                [vscode.LIBS]:
                c_cpp_properties_json[CONFIGURATIONS][0]\
                                                    [vscode.LIBS].append(path)

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

    try:
        os.makedirs(os.path.join(project_dir, "build"))
        os.makedirs(os.path.join(project_dir, "tests"))
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

    copy_dir_contents(project_dir, PROJECT_0_DIR, "", project_name)
    if not template_dir == PROJECT_0_DIR: 
        copy_dir_contents(project_dir, template_dir, "", project_name)  

    if open_vscode:
        if utils.is_windows_ubuntu():
            command_line = "cmd.exe /C code {}".format(
                utils.wslMapLinuxWindows(project_dir))
        elif utils.os_version() == utils.DARWIN:
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
    """Return process ids found by name.
    """    
    if not name:
        name = os.path.splitext(os.path.basename(config.node_exe()))[0]

    pids = []
    processes = [p.info for p in psutil.process_iter(attrs=["pid", "name"]) \
                                        if p.info["name"] and name in p.info["name"]]
    for process in processes:
        pids.append(process["pid"])

    return pids


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
    ]
    if config.nodeos_config_dir():
        args_.extend(["--config-dir", config.nodeos_config_dir()])
    if config.nodeos_data_dir():
        args_.extend(["--data-dir", config.nodeos_data_dir()])
    if config.nodeos_options():
        args_.extend(nodeos_options())

    if clear:
        node_stop()
        args_.extend(["--delete-all-blocks"])
        if config.genesis_json():
            args_.extend(["--genesis-json", config.genesis_json()])     
    return args_


def keosd_start():
    if not config.keosd_wallet_dir(raise_error=False):
        utils.spawn([config.keosd_exe()])

        while True:
            time.sleep(1)
            if config.keosd_wallet_dir(raise_error=False):
                break


def on_nodeos_error(clear=False):
    ERROR_WAIT_TIME = 5
    NOT_ERROR = [
        "exit shutdown",
        "configuration items in the config.ini file are redundantly",
        ]

    node_stop()
    args_ = args(clear)
    args_.insert(0, config.node_exe())
    command_line = " ".join(args_)

    logger.ERROR('''
    The local 'nodeos' failed to start few times in sequence. Perhaps, something is
    wrong with configuration of the system. See the command line issued:

    ''')
    print("\n{}\n".format(command_line))
    print('''
Now, see the result of execution of the command line:
    ''')

    def runInThread():
        proc = subprocess.Popen(
            " ".join(args_), 
            stdin=subprocess.DEVNULL, stdout=std_out_handle, 
            stderr=subprocess.PIPE, shell=True)
        out, err = proc.communicate()  

        err_msg = err.decode("ISO-8859-1")
        not_error = False
        if err_msg:
            for item in NOT_ERROR:
                if item in err_msg:
                    not_error = True
                    break

        if not_error:
            print(
            '''
Just another hang incident of the 'nodeos' executable.''')
            if clear:
                print(
                '''
Rerun the script.
                ''')
            else:
                print(
                '''
Rerun the script with 'nodeos' restarted.
                ''')                
        else:
            print(err_msg)

    thread = threading.Thread(target=runInThread)
    thread.start()

    # Wait for the nodeos process to crash
    for i in (0, int(ERROR_WAIT_TIME)):
        print(".", end="", flush=True)
        time.sleep(ERROR_WAIT_TIME)
    print()

    # Kill the process: it is stuck, or it is running well.
    node_stop()
    exit()


std_out_handle = None
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
        
    if not nodeos_stdout:
        nodeos_stdout = config.nodeos_stdout()

    global std_out_handle
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
        global std_out_handle
        if not std_out_handle == subprocess.DEVNULL:
            try:
                std_out_handle.close()
            except:
                pass

    if setup.is_save_command_lines:
        setup.add_to__command_line_file(
                                    config.node_exe() + " " + " ".join(args_))
    if setup.is_print_command_lines:
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
    DELAY_TIME = 4
    WAIT_TIME = 1

    NUMBER_BLOCKS_ADDED = 3
    NUMBER_GET_INFO_CALLS = 7
    CHECK_COUNT = 2
    RATIO_THRESHOLD = 2.5
    NODEOS = "nodeos"

    count = NUMBER_GET_INFO_CALLS
    block_num = None

    pid = None
    for i in range(0, 5):
        pids = [p.info for p in psutil.process_iter(attrs=["pid", "name"]) \
                                        if p.info["name"] and NODEOS in p.info["name"]]
        if pids and pids[0]["name"] == NODEOS:
            pid = pids[0]["pid"]
            break
        time.sleep(0.5)
    if not pid:
        raise errors.Error('''
Local node has failed to start.
            ''')
    proc = psutil.Process(pid)
    cpu_percent_start = proc.cpu_percent(interval=WAIT_TIME)

    print("Starting nodeos, cpu percent: ", end="", flush=True)
    for i in range(0, int(DELAY_TIME / WAIT_TIME)):
        cpu_percent = proc.cpu_percent(interval=WAIT_TIME)
        print("{:.0f}, ".format(cpu_percent), end="", flush=True)

    while True:

        if not proc.is_running():
            raise errors.Error('''
Local node has stopped.
''')
        count = count - 1

        cpu_percent = proc.cpu_percent(interval=WAIT_TIME)
        
        try:
            import eosfactory.core.cleos_get as cleos_get
            head_block_num = cleos_get.GetInfo(is_verbose=0).head_block
            if block_num is None:
                block_num = head_block_num
                count = int(NUMBER_BLOCKS_ADDED * 0.5/WAIT_TIME) + 1
        except:
            head_block_num = 0
            pass
        
        if block_num:
            print("{:.0f}* ".format(cpu_percent), end="", flush=True)
        else:
            print("{:.0f}; ".format(cpu_percent), end="", flush=True)

        if count == CHECK_COUNT and not block_num and \
                            cpu_percent_start / cpu_percent < RATIO_THRESHOLD:
            print(" stuck.")
            raise errors.Error(ERR_MSG_IS_STUCK)        

        if block_num and head_block_num - block_num >= NUMBER_BLOCKS_ADDED:
            print()
            logger.INFO('''
            Local node is running. Block number is {}
            '''.format(head_block_num))
            break

        if count <= 0:
            print()
            raise errors.Error('''
The local node does not respond.
            ''')


def is_local_node_process_running():
    return len(get_pid()) > 0


def kill(name):
    pids = get_pid(name)
    count = 10
    for pid in pids:
        p = psutil.Process(pid)
        p.terminate()
    
        while count > 0:
            time.sleep(1)
            if not psutil.pid_exists(pid):
                break            
            count = count -1

    if count <= 0:
        raise errors.Error('''
Failed to kill {}. Pid is {}.
    '''.format(
        os.path.splitext(os.path.basename(config.node_exe()))[0], str(pids))
    )

    return pids


def kill_keosd():
    kill(os.path.splitext(os.path.basename(config.keosd_exe()))[0])


def node_stop(verbose=True):
    # You can see if the process is a zombie by using top or 
    # the following command:
    # ps aux | awk '$8=="Z" {print $2}'

    kill_keosd()
    pids = kill(os.path.splitext(os.path.basename(config.node_exe()))[0])
    
    if verbose:
        logger.INFO('''
Local node is stopped {}.
        '''.format(str(pids)))        

    
def node_is_running():
    return not get_pid()

