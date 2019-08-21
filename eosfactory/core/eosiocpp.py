""""""

import os
import json

import eosfactory.core.errors as errors
import eosfactory.core.logger as logger
import eosfactory.core.utils as utils
import eosfactory.core.setup as setup
import eosfactory.core.config as config
import eosfactory.core.vscode as vscode
import eosfactory.core.teos as teos

WORKSPACE_FOLDER = "${workspaceFolder}"


def get_target_dir(contract_dir):

    path = os.path.join(contract_dir, "build")
    if os.path.exists(path):
        return path
        
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


def build(
        contract_dir_hint, c_cpp_properties_path=None,
        compile_only=False, is_test_mode=False, is_execute=False, 
        verbosity=None):
    """Produce ABI and WASM files.

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
    """
    contract_dir = config.contract_dir(contract_dir_hint)
    # contract_source_files[0] is directory, contract_source_files[1] is contents:
    contract_source_files = config.contract_source_files(contract_dir)
    c_cpp_properties = teos.get_c_cpp_properties(
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
                and vscode.TEST_OPTIONS in c_cpp_properties[teos.CONFIGURATIONS][0]:
        compile_options_ = c_cpp_properties[teos.CONFIGURATIONS][0]\
                                                        [vscode.TEST_OPTIONS]
    elif not is_test_mode \
                and vscode.CODE_OPTIONS in c_cpp_properties[teos.CONFIGURATIONS][0]:
        compile_options_ = c_cpp_properties[teos.CONFIGURATIONS][0]\
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
                    raise errors.Error("""
The option '-o' does not has its value set:
{}
                    """.format(compile_options_))

            if not os.path.isabs(target_path):
                target_path = os.path.join(build_dir, target_path)
                target_dir = os.path.dirname(target_path)
                if not os.path.exists(target_dir):
                    try:
                        os.makedirs(target_dir)
                    except Exception as e:
                        raise errors.Error("""
Cannot make directory set with the option '-o'.
{}
                        """.format(str(e)))
        
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
                        raise errors.Error("""
Cannot make directory set with the option '-abigen_output'.
{}
                        """.format(str(e)))

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
                raise errors.Error("""
The option '--src' does not has its value set:
{}
                """.format(compile_options_))

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
                    raise errors.Error("""
The source file
{} 
cannot be found. It is neither absolute nor relative to the contract directory
or relative to the 'src' directory.
                    """.format(input_file))

                temp = os.path.normpath(temp)
                if not temp in source_files:
                    source_files.append(temp)
        else:
            compile_options.append(entry)

    compile_options.append(recardian_dir)

    if not source_files:
        source_files = contract_source_files[1]
    
    if not source_files:
        raise errors.Error("""
Cannot find any source file (".c", ".cpp",".cxx", ".c++") in the contract folder.
        """)

    if not is_test_mode and len(source_files) > 1: 
            raise errors.Error("""
Cannot determine the source file of the contract. There is many files in 
the 'src' directory, namely:
{}
Specify the file with the compiler option '--src', for
example:
--src src_dir/hello.cpp
The file path is to be absolute or relative to the project directory.
            """.format("\n".join(source_files)))

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
        logger.TRACE("""
            Executing target
                {}
        """.format(target_path))
        command_line = [target_path]

        if setup.is_print_command_lines and setup.is_save_command_lines:
            setup.add_to__command_line_file(" ".join(command_line))
        if setup.is_print_command_lines or is_verbose:
            logger.DEBUG("""
                ######## command line:
                {}
                """.format(" ".join(command_line)), [logger.Verbosity.DEBUG])
        utils.long_process(command_line, build_dir, is_verbose=True, 
                                                            prompt=target_path)
        return

    command_line = [config.eosio_cpp()]

    if compile_only:
        command_line.append("-c")
    else:
        command_line.extend(["-o", target_path])

    for entry in c_cpp_properties[teos.CONFIGURATIONS][0][vscode.INCLUDE_PATH]:
        if WORKSPACE_FOLDER in entry:
            entry = entry.replace(WORKSPACE_FOLDER, contract_dir)
            command_line.append("-I=" + teos.linuxize_path(entry))
        else:
            path = teos.linuxize_path(entry)
            if not path in config.eosio_cpp_includes():
                command_line.append(
                    "-I=" + path)

    for entry in c_cpp_properties[teos.CONFIGURATIONS][0][vscode.LIBS]:
        command_line.append(
            "-l=" + teos.linuxize_path(entry))

    for entry in compile_options:
        command_line.append(entry)

    for input_file in source_files:
        command_line.append(input_file)

    if setup.is_print_command_lines and setup.is_save_command_lines:
        setup.add_to__command_line_file(" ".join(command_line))
    if setup.is_print_command_lines or is_verbose:
        logger.DEBUG("""
            ######## command line:
            {}
            """.format(" ".join(command_line)), [logger.Verbosity.DEBUG])
        
    utils.long_process(command_line, build_dir, is_verbose=True, 
                                                            prompt="eosio-cpp")
    if not compile_only:
        if "wasm" in target_path:
            logger.TRACE("""
                ABI file writen to file: 
                    {}
                """.format(os.path.normpath(abigen_path)), verbosity)        
            logger.TRACE("""
                WASM file writen to file: 
                    {}
                """.format(os.path.normpath(target_path)), verbosity)
        else:
            logger.TRACE("""
                terget writen to file: 
                    {}
                """.format(os.path.normpath(target_path)), verbosity)
    print("eosio-cpp: OK")            
