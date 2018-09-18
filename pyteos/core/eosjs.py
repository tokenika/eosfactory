import subprocess
import json
import pathlib
import re

import core.errors as errors
import core.config
import shell.setup as setup
import core.logger as logger


# TO DO resolve this code reuse issue.
def set_local_nodeos_address_if_none():
    if not setup.nodeos_address():
        setup.set_nodeos_address(
            "http://" + pyteos.core.config.getHttpServerAddress())
        setup.is_local_address = True

    return setup.is_local_address


class _Eosjs():
    '''A prototype for ``cleos`` command classes.
    '''

    def __init__(self, js, is_verbose=1):
        self.out_msg = None
        self.err_msg = None
        self.error = False
        self.json = None
        self.is_verbose = is_verbose
        cl = ["node", "-e"]
        cl.append(js)
        self.js = js 

        set_local_nodeos_address_if_none()
        # cl.extend(["--url", setup.nodeos_address()])

        if setup.is_print_request:
            cl.append("--print-request")
        if setup.is_print_response:
            cl.append("--print-response")

        if setup.is_print_command_line:
            print("command line sent to cleos:")
            print(" ".join(cl))
            print("")

        process = subprocess.run(
            cl,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE) 

        self.err_msg = process.stderr.decode("utf-8")
        if self.err_msg:
            self.error = True
            raise errors.Error(self.err_msg)

        out = process.stdout.decode("utf-8")
        if "FetchError:" in out:
            out = out[out.find("{") + 2 :out.find("}")]
            self.err_msg = out
            self.error = True
            raise errors.Error(self.err_msg)
        else:
            out = out[out.find("{"):]
            self.out_msg = out
            
        try:
            out = out.replace("'", '"')
            out = out.replace(': ', '": ')
            search = re.compile(r'\s(?=[a-z])')
            out = re.sub(search, ' "', out)
            out = out.replace('"null', 'null')
            self.json = json.loads(out)
        except:
            pass      

    def printself(self):
        if self.is_verbose > 0 or self.is_verbose == 0 and self.err_msg:
            logger.OUT(self.__str__())

    def __str__(self):
        if self.err_msg:
            return self.err_msg
        else:
            out = self.out_msg
            if self.out_msg_details:
                out = out + self.err_msg
            return out

    def __repr__(self):
        return None


class GetInfo(_Eosjs):
    '''Get current blockchain information.

    - **parameters**::

        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.
    '''
    def __init__(self, is_verbose=1):

        _Eosjs.__init__(
            self, 
            '''
    const Eos = require('eosjs'); 
    Eos().getInfo(
        (error, result) => {console.log(error, result);}
    );
            ''', 
            is_verbose)

        if not self.error:
            self.head_block = self.json["head_block_num"]
            self.head_block_time = self.json["head_block_time"]
            self.last_irreversible_block_num \
                = self.json["last_irreversible_block_num"]
            self.printself()

    def __str__(self):
        return json.dumps(self.json, sort_keys=True, indent=4)


def get_last_block():
    info = GetInfo(is_verbose=0)
    return GetBlock(info.head_block)


def get_block_trx_data(block_num):
    block = GetBlock(block_num, is_verbose=0)
    trxs = block.json["transactions"]
    if not len(trxs):
        logger.OUT("No transactions in block {}.".format(block_num))
    else:
        for trx in trxs:
            logger.OUT(trx["trx"]["transaction"]["actions"][0]["data"])


def get_block_trx_count(block_num):
    block = GetBlock(block_num, is_verbose=0)
    trxs = block.json["transactions"]
    if not len(trxs):
        logger.OUT("No transactions in block {}.".format(block_num))    
    return len(trxs)


class GetBlock(_Eosjs):
    '''Retrieve a full block from the blockchain.

    - **parameters**::
    
        block_number: The number of the block to retrieve.
        block_id: The ID of the block to retrieve, if set, defaults to "".
        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.
            
    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.    
    '''
    def __init__(self, block_number, block_id=None, is_verbose=1):
        block =  block_id if block_id else str(block_number)
        _Eosjs.__init__(
            self,
'''
    const Eos = require('eosjs'); 
    Eos().getBlock(
        {}, 
        (error, result) => {{console.log(error, result);}}
    );
            '''.format(block),
            is_verbose)

        if not self.error:
            self.block_num = self.json["block_num"]
            self.ref_block_prefix = self.json["ref_block_prefix"]
            self.timestamp = self.json["timestamp"]
            self.printself()

    def __str__(self):
        return json.dumps(self.json, sort_keys=True, indent=4)