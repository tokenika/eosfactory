#!/usr/bin/python3

import os
import subprocess
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
import eosfactory.core.teos as teos


TEMPLATE_CONTRACTS_DIR = "templates/contracts"
TEMPLATE_NAME = "CONTRACT_NAME"
TEMPLATE_EOSIO_DIR = "${EOSIO_DIR}"
TEMPLATE_HOME = "${HOME}"
TEMPLATE_ROOT = "${ROOT}"
C_CPP_PROP = "${c_cpp_prop}"
TASK_JSON = "${tasks}"
INCLUDES = [
        "${EOSIO_DIR}/contracts",
        "${EOSIO_DIR}/contracts/libc++/upstream/include",
        "${EOSIO_DIR}/contracts/musl/upstream/include",
        "${HOME}/opt/boost/include",
        "${ROOT}/usr/local/include/",
        "${EOSIO_DIR}/externals/magic_get/include",
        "${workspaceFolder}"
    ]
LIBS = [
        "${EOSIO_DIR}/build/contracts/musl/libc.bc",
        "${EOSIO_DIR}/build/contracts/libc++/libc++.bc",
        "${EOSIO_DIR}/build/contracts/eosiolib/eosiolib.bc"
]
COMPILER_OPTIONS = [
    "-emit-llvm", 
    "-O3", 
    "--std=c++14", 
    "--target=wasm32", 
    "-nostdinc",
    "-nostdlib", 
    "-nostdlibinc", 
    "-ffreestanding", 
    "-nostdlib",
    "-fno-threadsafe-statics", 
    "-fno-rtti", 
    "-fno-exceptions"
]
TASKS = '''
{
    "version": "2.0.0",   
    "tasks": [
        {
            "taskName": "Compile",
            "type": "shell",
            "windows": {
                "options": {
                    "shell": {
                        "executable": "bash.exe",
                        "args": [
                            "-c"
                        ]
                    }
                },
                "command": "mkdir -p build; python3 -m eosfactory.eoside.build '${workspaceFolder}' --compile"
            },
            "osx": {
                "command": "mkdir -p build; python3 -m eosfactory.eoside.build '${workspaceFolder}' --compile"
            },
            "linux": {
                "command": "mkdir -p build; python3 -m eosfactory.eoside.build '${workspaceFolder}' --compile"
            },
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            },
            "problemMatcher": [
            ]
        },
        {
            "taskName": "Build",
            "type": "shell",
            "windows": {
                "options": {
                    "shell": {
                        "executable": "bash.exe",
                        "args": [
                            "-c"
                        ]
                    }
                },
                "command": "mkdir -p build; python3 -m eosfactory.eoside.build '${workspaceFolder}'"        
            },
            "osx": {
                "command": "mkdir -p build; python3 -m eosfactory.eoside.build '${workspaceFolder}'"
            },
            "linux": {
                "command": "mkdir -p build; python3 -m eosfactory.eoside.build '${workspaceFolder}'"
            },
            "problemMatcher": [],
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            },
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "problemMatcher": [
            ]
        },
        {
            "taskName": "Test",
            "type": "shell",
            "windows": {
                "options": {
                    "shell": {
                        "executable": "bash.exe",
                        "args": [
                            "-c"
                        ]
                    }
                },            
                "command": "python3 ./tests/test1.py"
            },
            "osx": {
                "command": "python3 ./tests/test1.py"
            },
            "linux": {
                "command": "python3 ./tests/test1.py"
            },
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            },
            "problemMatcher": [
            ]
        },
        {
            "taskName": "Unittest",
            "type": "shell",
            "windows": {
                "options": {
                    "shell": {
                        "executable": "bash.exe",
                        "args": [
                            "-c"
                        ]
                    }
                },            
                "command": "python3 ./tests/unittest1.py"
            },
            "osx": {
                "command": "python3 ./tests/unittest1.py"
            },
            "linux": {
                "command": "python3 ./tests/unittest1.py"
            },
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            },
            "problemMatcher": [
            ]
        },
        {
            "taskName": "EOSIO API",
            "type": "shell",
            "windows": {
                "options": {
                    "shell": {
                        "executable": "bash.exe",
                        "args": [
                            "-c"
                        ]
                    }
                },            
                "command": "explorer.exe"
            },
            "osx": {
                "command": "open"
            },
            "linux": {
                "command": "sensible-browser"
            },
            "args": [
                "https://developers.eos.io/eosio-cpp/reference"
            ],
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            },
            "problemMatcher": [
            ]
        }
    ]
}
'''

c_cpp_properties_default = """
{
    "configurations": [
        {
            "includePath": %s,
            "libs": %s,
            "compilerOptions": %s,
            "defines": [],
            "intelliSenseMode": "clang-x64",
            "browse": {
                "path": %s,
                "limitSymbolsToIncludedHeaders": true,
                "databaseFilename": ""
            }
        }
    ],
    "version": 4
}
""" % (
    json.dumps(INCLUDES, indent=4),
    json.dumps(LIBS, indent=4),
    json.dumps(COMPILER_OPTIONS, indent=4),
    json.dumps(INCLUDES, indent=4))


def replace_templates(string): 
    home = os.environ["HOME"]
    root = ""
    eosio_dir = config.eosio_repository_dir()
    if teos.is_windows_ubuntu():
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
        return json.loads(replace_templates(c_cpp_properties_default))


def ABI(
        contract_dir_hint=None, c_cpp_properties_path=None,
        verbosity=None):
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

    code_name = os.path.splitext(os.path.basename(srcs[0]))[0]
    target_dir = teos.get_target_dir(source[0])
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
            '''.format(src), verbosity)
            shutil.move(
                srcPath, os.path.join(target_dir, 
                os.path.basename(srcPath)))
            return 

    extensions = [".c", ".cpp",".cxx", ".c++"]
    sourcePath = srcs[0]
    source_dir = os.path.dirname(srcs[0])

    command_line = [
        config.abigen_exe(),
        "-extra-arg=-c", "-extra-arg=--std=c++14", 
        "-extra-arg=--target=wasm32", "-extra-arg=-nostdinc", 
        "-extra-arg=-nostdinc++", "-extra-arg=-DABIGEN"
    ]
    c_cpp_properties = get_c_cpp_properties(
                                        contract_dir, c_cpp_properties_path)
    includes = c_cpp_properties["configurations"][0]["includePath"]
    for entry in includes:
        command_line.append("-extra-arg=-I" + strip_wsl_root(entry))
        if entry == "${workspaceFolder}":
            command_line.append("-extra-arg=-I" + source_dir)

    command_line.extend(
        [
            "-extra-arg=-fparse-all-comments",
            "-destination-file=" + target_path_abi,
            "-context=" + source_dir,
            sourcePath,
            "--"
        ]
    )

    if setup.is_print_command_line:
        print("######## {}:".format(config.abigen_exe()))
        print(" ".join(command_line))

    teos.process(command_line)

    logger.TRACE('''
    ABI file writen to file: {}
    '''.format(target_path_abi), verbosity)


def WAST(
        contract_dir_hint, c_cpp_properties_path=None,
        compile_only=False, verbosity=None):
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
    target_dir_path = teos.get_target_dir(source[0])

    workdir = os.path.join(target_dir_path, "working_dir")
    if not os.path.exists(workdir):
        os.makedirs(workdir)

    workdir_build = os.path.join(workdir, "build")
    if not os.path.exists(workdir_build):
        os.mkdir(workdir_build)    

    objectFileList = []
    extensions = [".h", ".hpp", ".hxx", ".c", ".cpp",".cxx", ".c++"]

    code_name = os.path.splitext(os.path.basename(srcs[0]))[0]
    targetPathWast = os.path.join(
        target_dir_path, code_name + ".wast")
    target_path_wasm = os.path.join(
        target_dir_path, code_name + ".wasm")

    c_cpp_properties = get_c_cpp_properties(
                                        contract_dir, c_cpp_properties_path)
    for file in srcs:
        if not os.path.splitext(file)[1].lower() in extensions:
            continue

        command_line = [
            config.wasm_clang_exe()
        ]

        options = c_cpp_properties["configurations"][0]["compilerOptions"]
        for entry in options:
            command_line.append(entry)

        includes = c_cpp_properties["configurations"][0]["includePath"]
        for entry in includes:
            command_line.append("-I" + strip_wsl_root(entry))
        if entry == "${workspaceFolder}":
            command_line.append("-I" + contract_dir)

        output = os.path.join(workdir_build, code_name + ".o")
        objectFileList.append(output)        
        command_line.extend(["-c", file, "-o", output])
        
        if setup.is_print_command_line:
            print("######## {}:".format(config.wasm_clang_exe()))
            print(" ".join(command_line))

        try:
            teos.process(command_line)
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
            " ".join(objectFileList)
        ]

        links = c_cpp_properties["configurations"][0]["libs"]
        for entry in links:
            command_line.append(strip_wsl_root(entry))

        if setup.is_print_command_line:
            print("######## {}:".format(config.wasm_llvm_link_exe()))
            print(" ".join(command_line))

        try:
            teos.process(command_line)
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
            teos.process(command_line)
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
            teos.process(command_line)
        except Exception as e:
            try:
                shutil.rmtree(workdir)
            except:
                pass
                        
            raise errors.Error(str(e))

        logger.TRACE('''
        WAST file writen to file: {}
        '''.format(os.path.normpath(targetPathWast)), verbosity)                      

        command_line = [
            config.wast2wasm_exe(), 
            targetPathWast, target_path_wasm, "-n"]

        if setup.is_print_command_line:
            print("######## {}:".format(config.wast2wasm_exe()))
            print(" ".join(command_line))

        try:
            teos.process(command_line)
        except Exception as e:
            try:
                shutil.rmtree(workdir)
            except:
                pass
                        
            raise errors.Error(str(e))
        
        logger.TRACE('''
            WASM file writen to file: {}
            '''.format(os.path.normpath(target_path_wasm)), verbosity)
    try:
        shutil.rmtree(workdir)
    except:
        pass

def project_from_template(
        project_name, template=None, workspace_dir=None,
        c_cpp_prop=None 
        remove_existing=False, 
        open_vscode=False, throw_exists=False, 
        verbosity=None):
    '''Given the project name and template name, create a smart contract project.

    - **parameters**::

        project_name: The name of the project, or an existing path to 
            a directory.
        template: The name of the template used, defaults to 
            config.DEFAULT_TEMPLATE, or an existing path to a directory.
        workspace_dir: If set, the folder for the work-space. Defaults to the 
            value returned by the config.contract_workspace() function.
        remove_existing: If set, overwrite any existing project.
        visual_studio_code: If set, open the ``VSCode``, if available.
        verbosity: The logging configuration.
    '''
    project_name = project_name.strip()
    template = template.strip()    
    template = utils.wslMapWindowsLinux(template)
    if not template:
        template = config.DEFAULT_TEMPLATE
    if not os.path.isdir(template):
        template = os.path.join(
            config.eosf_dir(), TEMPLATE_CONTRACTS_DIR, template) 
    if not os.path.isdir(template):
        raise errors.Error('''
        TemplateCreate '{}' does not exist.
        '''.format(template)) 
       
    if not workspace_dir \
                            or not os.path.isabs(workspace_dir) \
                            or not os.path.exists(workspace_dir):
        workspace_dir = config.contract_workspace()
    workspace_dir = workspace_dir.strip()

    if c_cpp_prop:
        if os.path.exists(c_cpp_prop):
            try:
                with open(c_cpp_properties_path, "r") as input:
                    c_cpp_prop = json.loads(input.read())
            except Exception:
                c_cpp_prop = c_cpp_properties_default
    else:
        c_cpp_prop = c_cpp_properties_default

    c_cpp_prop = replace_templates(c_cpp_properties)

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
            if teos.is_windows_ubuntu():
                home = config.wsl_root() + home
                root = config.wsl_root()
                eosio_dir = config.wsl_root() + eosio_dir
            template = template.replace(TEMPLATE_HOME, home)
            template = template.replace(TEMPLATE_ROOT, root)
            template = template.replace(TEMPLATE_EOSIO_DIR, eosio_dir)
        import pdb; pdb.set_trace()
        template = template.replace("${" + TEMPLATE_NAME + "}", project_name)
        template = template.replace(C_CPP_PROP, c_cpp_properties)
        template = template.replace(TASK_JSON, TASKS)

        with open(contract_path, "w") as output:
            output.write(template)

    copy_dir_contents(project_dir, template, "", project_name)

    logger.TRACE('''
    * Contract project '{}' created from template '{}'
    '''.format(project_name, project_dir), verbosity)    

    if open_vscode:
        if teos.is_windows_ubuntu():
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
    '''.format(project_name, template), verbosity)

    return project_dir


def strip_wsl_root(path):
    wsl_root = config.wsl_root()
    return path.replace(wsl_root, "")
