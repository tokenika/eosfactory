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
import json
import time
import re
import pathlib
import setup


setup_setup = setup.Setup()


class _Control:
    """ A prototype for the control classes.

    Each control class represents a call to a Tokenika `teos` instance that
    is launched to responce just the call. 
    """
    global setup_setup

    error = False
    _out = ""
    json = json.loads("{}")

    def __init__(
                self, jarg, first, second, 
                is_verbose=True, suppress_error_msg=False):
        self.jarg = jarg

        cl = [setup_setup.teos_exe, first, second,
            "--jarg", str(self.jarg).replace("'", '"'), "--both"]

        if setup_setup.is_verbose() and is_verbose:
            cl.append("-V")

        process = subprocess.run(
            cl,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=str(pathlib.Path(setup_setup.teos_exe).parent)) 

        # Both, right and error output is passed with stdout:
        self._out = process.stdout.decode("utf-8")

        # With "--both", json output is passed with stderr: 
        json_resp = process.stderr.decode("utf-8")

        if setup_setup.is_verbose() and is_verbose:
            print(self._out)
     
        if re.match(r'^ERROR', self._out):
            self.error = True
            if not suppress_error_msg and not setup_setup.is_suppress_error_msg():
                print(self._out)
        try:
            self.json = json.loads(json_resp)
        except:
            self.json = json_resp

    def __str__(self):
        return self._out
    
    def __repr__(self):
        return repr(self.json)


class GetConfig(_Control):
    """
    Get the configurationt of the teos executable.
    """
    def __init__(self, contract_dir="", is_verbose=True):
        jarg = json.loads("{}")
        jarg["contract-dir"] = contract_dir
        _Control.__init__(self, jarg, "get", "config", is_verbose) 


class Template(_Control):
    def __init__(
            self, name, template="", remove_existing=False, 
            visual_studio_code=False, is_verbose=True
        ):

        jarg = json.loads("{}")
        jarg["name"] = name
        if template:
            jarg["template"] = template
        if remove_existing:
            jarg["remove"] = 1
        if visual_studio_code:
            jarg["vsc"] = 1

        _Control.__init__(self, jarg, "bootstrap", "contract", is_verbose)
        print(self.json)
 
    def contract_path(self):
        if not self.error:
            try:
                return self.json["contract_dir"] 
            except:
                self.error = True
                return "contract_path() ERROR!"
        else:
            return "contract_path() ERROR!"       
                   

class ABI(_Control):
    def __init__(
            self, source, code_name="", include_dir="", is_verbose=True):

        try:
            source = source.contract_dir
        except:
            pass

        jarg = json.loads("{}")
        jarg["sourceDir"] = source
        jarg["includeDir"] = include_dir
        jarg["codeName"] = code_name

        _Control.__init__(self, jarg, "generate", "abi", is_verbose)


class WAST(_Control):
    def __init__(
            self, source, code_name="", include_dir="", is_verbose=True):

        try:
            source = source.contract_dir
        except:
            pass

        jarg = json.loads("{}")
        jarg["sourceDir"] = source
        jarg["includeDir"] = include_dir
        jarg["codeName"] = code_name
        jarg["compileOnly"] = "0"

        _Control.__init__(self, jarg, "build", "contract", is_verbose) 

class NodeStart(_Control):
    def __init__(self, clear=0, is_verbose=True):
        jarg = json.loads("{}")
        jarg["delete-all-blocks"] = clear
        jarg["DO_NOT_LAUNCH"] = 1
        _Control.__init__(self, jarg, "daemon", "start", False)

        self.command_line = ""
        if not self.error and not "head_block_num" in self.json:
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
    def __init__(self, is_verbose=True):
        count = 15
        num = 5
        
        while True:
            time.sleep(1)
            self.get_info = GetInfo(is_verbose=False, suppress_error_msg=True)
            self.ok = False
            count = count - 1

            try:
                head_block_num = int(self.get_info.json["head_block_num"])
            except:
                head_block_num = -1

            if head_block_num >= num:
                self.ok = True
                break      

            if count <= 0:
                break


class NodeStop(_Control):
    def __init__(self, is_verbose=True):
        jarg = json.loads("{}")
        _Control.__init__(self, jarg, "daemon", "stop", is_verbose)


def node_reset():
    node = NodeStart(1)
    probe = NodeProbe()


def node_start():
    node = NodeStart(0)
    probe = NodeProbe()


def node_stop():
    stop = NodeStop()

