import enum
import re
import inspect
from termcolor import cprint, colored
import setup

def translate(msg):
    import eosf
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    msg = ansi_escape.sub('', msg)
    return eosf.accout_names_2_object_names(setup.heredoc(msg))


class Error:
    def __init__(self, msg, is_fatal=True):
        self.msg = translate(msg)
        self.is_fatal = is_fatal


class AccountNotExist(Error):
    msg_template = '''
Account ``{}`` does not exist in the blockchain. It may be created.
'''
    def __init__(self, msg):
        Error.__init__(self, msg, True)


class WalletExists:
    msg_template = '''
Account ``{}`` does not exist in the blockchain. It may be created.
'''
    def __init__(self, msg):
        Error.__init__(self, msg, True)


class WalletNotExist:
    msg_template = '''
Wallet ``{}`` does not exist.
'''
    def __init__(self, msg):
        Error.__init__(self, msg, True)


class InvalidPassword:
    msg_template = '''
Invalid password for wallet {}.
'''
    def __init__(self, msg):
        Error.__init__(self, msg, True)


class LowRam:
    msg_template = '''
Ram needed is {}kB, deficiency is {}kB.
'''
    def __init__(self, needs_byte, deficiency_byte):
        self.needs_kbyte =  needs_byte// 1024 + 1
        self.deficiency_kbyte = deficiency_byte // 1024 + 1
        Error.__init__(self, self.msg_template.format(
            self.needs_kbyte, self.deficiency_kbyte), True)   

class Verbosity(enum.Enum):
    COMMENT = ['green', None, []]
    INFO = ['blue', None, ['bold']] # has to differ from TRACE! (enum!!!)
    TRACE = ['blue', None, []]
    ERROR = ['red', None, ['reverse']]
    ERROR_TESTING = ['green', None, ['reverse']]
    OUT = [None, None, []]
    DEBUG = ['yellow', None, []]

_is_throw_error = True
def set_throw_error(status=True):
    global _is_throw_error
    _is_throw_error = status

_is_testing_error = False
def set_is_testing_errors(status=True):
    '''Changes the color of the ``ERROR`` logger printout.

    Makes it less alarming.
    '''
    global _is_testing_error
    if status:
        _is_testing_error = True
        set_throw_error(False)
    else:
        _is_testing_error = False
        set_throw_error(True)

class Logger():
    verbosity = [Verbosity.TRACE, Verbosity.OUT, Verbosity.DEBUG]
    RECENT_ERROR = None

    def __init__(self, verbosity=None):
        if verbosity is None:
            self._verbosity = Logger.verbosity
        else:
            self._verbosity = verbosity

        self.cleos_object = None
        self.trace_buffer = ""
        self.out_buffer = ""
        self.out_info_buffer = ""
        self.error_buffer = ""
        self.debug_buffer = ""

    def COMMENT(self, msg):
        frame = inspect.stack()[1][0]
        test_name = inspect.getframeinfo(frame).function
        color = Verbosity.COMMENT.value
        cprint(
            "\n###  " + test_name + ":\n" + translate(msg) + "\n",
            color[0], color[1], attrs=color[2])

    def SCENARIO(self, msg):
        self.COMMENT(msg)

    def TRACE(self, msg, do=False):
        msg = translate(msg)
        self.trace_buffer = msg
        if msg and (Verbosity.TRACE in self._verbosity or do):
            color = Verbosity.TRACE.value
            cprint(msg, color[0], color[1], attrs=color[2])

    def INFO(self, msg, do=False):
        if msg and (
                Verbosity.TRACE in self._verbosity or
                Verbosity.INFO in self._verbosity or
                do
            ):
            color = Verbosity.INFO.value
            cprint(translate(msg), color[0], color[1], attrs=color[2])        

    def OUT(self, msg, do=False):
        if msg and (Verbosity.OUT in self._verbosity or do):
            color = Verbosity.OUT.value
            cprint(translate(msg), color[0], color[1], attrs=color[2])

    def DEBUG(self, msg, do=False):
        msg = translate(msg)
        self.debug_buffer = msg

        if msg and (Verbosity.DEBUG in self._verbosity or do):
            color = Verbosity.DEBUG.value
            cprint(msg, color[0], color[1], attrs=color[2])

    def error_map(self, err_msg):
        if "main.cpp:3008" in err_msg:
            return AccountNotExist(
                AccountNotExist.msg_template.format(self.name))

        if "Error 3080001: Account using more than allotted RAM" in err_msg:
            needs = int(re.search('needs\s(.*)\sbytes\shas', err_msg).group(1))
            has = int(re.search('bytes\shas\s(.*)\sbytes', err_msg).group(1))
            return LowRam(needs, (needs - has))

        if "transaction executed locally, but may not be" in err_msg:
            return None

        if "Wallet already exists" in err_msg:
            return WalletExists(
                WalletExists.msg_template.format(self.name))

        if "Error 3120002: Nonexistent wallet" in err_msg:
            return WalletNotExist(
                WalletNotExist.msg_template.format(self.name))
 
        if "Invalid wallet password" in err_msg:
            return InvalidPassword(
                InvalidPassword.msg_template.format(self.name))
        
        #######################################################################
        # NOT ERRORS
        #######################################################################
        
        if "Error 3120008: Key already exists" in err_msg:
            return None                

        if not err_msg:
            return None
        return Error(err_msg)

    def switch(self, cleos_object_or_str):       
        cleos_object_or_str.error_object = \
            self.error_map(cleos_object_or_str.err_msg)

        return cleos_object_or_str   
                     
    def ERROR_OBJECT(self, err_msg):
        try:
            cleos_object = self.switch(err_msg)
            return cleos_object.error_object
        except:
            return None

    def ERROR(self, cleos_or_str=None, is_silent=False, is_fatal=True):
        '''Print an error message or throw 'Exception'.

If the ``verbosity`` parameter is empty list, do nothing.

The 'cleos_or_str' argument may be a string error message or any object having the string attribute ``err_msg``.

If 'set_throw_error(True)', an `Exception object is thrown, otherwise the
message is printed.

arguments:
cleos_or_str -- error message string or object having the attribute err_msg
        '''
        Logger.RECENT_ERROR = None

        if cleos_or_str is None:
            cleos_or_str = self

        cleos_object = None
        if not isinstance(cleos_or_str, str):
            if not cleos_or_str.error:
                return False

            cleos_object = self.switch(cleos_or_str)
            if cleos_object.error_object is None:
                return False
                
            Logger.RECENT_ERROR = cleos_object.error_object           
            msg = cleos_object.error_object.msg
        else:
            msg = cleos_or_str

        if not msg or not self._verbosity or is_silent:
            return True
        
        if _is_testing_error:
            color = Verbosity.ERROR_TESTING.value
        else:
            color = Verbosity.ERROR.value

        msg = colored(
            "ERROR:\n{}".format(translate(msg)), 
            color[0], color[1], attrs=color[2])  + "\n"
        if not cleos_object is None:
            cleos_object.error_object.msg = msg

        self.error_buffer = msg
        global _is_throw_error

        if _is_throw_error and is_fatal:
            raise Exception(msg)
        else:
            print(msg)

        return True
