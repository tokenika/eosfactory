#!/usr/bin/python3

import os
import subprocess
import time
import re
import pathlib
import shutil
import pprint

import eosfactory.core.logger as logger
import eosfactory.core.utils as utils
import eosfactory.core.setup as setup
import eosfactory.core.config as config
import eosfactory.core.errors as errors


TEMPLATE_CONTRACTS_DIR = "templates/contracts"
TEMPLATE_NAME = "CONTRACT_NAME"
TEMPLATE_EOSIO_DIR = "@EOSIO_DIR@"
TEMPLATE_HOME = "@HOME@"
TEMPLATE_ROOT = "@ROOT@"


def ABI(contract_dir_hint=None, code_name=None, include_dir=None):
    '''Given a hint to a contract directory, produce ABI file.
    '''
    contract_dir = config.contract_dir(contract_dir_hint)
    source = config.contract_source_files(contract_dir)
    srcs = source[1]
    if not srcs:
        raise errors.Error('''
        "The source is empty. The assumed contract dir is   
        {}
        '''.format(contract_dir))
        return

    if not code_name:
        code_name = os.path.splitext(os.path.basename(srcs[0]))[0]
    target_dir = get_target_dir(source[0])
    target_path_abi = os.path.normpath(
                        os.path.join(target_dir, code_name  + ".abi"))

    for src in srcs:
        srcPath = src
        if os.path.splitext(src)[1].lower() == ".abi":
            logger.INFO('''
            NOTE:
            An ABI exists in the source directory. Cannot overwrite it:
            {}
            Just copying it to the target directory.
            '''.format(src))
            shutil.move(
                srcPath, os.path.join(target_dir, 
                os.path.basename(srcPath)))
            return    

    eosio_abigen = None
    try:
        eosio_abigen = config.eosio_abigen()
    except:
        pass

    extensions = [".c", ".cpp",".cxx", ".c++"]
    if eosio_abigen:
        command_line = [config.eosio_abigen(), "-output=" + target_path_abi]
        for file in srcs:
            if not os.path.splitext(file)[1].lower() in extensions:
                continue
            command_line.append(file)
        
        try:
            process(command_line)
        except Exception as e:
            raise errors.Error(str(e))
    else:
        ###########################################################################
        # eosio.cdt is not available.        
        sourcePath = srcs[0]
        source_dir = os.path.dirname(srcs[0])

        command_line = [
            config.abigen_exe(),
            "-extra-arg=-c", "-extra-arg=--std=c++14", 
            "-extra-arg=--target=wasm32", "-extra-arg=-nostdinc", 
            "-extra-arg=-nostdinc++", "-extra-arg=-DABIGEN",
            "-extra-arg=-I" + config.eosio_repository_dir() + "/contracts/libc++/upstream/include",
            "-extra-arg=-I" + config.eosio_repository_dir() + "/contracts/musl/upstream/include",
            "-extra-arg=-I" + config.eosio_repository_dir() + "/externals/magic_get/include",
            "-extra-arg=-I" + config.boost_include_dir(),
            "-extra-arg=-I" + config.eosio_repository_dir() + "/contracts",
            "-extra-arg=-I" + config.eosio_repository_dir() + "/build/contracts",
            "-extra-arg=-I" + source_dir
        ]

        if include_dir:
            include_dirs = include_dir.split(",")
            for dir in include_dirs:
                command_line.append("-extra-arg=-I " + dir)

        command_line.extend(
            [
                "-extra-arg=-fparse-all-comments",
                "-destination-file=" + target_path_abi,
                # "-verbose=" + to_string(verbose),
                "-context=" + source_dir,
                sourcePath,
                "--"
            ]
        )

        if setup.is_print_command_line:
            print("######## {}:".format(config.abigen_exe()))
            print(" ".join(command_line))

        process(command_line)

    logger.TRACE('''
    ABI file writen to file: {}
    '''.format(target_path_abi))


def WAST(
        contract_dir_hint, code_name=None, include_dir=None, 
        compile_only=False):
    '''Given a hint to a contract directory, produce WAST and WASM code.
    '''

    contract_dir = config.contract_dir(contract_dir_hint)
    source = config.contract_source_files(contract_dir)
    srcs = source[1]
    if not srcs:
        raise errors.Error('''
        "The source is empty. The assumed contract dir is  
        {}
        '''.format(contract_dir))
        return

    targetPathWast = None
    target_dir_path = get_target_dir(source[0])

    workdir = os.path.join(target_dir_path, "working_dir")
    if not os.path.exists(workdir):
        os.makedirs(workdir)

    workdir_build = os.path.join(workdir, "build")
    if not os.path.exists(workdir_build):
        os.mkdir(workdir_build)    

    objectFileList = []
    extensions = [".h", ".hpp", ".hxx", ".c", ".cpp",".cxx", ".c++"]
    if not code_name:
        code_name = os.path.splitext(os.path.basename(srcs[0]))[0]
    targetPathWast = os.path.join(
        target_dir_path, code_name + ".wast")
    target_path_wasm = os.path.join(
        target_dir_path, code_name + ".wasm")

    eosio_cpp = None
    try:
        eosio_cpp = config.eosio_cpp()
    except:
        pass

    if eosio_cpp:
        command_line = [
            config.eosio_cpp(),
            "-o",
            target_path_wasm
            ]
        for file in srcs:
            if not os.path.splitext(file)[1].lower() in extensions:
                continue
            command_line.append(file)

        try:
            process(command_line)
        except Exception as e:                       
            raise errors.Error(str(e))
    else:
        ###########################################################################
        # eosio.cdt is not available.
        for file in srcs:
            if not os.path.splitext(file)[1].lower() in extensions:
                continue

            command_line = [
                config.wasm_clang_exe(),
                "-emit-llvm", "-O3", "--std=c++14", "--target=wasm32", "-nostdinc",
                #"-DBOOST_DISABLE_ASSERTS -DBOOST_EXCEPTION_DISABLE",
                "-nostdlib", "-nostdlibinc", "-ffreestanding", "-nostdlib",
                "-fno-threadsafe-statics", "-fno-rtti", "-fno-exceptions",
                "-I", config.eosio_repository_dir() 
                    + "/contracts/libc++/upstream/include",
                "-I", config.eosio_repository_dir() 
                    + "/contracts/musl/upstream/include",
                "-I", config.eosio_repository_dir() 
                    + "/externals/magic_get/include",
                "-I", config.boost_include_dir(),
                "-I", config.eosio_repository_dir() + "/contracts",
                "-I", config.eosio_repository_dir() + "/build/contracts",
                "-I", contract_dir
            ]

            if include_dir:
                include_dirs = include_dir.split(",")
                for dir in include_dirs:
                    command_line.extend(["-I", dir])

            output = os.path.join(workdir_build, code_name + ".o")
            objectFileList.append(output)        
            command_line.extend(["-c", file, "-o", output])
            
            if setup.is_print_command_line:
                print("######## {}:".format(config.wasm_clang_exe()))
                print(" ".join(command_line))

            try:
                process(command_line)
            except Exception as e:
                try:
                    shutil.rmtree(workdir)
                except:
                    pass
                            
                raise errors.Error(str(e))

        if not compile_only:
            command_line = [ 
                config.wasm_llvm_link_exe(),
                "-only-needed", 
                "-o",  workdir + "/linked.bc",
                " ".join(objectFileList),
                config.eosio_repository_dir() + "/build/contracts/musl/libc.bc",
                config.eosio_repository_dir() + "/build/contracts/libc++/libc++.bc",
                config.eosio_repository_dir() + "/build/contracts/eosiolib/eosiolib.bc"
            ]
            if setup.is_print_command_line:
                print("######## {}:".format(config.wasm_llvm_link_exe()))
                print(" ".join(command_line))

            try:
                process(command_line)
            except Exception as e:                           
                raise errors.Error(str(e))

            command_line = [
                config.wasm_llc_exe(),
                "-thread-model=single", "--asm-verbose=false",
                "-o", workdir + "/assembly.s",
                workdir + "/linked.bc"
            ]
            if setup.is_print_command_line:
                print("######## {}:".format(config.wasm_llc_exe()))
                print(" ".join(command_line))

            try:
                process(command_line)
            except Exception as e:
                raise errors.Error(str(e))
                try:
                    shutil.rmtree(workdir)
                except:
                    pass
                            
                raise errors.Error(str(e))          

            command_line = [
                config.s2wasm_exe(),
                "-o", targetPathWast,
                "-s", "16384",
                workdir + "/assembly.s"
            ]
            if setup.is_print_command_line:
                print("######## {}:".format(config.s2wasm_exe()))
                print(" ".join(command_line))

            try:
                process(command_line)
            except Exception as e:
                try:
                    shutil.rmtree(workdir)
                except:
                    pass
                            
                raise errors.Error(str(e))

            logger.TRACE('''
            WAST file writen to file: {}
            '''.format(os.path.normpath(targetPathWast)))                      

            command_line = [
                config.wast2wasm_exe(), 
                targetPathWast, target_path_wasm, "-n"]

            if setup.is_print_command_line:
                print("######## {}:".format(config.wast2wasm_exe()))
                print(" ".join(command_line))

            try:
                process(command_line)
            except Exception as e:
                try:
                    shutil.rmtree(workdir)
                except:
                    pass
                            
                raise errors.Error(str(e))
        try:
            shutil.rmtree(workdir)
        except:
            pass

    logger.TRACE('''
    WASM file writen to file: {}
    '''.format(os.path.normpath(target_path_wasm)))

def template_create(
        project_name, template_dir=None, workspace_dir=None, 
        remove_existing=False, open_vscode=False, throw_exists=False):
    '''Given the project name and template name, create a smart contract project.
    '''
    project_name = project_name.strip()

    template_dir = template_dir.strip()    
    template_dir = utils.wslMapWindowsLinux(template_dir)
    if not template_dir:
        template_dir = config.DEFAULT_TEMPLATE
    if not os.path.isdir(template_dir):
        template_dir = os.path.join(
            config.eosf_dir(), TEMPLATE_CONTRACTS_DIR, template_dir) 
    if not os.path.isdir(template_dir):
        raise errors.Error('''
        TemplateCreate '{}' does not exist.
        '''.format(template_dir)) 
       
    if not workspace_dir \
                            or not os.path.isabs(workspace_dir) \
                            or not os.path.exists(workspace_dir):
        workspace_dir = config.contract_workspace()
    workspace_dir = workspace_dir.strip()

    project_name = utils.wslMapWindowsLinux(project_name.strip())
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
            
        
        template = template.replace(
                            "@" + TEMPLATE_NAME + "@", project_name)
        with open(contract_path, "w") as output:
            output.write(template)

    copy_dir_contents(project_dir, template_dir, "", project_name)
    logger.TRACE('''
    * Contract project '{}' created from template '{}'
    '''.format(project_name, project_dir))    

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

    return project_dir


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
    
    target_dir = os.path.join(source_dir, "..", "build")
    if os.path.exists(target_dir):
        return target_dir

    target_dir = os.path.join(source_dir, "build")
    if not os.path.exists(target_dir):
        try:
            os.mkdir(target_dir)
        except Exception as e:
            raise errors.Error(str(e))

    return target_dir


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


def node_start(clear=False, verbosity=None):
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
        args_.insert(0, config.node_exe())
        subprocess.Popen(
            " ".join(args_), 
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL, shell=True)

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

