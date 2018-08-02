#!/usr/bin/python3

"""
Python front-end for C++ `teos` controll classes, which implement functionality 
needed for EOSIO smart-contract development process, yet not available form the
EOSIO `cleos`.

.. module:: pyteos
    :platform: Unix, Windows
    :synopsis: Python front-end for C++ `teos` controll classes which implement 
        functionality needed for EOSIO smart-contract development process, yet 
        not available form the EOSIO `cleos`.

.. moduleauthor:: Tokenika

"""

import os
import subprocess
import json as json_module
import time
import re
import pathlib
import setup
import cleos
import shutil


setup_setup = setup.Setup()

class _Teos:
    """ A prototype for the control classes.

    Each control class represents a call to a Tokenika `teos` instance that
    is launched to responce just the call. 
    """
    global setup_setup

    error = False
    err_msg = ""
    is_verbose = True
    json = json_module.loads("{}")

    def __init__(
                self, jarg, first, second, 
                is_verbose_arg=True):

        self.jarg = jarg     

        cl = [setup_setup.teos_exe, first, second,
            "--jarg", str(self.jarg).replace("'", '"'), "--both"]

        if setup.is_verbose() and is_verbose_arg:
            cl.append("-V")

        if setup.is_print_request():
            print("REQUEST:")
            print("---------------------")
            print(json_module.dumps(jarg))
            print("---------------------")
            print("")   

        if setup.is_print_command_line():
            print("command line sent to cleos:")
            print(" ".join(cl))
            print("")

        process = subprocess.run(
            cl,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=str(pathlib.Path(setup_setup.teos_exe).parent)) 

        # Both, right and error output is passed with stdout:
        self.out_msg = process.stdout.decode("utf-8")

        # With "--both", json output is passed with stderr: 
        json_resp = process.stderr.decode("utf-8")

        self.is_verbose = setup.is_verbose() and is_verbose_arg

        if setup.is_print_response():
            print("RESPONSE:")
            print("---------------------")
            print(json_module.dumps(json_module.loads(json_resp), indent=4))
            print("---------------------")
            print("")

        if self.is_verbose:
            print(self.out_msg)
     
        if re.match(r'^ERROR', self.out_msg):
            self.error = True
            if is_verbose_arg >= 0 and setup.is_verbose() >= 0:
                print(self.out_msg)
        try:
            self.json = json_module.loads(json_resp)
        except:
            self.json = json_resp

    def __str__(self):
        return self.out_msg
    
    def __repr__(self):
        return repr(self.json)

class GetConfig(_Teos):
    """
    Get the configurationt of the teos executable.
    """
    def __init__(self, contract_dir="", is_verbose=1):
        jarg = json_module.loads("{}")
        jarg["contract-dir"] = contract_dir
        _Teos.__init__(self, jarg, "get", "config", is_verbose) 


def get_node_wallet_dir():
    """
    Get the directory of the `nodeos` local wallet.
    """
    return GetConfig(is_verbose=0).json["EOSIO_WALLET_DIR"]


def get_keosd_wallet_dir():
    """
    Get the directory of the `nodeos` local wallet.
    """
    return GetConfig(is_verbose=0).json["KEOSD_WALLET_DIR"]


class TemplateCreate(_Teos):
    def __init__(
            self, name, template="", user_workspace="", remove_existing=False, 
            visual_studio_code=False, is_verbose=1
        ):

        jarg = json_module.loads("{}")
        jarg["name"] = name
        if not user_workspace is None:
            jarg["workspace"] = user_workspace
        if template:
            jarg["template"] = template
        if remove_existing:
            jarg["remove"] = 1
        if visual_studio_code:
            jarg["vsc"] = 1

        _Teos.__init__(self, jarg, "template", "create", is_verbose)
        try:
            self.contract_path_absolute = self.json["contract_dir"] 
            self.contract_build_path = self.json["contract_build_path"]
        except:
            pass
        
        if self.is_verbose:
            print(self.out_msg)
 

    def delete(self):
        try:
            shutil.rmtree(str(self.contract_path_absolute))
            return True
        except:
            return False
                   

class ABI(_Teos):
    def __init__(
            self, source, code_name="", include_dir="", is_verbose=1):

        try:
            source = source.contract_dir
        except:
            pass

        jarg = json_module.loads("{}")
        jarg["sourceDir"] = source
        jarg["includeDir"] = include_dir
        jarg["codeName"] = code_name

        _Teos.__init__(self, jarg, "generate", "abi", is_verbose)


class WAST(_Teos):
    def __init__(
            self, source, code_name="", include_dir="", is_verbose=1):

        try:
            source = source.contract_dir
        except:
            pass

        jarg = json_module.loads("{}")
        jarg["sourceDir"] = source
        jarg["includeDir"] = include_dir
        jarg["codeName"] = code_name
        jarg["compileOnly"] = "0"

        _Teos.__init__(self, jarg, "build", "contract", is_verbose)        

class NodeStart(_Teos):
    def __init__(self, clear=0, is_verbose=1):
        jarg = json_module.loads("{}")
        jarg["delete-all-blocks"] = clear
        jarg["DO_NOT_LAUNCH"] = 1
        _Teos.__init__(self, jarg, "daemon", "start", is_verbose)

        self.command_line = ""

        if not self.error:
            if "DO_NOT_LAUNCH" in self.json and self.json["DO_NOT_LAUNCH"]:
                return
                
            self.command_line = self.json["command_line"]
            if self.json["is_windows_ubuntu"] == "true":
                subprocess.call(
                    ["cmd.exe", "/c", "start", "/MIN", "bash.exe", "-c", 
                    self.json["command_line"]])
            else:
                if self.json["uname"] == "Darwin":
                    subprocess.Popen(
                        "open -a "
                        + self.json["exe"] + " --args " + self.json["args"],
                        shell=True)
                else:
                    subprocess.Popen(
                        "gnome-terminal -- " + self.json["command_line"],
                        shell=True)                    

class NodeProbe:
    error = True
    get_info = ""
    err_msg = ""

    def __init__(self, is_verbose=1):
        count = 15
        num = 5
        block_num = None
       
        while True:
            time.sleep(1)
            self.get_info = cleos.GetInfo(is_verbose=-1)
            self.ok = False
            count = count - 1
            print(".", end="", flush=True)

            try:
                head_block_num = int(self.get_info.json["head_block_num"])
            except:
                head_block_num = 0

            if block_num is None:
                block_num = head_block_num

            if head_block_num - block_num >= num:
                self.error = False
                break      

            if count <= 0:
                self.err_msg = """
                The local node do not response. 
                """
                if is_verbose >= 0:
                    print("ERROR:")
                    print(self.err_msg)
                    print()                    
                break
        
class NodeStop(_Teos):
    def __init__(self, is_verbose=1):
        jarg = json_module.loads("{}")
        _Teos.__init__(self, jarg, "daemon", "stop", is_verbose)                    
    
class NodeIsRunning(_Teos):
    daemon_pid = ""
    def __init__(self, is_verbose=1):
        jarg = json_module.loads("{}")
        _Teos.__init__(self, jarg, "daemon", "isrunning", is_verbose)

        if not self.error:
            self.daemon_pid = self.json["daemon_pid"]



