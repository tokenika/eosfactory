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
import importlib

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
# The root directory of the Windows WSL, or empty string if not Windows:
ROOT = config.wsl_root() 
HOME = ROOT + os.environ["HOME"] # Linux ~home<user name>
PROJECT_0_DIR = os.path.join(config.template_dir(), config.PROJECT_0)
ERR_MSG_IS_STUCK = "The process of 'nodeos' is stuck."


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


def resolve_home(string): 
    return string.replace(TEMPLATE_HOME, HOME)


def naturalize_path(path):
    path = path.replace(TEMPLATE_HOME, HOME)
    if path.find("/mnt/") != 0:
        path = ROOT + path
    return utils.wslMapLinuxWindows(path, back_slash=False)


def linuxize_path(path):
    return utils.wslMapWindowsLinux(path.replace(ROOT, ""))


def project_from_template(
        project_name, template=None, workspace_dir=None,
        c_cpp_prop_path=None,
        includes=None,
        libs=None, 
        remove_existing=False, 
        open_vscode=False, throw_exists=False, 
        verbosity=None):
    """Given the project name and template name, create a smart contract project.

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
    """
    project_name = linuxize_path(project_name.strip())
    template = linuxize_path(template.strip())
    template_dir = template if os.path.isdir(template) else \
                                os.path.join(config.template_dir(), template)
    if not os.path.isdir(template_dir):
        raise errors.Error("""
The contract project template '{}' does not exist.
        """.format(template_dir)) 

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
                    raise errors.Error("""
Cannot remove the directory {}.
error message:
==============
{}
                    """.format(project_dir, str(e)))
            else:
                msg = """
NOTE:
Contract workspace
'{}'
already exists. Cannot overwrite it.
                """.format(project_dir)
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

    logger.INFO("""
######## Created contract project '{}', 
    originated from template 
    '{}'.
    """.format(project_dir, template_dir), verbosity)

    return project_dir


def get_pid(name=None):
    """Return process ids found by name.
    """    
    if not name:
        name = os.path.splitext(os.path.basename(config.node_exe()))[0]

    if os.path.exists(name):
        name = os.path.splitext(os.path.basename(name))[0]

    processes = [p.info for p in psutil.process_iter(attrs=["pid", "name"]) \
                                        if name in p.info["name"]]
    
    pids = []
    for process in processes:
        pids.append(process["pid"])

    return pids


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
        "--plugin eosio::history_api_plugin",
    ]
    if config.nodeos_config_dir():
        args_.extend(["--config-dir", config.nodeos_config_dir()])
    if config.nodeos_data_dir():
        args_.extend(["--data-dir", config.nodeos_data_dir()])
    if config.nodeos_options():
        args_.extend(config.nodeos_options())

    if clear:
        node_stop()
        args_.extend(["--delete-all-blocks"])
        if config.genesis_json():
            args_.extend(["--genesis-json", config.genesis_json()])     
    return args_


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

    logger.ERROR("""
    The local ``nodeos`` failed to start few times in sequence. Perhaps, something is
    wrong with configuration of the system. See the command line issued:

    """)
    print("\n{}\n".format(command_line))
    print("""
Now, see the result of execution of the command line:
    """)

    def runInThread():
        proc = subprocess.Popen(
            " ".join(args_), 
            stdin=subprocess.DEVNULL, stdout=std_out_handle, 
            stderr=subprocess.PIPE, shell=True)
        _, err = proc.communicate()  

        err_msg = err.decode("ISO-8859-1")
        not_error = False
        if err_msg:
            for item in NOT_ERROR:
                if item in err_msg:
                    not_error = True
                    break

        if not_error:
            print(
            """
Just another hang up incident of the ``nodeos`` executable.""")
            if clear:
                print(
                """
Rerun the script.
                """)
            else:
                print(
                """
Rerun the script with ``nodeos`` restarted.
                """)                
        else:
            print(err_msg)

    thread = threading.Thread(target=runInThread)
    thread.start()

    # Wait for the nodeos process to crash
    for _ in (0, int(ERROR_WAIT_TIME)):
        print(".", end="", flush=True)
        time.sleep(ERROR_WAIT_TIME)
    print()

    # Kill the process: it is stuck, or it is running well.
    node_stop()
    exit()


std_out_handle = None
def node_start(clear=False, nodeos_stdout=None):
    """Start the local EOSIO node.

    Args:
        clear (bool): If set, the blockchain is deleted and then re-created.
        nodeos_stdout (str): If set, a file where *stdout* stream of
            the local ``nodeos`` is send. Note that the file can be included to 
            the configuration of EOSFactory, see :func:`.core.config.nodeos_stdout`.
            If the file is set with the configuration, and in the same time 
            it is set with this argument, the argument setting prevails. 
    """
    
    args_ = args(clear)
        
    if not nodeos_stdout:
        nodeos_stdout = config.nodeos_stdout()

    global std_out_handle
    std_out_handle = subprocess.DEVNULL
    if nodeos_stdout:
        try:
            std_out_handle = open(nodeos_stdout, 'w')
        except Exception as e:
            raise errors.Error("""
Error when preparing to start the local EOS node, 
opening the given stdout log file that is 
{}
Error message is
{}
            """.format(nodeos_stdout, str(e)))

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

    # Wait for nodeos to appear in the process list:
    pid = None
    for _ in range(0, int(DELAY_TIME / WAIT_TIME)):
        pids = [p.info for p in psutil.process_iter(attrs=["pid", "name"]) \
                                        if NODEOS in p.info["name"]]
        if pids and pids[0]["name"] == NODEOS:
            pid = pids[0]["pid"]
            break
        time.sleep(WAIT_TIME)
    if not pid:
        raise errors.Error("""
Local node has failed to start.
            """)

    proc = psutil.Process(pid)
    cpu_percent_start = proc.cpu_percent(interval=WAIT_TIME)

    # Give nodeos a time to restart:
    print("Starting nodeos, cpu percent: ", end="", flush=True)
    for _ in range(0, int(DELAY_TIME / WAIT_TIME)):
        cpu_percent = proc.cpu_percent(interval=WAIT_TIME)
        print("{:.0f}, ".format(cpu_percent), end="", flush=True)

    # Probe the process:
    while True:
        if not proc.is_running():
            raise errors.Error("""
Local node has stopped.
""")
        count = count - 1
        cpu_percent = proc.cpu_percent(interval=WAIT_TIME)

        try:
            GET_COMMANDS = importlib.import_module(".get", setup.light_full)
            head_block_num = GET_COMMANDS.GetInfo(is_verbose=0).head_block
            if block_num is None:
                block_num = head_block_num
                count = int(NUMBER_BLOCKS_ADDED * 0.5/WAIT_TIME) + 1
        except errors.IsNodeRunning:
            head_block_num = 0
        except Exception as e:
            raise errors.Error(str(e))

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
            logger.INFO("""
            Local node is running. Block number is {}
            """.format(head_block_num))
            break

        if count <= 0:
            print()
            raise errors.Error("""
The local node does not respond.
            """)


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
        raise errors.Error("""
Failed to kill {}. Pid is {}.
    """.format(
        os.path.splitext(os.path.basename(config.node_exe()))[0], str(pids))
    )

    return pids


def keosd_kill():
    kill(os.path.splitext(os.path.basename(config.keosd_exe()))[0])


def node_stop(verbose=True):
    # You can see if the process is a zombie by using top or 
    # the following command:
    # ps aux | awk '$8=="Z" {print $2}'
    pids = kill(os.path.splitext(os.path.basename(config.node_exe()))[0])
    
    if verbose:
        logger.INFO("""
Local node is stopped {}.
        """.format(str(pids)))        

    
def node_is_running():
    return not get_pid()

